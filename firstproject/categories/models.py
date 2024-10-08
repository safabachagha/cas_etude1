from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.
class Category(models.Model):  # Nom de la classe en majuscule
    
    letters_only = RegexValidator(r'^[A-Za-z\s]+$', 'Only letters are allowed')

    title = models.CharField(max_length=255,validators=[letters_only])
    created_at = models.DateTimeField(auto_now_add=True)  # Correction "DateTimeField"
    updated_at = models.DateTimeField(auto_now=True)  # Correction "DateTimeF
    class Meta:
        verbose_name_plural="categories"
def validate_letters_only(value):
    if not re.match(r'^[A-Za-z\s]+$',value):
       raise ValidationError('the field should only contain contrain  letters' )