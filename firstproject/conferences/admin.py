
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference  # On importe seulement Conference depuis conferences.models
from users.models import Reservation  # On importe Reservation depuis users.models
from users.models import *
from users.models import Participant
from django.db.models import Count
from django.utils import timezone  # Ajout de timezone pour les filtres de date

class ReservationInline(admin.StackedInline):
    model = Reservation
    extra = 1
    readonly_fields = ('reservation_date',)
    can_delete = True

class ParticipantFilter(admin.SimpleListFilter):
    title = "Participant filter"
    parameter_name = "participants"

    def lookups(self, request, model_admin):
        return (
            ('0', 'No Participants'),
            ('more', 'More Participants'),
        )

    def queryset(self, request,queryset):
        if self.value()=='0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value()=='more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset
    def queryset(self, request, queryset):
        if self.value() == '0':
            # Filtrer les objets sans réservations
            return queryset.filter(reservations__isnull=True)
        elif self.value() == 'more':
            # Filtrer les objets avec au moins une réservation
            return queryset.filter(reservations__isnull=False).distinct()

class ConferenceDateFilter(admin.SimpleListFilter):
    title = "Date Conf filter"
    parameter_name='conference_date'

    def lookups(self, request,model_admin):
        return (
            ('past','past conf'),
            ('today','today conf'),
            ('upcomming','upcomming conf'),
        )
    def queryset(self, request,queryset):
        if self.value()=='past':
            return queryset.filter(end_date__lt=timezone.now().date())
        if self.value()=='today':
            return queryset.filter(start_date=timezone.now().date())
        if self.value()=='upcomming':
            return queryset.filter(start_date__gt=timezone.now().date())
        return queryset

class ConferenceAdmin(admin.ModelAdmin):
    list_display=('title','location','start_date', 'end_date','price')
    search_fields=('title',)
    list_per_page=2
    ordering=('start_date','title')
    fieldsets= (
        ('Description', {
            'fields':('title','description','category','location','price','capacity')
        }),
        ('Horraires',{
            'fields':('start_date','end_date','created_at','updated_at')
        }),
        ('Docuemnts', {
            'fields':('program',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReservationInline]
    autocomplete_fields = ('category',)
    list_filter = ('title', ParticipantFilter, ConferenceDateFilter)

admin.site.register(Conference, ConferenceAdmin)
