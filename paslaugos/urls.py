from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('automobiliai/', automobiliai, name='automobiliai'),
    path('automobilio_modeliai/', automobilio_modeliai, name='automobilio_modeliai'),
    path('uzsakymas/', uzsakymas, name='uzsakymas'),
    path('paslauga/', paslauga, name='paslauga'),
    path('automobilio_duomenys/<int:automobilio_modelis_id>/', automobiliu_duomenys, name='automobiliu_duomenys')

]
