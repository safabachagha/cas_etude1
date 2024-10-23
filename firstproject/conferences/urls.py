from django.urls import path
from .views import *

urlpatterns = [
    path ('list/',conferencelist,name="listeconf"),
    path('listViewConfernce/',ConferenceListView.as_view(),name="listeViewconf"),
    path
]

