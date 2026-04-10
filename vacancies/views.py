from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Count
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import formats

from .forms import ApplicationForm
from .models import Application, ApplicationStatus, Vacancy


def active_vacancy_queryset():
    return Vacancy.objects.filter(is_active=True)


def home(request):
    return render(request, "vacancies/home.html", {"nav_active": "home"})


def vacancy_list(request):
    qs = active_vacancy_queryset().annotate(
        applications_count=Count("applications")
    ).order_by("-created_at")
    inst_type = request.GET.get("type", "").strip()
    q = request.GET.get("q", "").strip()

    if inst_type in ("higher", "professional"):
        qs = qs.filter(institution_type=inst_type)
    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(institution__icontains=q)
            | Q(department__icontains=q)
        )

    applied_vacancy_ids = set()
    if request.user.is_authenticated:
        applied_vacancy_ids = set(
            Application.objects.filter(user=request.user).values_list("vacancy_id", flat=True)
        )

    return render(
        request,
        "vacancies/vacancy_list.html",
        {
            "vacancies": qs,
            "filter_type": inst_type,
            "filter_q": q,
            "nav_active": "vacancies",
            "applied_vacancy_ids": applied_vacancy_ids,
        },
    )


def vacancy_payload(v: Vacancy) -> dict:
    return {
        "id": v.pk,
        "title": v.title,
        "institution": v.institution,
        "type": v.institution_type,
        "department": v.department,
        "employment": v.employment,
        "location": v.location,
        "deadline": v.deadline.isoformat(),
        "deadline_display": formats.date_format(v.deadline, "DATE_FORMAT"),
        "description": v.description,
    }


@login_required
def apply(request):
    applied_ids = list(
        Application.objects.filter(user=request.user).values_list("vacancy_id", flat=True)
    )
    vacancies_qs = active_vacancy_queryset().exclude(pk__in=applied_ids)

    initial_vacancy = None
    raw_vid = request.GET.get("vacancy")
    if raw_vid and raw_vid.isdigit():
        cand = active_vacancy_queryset().filter(pk=int(raw_vid)).first()
        if cand and cand.pk not in applied_ids:
            initial_vacancy = cand
        elif cand and cand.pk in applied_ids:
            messages.warning(
                request,
                "Siz ushbu ish o‘rniga allaqachon ariza yuborgansiz. Pastda faqat hali ariza yubormagan "
                "ish o‘rinlari ro‘yxati ko‘rsatiladi.",
            )

    if request.method == "POST":
        form = ApplicationForm(
            request.POST,
            request.FILES,
            vacancy_queryset=vacancies_qs,
            applicant_user=request.user,
        )
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.status = ApplicationStatus.SUBMITTED
            application.save()
            return redirect(reverse("vacancies:application_success"))
    else:
        initial = {}
        if initial_vacancy:
            initial["vacancy"] = initial_vacancy.pk
        form = ApplicationForm(
            vacancy_queryset=vacancies_qs,
            applicant_user=request.user,
            initial=initial,
        )

    vacancies_for_js = [vacancy_payload(v) for v in vacancies_qs]
    return render(
        request,
        "vacancies/apply.html",
        {
            "form": form,
            "vacancies_for_js": vacancies_for_js,
            "nav_active": "apply",
            "no_open_vacancies": not vacancies_qs.exists(),
        },
    )


@login_required
def application_success(request):
    return render(
        request,
        "vacancies/application_success.html",
        {"nav_active": "apply"},
    )


@login_required
def profile(request):
    applications = (
        Application.objects.filter(user=request.user)
        .select_related("vacancy")
        .order_by("-submitted_at")
    )
    return render(
        request,
        "vacancies/profile.html",
        {
            "applications": applications,
            "nav_active": "profile",
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("vacancies:home"))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Hisobingiz yaratildi. Endi ariza topshirishingiz mumkin.")
            return redirect(reverse("vacancies:home"))
    else:
        form = UserCreationForm()
    return render(
        request,
        "registration/register.html",
        {"form": form, "nav_active": "register"},
    )


class VacancyLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_active"] = "login"
        return ctx


class VacancyLogoutView(LogoutView):
    next_page = reverse_lazy("vacancies:home")
