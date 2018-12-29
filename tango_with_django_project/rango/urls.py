from django.urls import path
from rango import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('category/<slug:category_name_url>', views.category, name="category"),
]