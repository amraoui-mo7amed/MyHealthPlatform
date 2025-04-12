from django.shortcuts import render
from django.http import JsonResponse
from frontend.models.contact import Contact

def contact_list_view(request):
    # Retrieve all contacts from the database
    contacts = Contact.objects.all()
    # Return the contacts as a JSON response
    return render(request, 'contacts/list.html', {'contacts': contacts})