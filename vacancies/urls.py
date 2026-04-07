from django.urls import path

from . import views

app_name = "vacancies"

urlpatterns = [
    path("", views.home, name="home"),
    path("vacancies/", views.vacancy_list, name="vacancy_list"),
    path("apply/", views.apply, name="apply"),
    path("apply/success/", views.application_success, name="application_success"),
]
