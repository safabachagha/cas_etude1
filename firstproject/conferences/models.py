from django.db import models
from django.core.validators import MaxValueValidator, FileExtensionValidator
from categories.models import Category  # Correction de l'import
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date  # Import nécessaire pour les dates

class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
   

    start_date = models.DateField(default=timezone.now)

    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=900,
                                                               message="capacity must be under 900")])
    program=models.FileField(upload_to='files/',validators=[
        FileExtensionValidator(allowed_extensions=['pdf','png','jpeg','jpg'],message="only pdf,png,jpg,jpeg are allowed")])
    created_at = models.DateTimeField(auto_now_add=True)  # Horodatage automatique à la création
    updated_at = models.DateTimeField(auto_now=True)  # Horodatage automatique à chaque mise à jour

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")  # Liaison avec la catégorie
    class Meta:
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date()
                ),
                name="the start date must be greater than today or equal"
            )
        ]

                              
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date')
    
    def __str__(self):
        return f"title conference = {self.title}"  # Correction de la méthode __str__
