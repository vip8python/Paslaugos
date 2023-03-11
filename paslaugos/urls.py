from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # path('', index_meniu, name='index'),
    path('automobiliai/', automobiliai, name='automobiliai'),
    path('automobilio_modeliai/', automobilio_modeliai, name='automobilio_modeliai'),
    path('uzsakymas/', uzsakymas, name='uzsakymas'),
    path('paslauga/', paslauga, name='paslauga'),
    path('automobilio_duomenys/<int:automobilis_id>/', automobilio_duomenys, name='automobiliu_duomenys'),
    path('saskaitos/', SaskaitosListView.as_view(), name='saskaitos'),
    path('saskaitos/<int:pk>', SaskaitosDetailView.as_view(), name='saskaitos-detail')

]
