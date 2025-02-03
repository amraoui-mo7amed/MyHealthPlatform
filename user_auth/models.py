from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Get the default User model
UserModel = get_user_model()

class UserProfile(models.Model):
    """
    UserProfile model extending the default User model with additional fields.
    Contains personal information, role-based fields, and status indicators.
    """
    
    # Role choices for different user types
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    ]
    
    # Algerian wilayas (provinces) for location selection
    ALGERIAN_WILAYAS = [
        ('01', 'Adrar'),
        ('02', 'Chlef'),
        ('03', 'Laghouat'),
        ('04', 'Oum El Bouaghi'),
        ('05', 'Batna'),
        ('06', 'Béjaïa'),
        ('07', 'Biskra'),
        ('08', 'Béchar'),
        ('09', 'Blida'),
        ('10', 'Bouira'),
        ('11', 'Tamanrasset'),
        ('12', 'Tébessa'),
        ('13', 'Tlemcen'),
        ('14', 'Tiaret'),
        ('15', 'Tizi Ouzou'),
        ('16', 'Algiers'),
        ('17', 'Djelfa'),
        ('18', 'Jijel'),
        ('19', 'Sétif'),
        ('20', 'Saïda'),
        ('21', 'Skikda'),
        ('22', 'Sidi Bel Abbès'),
        ('23', 'Annaba'),
        ('24', 'Guelma'),
        ('25', 'Constantine'),
        ('26', 'Médéa'),
        ('27', 'Mostaganem'),
        ('28', 'MSila'),
        ('29', 'Mascara'),
        ('30', 'Ouargla'),
        ('31', 'Oran'),
        ('32', 'El Bayadh'),
        ('33', 'Illizi'),
        ('34', 'Bordj Bou Arréridj'),
        ('35', 'Boumerdès'),
        ('36', 'El Tarf'),
        ('37', 'Tindouf'),
        ('38', 'Tissemsilt'),
        ('39', 'El Oued'),
        ('40', 'Khenchela'),
        ('41', 'Souk Ahras'),
        ('42', 'Tipaza'),
        ('43', 'Mila'),
        ('44', 'Aïn Defla'),
        ('45', 'Naâma'),
        ('46', 'Aïn Témouchent'),
        ('47', 'Ghardaïa'),
        ('48', 'Relizane'),
        ('49', 'Timimoun'),
        ('50', 'Bordj Badji Mokhtar'),
        ('51', 'Ouled Djellal'),
        ('52', 'Béni Abbès'),
        ('53', 'In Salah'),
        ('54', 'In Guezzam'),
        ('55', 'Touggourt'),
        ('56', 'Djanet'),
        ('57', 'El MGhair'),
        ('58', 'El Menia')
    ]

    # User Information
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(max_length=1200, upload_to='user/', verbose_name='User Image')
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='PATIENT', verbose_name='User Role')
    
    # Personal Details
    birthdate = models.DateField(verbose_name='Birthdate', default='1999-01-01')
    gender = models.CharField(
        max_length=10,
        verbose_name='Gender',
        choices=[('male', 'Male'), ('female', 'Female')],
        default='male'
    )
    phone_number = models.CharField(max_length=10, verbose_name='Phone Number', default='')
    wilaya = models.CharField(
        max_length=20,
        verbose_name='Wilaya',
        choices=ALGERIAN_WILAYAS,
        default='16'  # Default to Algiers
    )
    certificate_serial = models.CharField(max_length=20, verbose_name='Certificate Serial', default='', null=True, blank=True)
    speciality = models.CharField(max_length=20, verbose_name='Speciality', default='', null=True, blank=True)

    # Status Fields
    is_approved = models.BooleanField(default=True, verbose_name='Is Approved')
    email_confirmed = models.BooleanField(default=False, verbose_name='Email Confirmed')
    notifications_count = models.IntegerField(default=0, verbose_name='User Notifications')

    def __str__(self):
        """String representation of the UserProfile model"""
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        """
        Override save method to set is_approved to False for new Doctor profiles
        """
        if not self.pk and self.role == 'DOCTOR':
            self.is_approved = False
        super().save(*args, **kwargs)

class OTP(models.Model):
    """
    One-Time Password model for user authentication
    Stores OTP codes with expiration times for user verification
    """
    
    # User relationship and OTP details
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6,unique=True)  # OTP code
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    expires_at = models.DateTimeField()  # Expiration timestamp

    def __str__(self):
        """String representation of the OTP model"""
        return f'OTP for {self.user.username}'

    def is_valid(self):
        """
        Check if the OTP is still valid based on expiration time
        Returns:
            bool: True if OTP is valid, False if expired
        """
        return timezone.now() < self.expires_at
