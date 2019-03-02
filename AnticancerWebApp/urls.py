
from django.contrib import admin
from django.urls import path
from acp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="en"),
    path('index/', views.index),
    path('searchMultiplePeptides/', views.searchMultiplePeptides, name="searchMultiplePeptides"),
    path('tr/searchMultiplePeptides/', views.searchMultiplePeptides, name="searchMultiplePeptides"),
    path('searchFile/', views.searchFile, name="searchFile"),
    path('contact/', views.contact, name="contact"),
    path('information/', views.information, name="information"),
    path('tr/', views.anasayfa, name="tr"),
    path('tr/anasayfa/', views.anasayfa, name="anasayfa"),
    path('tr/iletisim/', views.iletisim, name="iletisim"),
    path('tr/yardim/', views.yardim, name="yardim"),
    path('tr/dosyarama/', views.dosyaarama, name="dosyaarama"),
    path('tr/cokluarama/', views.cokluarama, name="cokluarama"),

]
