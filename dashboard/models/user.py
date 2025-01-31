from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class PatientData(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='patient_data')
    phone_number = models.CharField(max_length=10, verbose_name='Phone Number')
    gender = models.CharField(
        max_length=10,
        verbose_name='Gender',
        choices=[('male', 'Male'), ('female', 'Female')],
        default='male'
    )

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

    wilaya = models.CharField(
        max_length=20,
        verbose_name='Wilaya',
        choices=ALGERIAN_WILAYAS,
        default='16'  # Default to Algiers
    )

    have_diet = models.BooleanField(
        default=False,
        verbose_name='Do you have a diet?'
    )

    def __str__(self):
        return f'{self.user.username} Patient Data'