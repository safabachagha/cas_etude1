from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from conferences.models import Conference


class Participant(AbstractUser):
    # Validateur pour le CIN (carte d'identité nationale)
    cin_validator = RegexValidator(
        regex='^\d{8}$',
        message="This field must contain exactly 8 digits"
    )
    def email_validator(value):
        if not value.endswith('@esprit.tn'):
            raise ValidationError('Email invalid, only @esprit.tn domain is allowed')
        
    cin = models.CharField(primary_key=True, max_length=8, validators=[cin_validator])
    email = models.EmailField(unique=True, max_length=255, validators=[email_validator])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'
    
    # Choix pour la catégorie de participant
    CHOICES = (
        ('etudiant', 'Etudiant'),
        ('chercheur', 'Chercheur'),
        ('docteur', 'Docteur'),
        ('enseignant', 'Enseignant'),
    )
    participant_category = models.CharField(max_length=255, choices=CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Utilisation d'une chaîne pour éviter les problèmes d'importation circulaire
    reservations = models.ManyToManyField(Conference, through='Reservation', related_name='reservations')
    
    class Meta:
        verbose_name_plural = "Participants"


class Reservation(models.Model):
    # Utilisez une chaîne pour éviter les dépendances circulaires
    conference = models.ForeignKey(Conference , on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError('you can only reserve for upcomming conference')
        reservation_count=Reservation.objects.filter(
            participant=self.participant,
            reservation_date__date=timezone.now().date()
        )
        print(reservation_count)
        if len(reservation_count) >= 2:
            raise ValidationError("You can only make up to 3 reservations per day")
        
    class Meta:
        unique_together = ('conference', 'participant')  # Empêche les réservations en double pour la même conférence
        verbose_name_plural="Reservations"