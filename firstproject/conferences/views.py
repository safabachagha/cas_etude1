from django.shortcuts import render
from .models import Conference




def conferencelist(req):
    liste=Conference.objects.all().order_by('-start_date')
    print(liste)
    return render(req,'conferences/conferencelist.html',{'conferenceslist':liste})

class ConferenceListView(ListView):
    model=Conference
    template_name=conferences/confernece_list.html
    context_objetct_name='conferences'
    
    def def get_queryset(self):
        return 