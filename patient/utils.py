import requests
import logging
import os
import json
import os
from mistralai import Mistral
from doctor import models as dc_models 
from decouple import config
from datetime import datetime, timedelta
from doctor.models import WEEK_DAYS, MEAL_TYPES

logger = logging.getLogger(__name__)

from django.utils.translation import gettext as _
def process_ai_diet_request(  patient,  bmi, diabetes=None, obesity=None, diabetes_and_obesity=None, provider = None):
    """
        Sends user details to an AI service (e.g., OpenRouter or Mistral) to generate a diet plan.
    """
    try:
        # Construct the prompt with user details
        prompt = f"""
        Generate a personalized diet plan for the following patient:
        - BMI: {bmi.bmi_value}
        - Height: {bmi.height} cm
        - Weight: {bmi.weight} kg
        - Illnesses: {', '.join([illness.name for illness in bmi.sickness.all()])}
        """

        if diabetes:
            prompt += f"""
            - Diabetes Details:
              - Glucose Type: {diabetes.glucose_type}
              - Fasting Glucose: {diabetes.fasting_glucose}
              - HbA1c: {diabetes.hba1c}
              - Cholesterol: {diabetes.cholesterol}
            """

        if obesity:
            prompt += f"""
            - Obesity Details:
              - Glucose: {obesity.glucose}
              - HDL: {obesity.hdl}
              - LDL: {obesity.ldl}
              - Triglycerides: {obesity.triglycerides}
              - Cholesterol: {obesity.cholesterol}
              - AC Uric: {obesity.ac_uric}
            """

        if diabetes_and_obesity:
            prompt += f"""
            - Diabetes and Obesity Details:
              - Glucose: {diabetes_and_obesity.glucose}
              - HbA1c: {diabetes_and_obesity.hb1ac}
              - HDL: {diabetes_and_obesity.hdl}
              - LDL: {diabetes_and_obesity.ldl}
              - Triglycerides: {diabetes_and_obesity.triglycerides}
              - Cholesterol: {diabetes_and_obesity.cholesterol}
              - AC Uric: {diabetes_and_obesity.ac_uric}
              - FNS: {diabetes_and_obesity.fns}
              - CRP: {diabetes_and_obesity.crp}
              - Vitamin D: {diabetes_and_obesity.vitamin_d}
              - B12: {diabetes_and_obesity.b12}
              - Magnesium: {diabetes_and_obesity.magnesium}
            """

        if provider == "openrouter":
        # Send the prompt to the AI service
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {config('OPENROUTER_API_KEY')}",  # Replace with your OpenRouter API key
                "Content-Type": "application/json"
            }
            data = {
                "model": "google/gemini-2.5-pro-exp-03-25:free",  # Specify the AI model
                "messages": [
                    {
                        "role": "system",
                        "content": """
                            You are a helpful assistant that generates personalized diet plans using the provided patient details.
                            Rules: 
                            - provide a daily diet plan with breakfast, lunch, snaks, and dinner
                            - the week starts from saturday 
                            - just send the diet plan without any other text
                            - dont use nested objects
                            - example response:
                                {
                                    "saturday": 
                                        {
                                            "breakfast": "Oatmeal with fruits",
                                            "lunch": "Grilled chicken salad",
                                            
                                        }
                                }, 

                            """
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }

            response = requests.post(api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the AI response
            ai_response = response.json()
            diet_plan = ai_response.get('choices')[0]['message']['content']

            return {
                "success": True,
                "diet_plan": diet_plan
            }
        if provider == 'mistral': 
            print('using mistral')
            api_key = config('MISTRALAI_API_KEY')
            
            model = "mistral-large-latest"
            client = Mistral(api_key=api_key)
            messages = [
                {
                    "role": "system",
                    "content": """
                        You are a helpful assistant that generates personalized diet plans using the provided patient details.
                        Rules: 
                            - provide a daily diet plan with breakfast, lunch, snaks, and dinner
                            - meals must be from everdyday life food
                            - the week starts from saturday 
                            - just send the diet plan without any other text
                            - return the diet plan as a json format
                            - days must be 3 chars long
                            - example response:
                                {
                                    "SAT": 
                                        {
                                            "breakfast": "Oatmeal with fruits",
                                            "lunch": "Grilled chicken salad",
                                               
                                        }
                                }
                            """
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

            chat_response = client.chat.complete(
                model = model,
                messages = messages,
                response_format = {
                    "type": "json_object",
                }
            )
            return {
                "success": True,
                "diet_plan": chat_response.choices[0].message.content
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with AI service: {str(e)}")
        return {
            "success": False,
            "error": _("Failed to generate AI diet. Please try again.")
        }
    

def createDietPlan(data, dietRequest):
    """
       Save the diet into the database
    """
    
    jsonDiet = json.loads(data['diet_plan'])
    diet_request = dietRequest
    diet_request.update_status = 'NONE'
    diet_request.save()
    # Calculate dates
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)
            
            # Create diet with start and end dates
    diet = dc_models.Diet.objects.create(
                diet_request=diet_request,
                start_date=start_date,
                end_date=end_date,
            )
    diet.save()
    # Dealing with week days 
    for item in jsonDiet:
        daily_plan = dc_models.DailyMealPlan.objects.create(diet=diet, day=item)
        for meal_type, meals in jsonDiet[item].items():
            dc_models.Meal.objects.create(daily_plan=daily_plan, meal_type=meal_type,description=meals)
            
