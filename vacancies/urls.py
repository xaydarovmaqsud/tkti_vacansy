from django.urls import path

from . import views

app_name = "vacancies"

urlpatterns = [
    path("", views.home, name="home"),
    path("vacancies/", views.vacancy_list, name="vacancy_list"),
    path("accounts/login/", views.VacancyLoginView.as_view(), name="login"),
    path("accounts/logout/", views.VacancyLogoutView.as_view(), name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/profile/", views.profile, name="profile"),
    path("apply/", views.apply, name="apply"),
    path("apply/success/", views.application_success, name="application_success"),
]
