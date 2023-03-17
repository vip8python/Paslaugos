from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # re_path(r'^hello/$', hello_world),
    path('automobiliai/', automobiliai, name='automobiliai'),
    path('automobilio_modeliai/', automobilio_modeliai, name='automobilio_modeliai'),
    path('uzsakymai/', UzsakymaiListView.as_view(), name='uzsakymas'),
    path('uzsakymai/<int:pk>', UzsakymasDetailView.as_view(), name='uzsakymas-detail'),
    path('paslauga/', paslauga, name='paslauga'),
    path('automobilio_duomenys/<int:automobilis_id>/', automobilio_duomenys, name='automobiliu_duomenys'),
    path('saskaitos/', SaskaitosListView.as_view(), name='saskaitos'),
    path('saskaitos/<int:pk>', SaskaitosDetailView.as_view(), name='saskaitos-detail'),
    path('search/', search, name='search'),
    path('logout/', CustomLogout.as_view(), name='logout'),
    path('manoauto/', AutoByUserListView.as_view(), name='manoauto'),
    path('register/', register, name='register'),
    path('profilis/', profilis, name='profilis'),
    ]
