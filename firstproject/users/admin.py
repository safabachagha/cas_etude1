from django.contrib import admin
from .models import Participant,Reservation


# Action pour marquer les réservations comme "confirmées"
def make_confirmed(modeladmin, request, queryset):
    queryset.update(confirmed=True)  # Mettre à jour toutes les réservations sélectionnées comme confirmées
    modeladmin.message_user(request, "Les réservations sélectionnées ont été confirmées.")

# Action pour marquer les réservations comme "non confirmées"
def make_unconfirmed(modeladmin, request, queryset):
    queryset.update(confirmed=False)  # Mettre à jour toutes les réservations sélectionnées comme non confirmées
    modeladmin.message_user(request, "Les réservations sélectionnées ont été marquées comme non confirmées.")

# Personnalisation de l'administration de Reservation
class ReservationAdmin(admin.ModelAdmin):
    # list_display : contrôle les champs affichés dans la liste des réservations
    list_display = ('conference', 'participant', 'reservation_date', 'confirmed')  # Affiche les champs souhaités

    # list_filter : permet de filtrer les réservations par date de réservation ou statut confirmé/non confirmé
    list_filter = ('confirmed', 'reservation_date')

    # search_fields : permet de rechercher les réservations par nom de la conférence ou nom d'utilisateur du participant
    search_fields = ('conference__title', 'participant__username')

    # Ajout des actions personnalisées dans la liste d'administration
    actions = [make_confirmed, make_unconfirmed]

    # Configuration des actions
    make_confirmed.short_description = "Confirmer les réservations sélectionnées"
    make_unconfirmed.short_description = "Annuler la confirmation des réservations sélectionnées"






class ParticipantAdmin(admin.ModelAdmin):
    # a. Personnalisez l'affichage dans la liste des participants
    list_display = ('cin', 'username', 'email', 'first_name', 'last_name', 'participant_category', 'created_at', 'updated_at')
    
    # b. Ajoutez des champs de recherche sur des attributs comme 'username', 'email'
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # c. Activez les filtres pour certaines colonnes
    list_filter = ('participant_category', 'created_at')
    
    # d. Pagination
    list_per_page = 10  # Limite de 10 participants par page
    
    # e. Champs non modifiables (lecture seule) pour 'created_at' et 'updated_at'
    readonly_fields = ('created_at', 'updated_at')
    
    # f. Organisation des champs dans des sections (fieldsets)
    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'cin', 'participant_category')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Participant, ParticipantAdmin)
