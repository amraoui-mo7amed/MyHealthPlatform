from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from dashboard.decorators import role_or_admin_required
from patient.models import DietRequest
from doctor import models as dc_models
from datetime import datetime, timedelta
from django.http import JsonResponse
from decouple import config
import requests
from django.conf import settings

UserModel = get_user_model()

@login_required
def list(request):
    # Define the YouTube Data API endpoint and parameters
    YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')  # Ensure this is set in your settings.py
    YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
    search_query = "nutrition tips"  # Example search query
    max_results = 10  # Number of results to fetch

    # Make a request to the YouTube Data API
    try:
        response = requests.get(YOUTUBE_API_URL, params={
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY,
        })
        response.raise_for_status()  # Raise an exception for HTTP errors
        youtube_data = response.json()
        videos = youtube_data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube data: {e}")
        videos = []

    # Render the template with the YouTube videos
    print("Videos:", videos)
    return render(request, 'nutrition/home.html', {
        "videos": videos,
    })