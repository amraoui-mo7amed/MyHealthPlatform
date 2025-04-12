# MyHealthPlatform

## Project Overview
MyHealthPlatform is a Django-based web application designed to manage and track health-related data. It provides users with a comprehensive platform to monitor their health metrics, schedule appointments, and access medical resources.

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (or any other database supported by Django)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/MyHealthPlatform.git
   cd MyHealthPlatform
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - Create a new PostgreSQL database.
   - Update the `DATABASES` setting in `settings.py` with your database credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

   ```
   MHP ( Project Name ) ----- Core # Base application that contain all the project settings    
                              (Database, Server, Context Proccesors, Templates, Applications ...)
                        ----- Dashboard => - allow the admin to control objects ( ```CRUD``` )
                                           - Accept or decline the the doctors 
                                           - view the doctor's diplomas 
                                           - view the global static ( users count, doctors count...  )
                                           - allow the doctor the view or create or delete the        
                                             patient's diet requests/ diet plan 
                                           - allow the patient to view his dit plan 
                                           - allow the patient to show the couching/ nutrition 
                                           - allow the admin to view the contact requests 
                                           - allow the patient to view his diet archive   
                                           - allow the doctor to view the patient's diet 
                        ----- frontend  => - shows the landing page of the (details about the      
                                             platfrom)
                        ----- Patient   => - Allow patient to create the diet request 
                        ----- Doctor    => - Create diet plan for patient 
                                           - View the diet request details 
                        ----- User Auth => - responsible of signup/log in/ logout/ reset password /   
                                             email confirmation 


   ```