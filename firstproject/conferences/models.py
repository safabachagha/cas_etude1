from django.db import models
from django.core.validators import MaxValueValidator
from categories.models import Category  # Correction de l'import
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(validators=[MaxValueValidator(500)])
    program = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png', 'docx'], message='Only PDF, PNG, JPEG, or DOCX allowed')])

    created_at = models.DateTimeField(auto_now_add=True)  # Corrected typo
    updated_at = models.DateTimeField(auto_now=True)  # Corrected typo

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")  # Associating conference with a category

    class Meta:
        verbose_name_plural = "conferences"
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__gte=timezone.now().date()),
                name="start_date_must_be_greater_or_equal_than_today"
            )
        ]

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date')