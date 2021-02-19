from django.urls import path
from lanex import views

app_name = 'lanex'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('user/', views.userpage, name='user'),
    path('explore/', views.explore, name='explore'),
]
