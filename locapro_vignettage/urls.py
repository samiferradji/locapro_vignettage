"""locapro_vignettage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from labeling import services
from labeling import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login),
    url(r'^login/', auth_views.login),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^home/', views.home),
    url(r'^labeling/', views.labeling),
    url(r'^list_des_produits/', services.list_of_produit),
    url(r'^list_des_tables/', services.list_of_tables),
    url(r'^list_of_labeling/', services.list_of_labeling),
    url(r'^list_des_lots/', services.list_of_lots),
    url(r'^saisie_en_cours/', services.list_of_labeling_details_tempo),
    url(r'^labeling_details/', services.list_of_labeling_details),
    url(r'^list_des_employes/', services.list_of_employee),
    url(r'^list_des_tables/', services.list_of_tables),
    url(r'^production/', views.production),
    url(r'^statistics/', views.statistiques),
    url(r'^statistics_view/', views.statistiques_view),
    url(r'^dashboard/', views.dashboard),
    url(r'^history/', views.history)

]
