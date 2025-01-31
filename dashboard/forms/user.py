from django import forms
from dashboard.models.user import PatientData
from django.core.validators import RegexValidator

class PatientDataForm(forms.ModelForm):
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='Phone number must be exactly 10 digits.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'pattern': '\d{10}',
            'title': 'Please enter exactly 10 digits'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'margin-bottom: 15px;'
            })
        # Specific field customizations
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter your phone number'
        })
        self.fields['have_diet'].widget.attrs.update({
            'class': 'form-check-input',
            'style': 'margin-left: 10px; margin-bottom: 15px;'
        })

    class Meta:
        model = PatientData
        fields = ['phone_number', 'gender', 'wilaya', 'have_diet']
        labels = {
            'phone_number': 'Phone Number',
            'gender': 'Gender',
            'wilaya': 'Wilaya',
            'have_diet': 'Do you have a diet?'
        }
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'wilaya': forms.Select(attrs={'class': 'form-select'}),
        } 