from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import formats

from .forms import ApplicationForm
from .models import Vacancy


def active_vacancy_queryset():
    return Vacancy.objects.filter(is_active=True)


def home(request):
    return render(request, "vacancies/home.html", {"nav_active": "home"})


def vacancy_list(request):
    qs = active_vacancy_queryset()
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

    return render(
        request,
        "vacancies/vacancy_list.html",
        {
            "vacancies": qs,
            "filter_type": inst_type,
            "filter_q": q,
            "nav_active": "vacancies",
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


def apply(request):
    vacancies_qs = active_vacancy_queryset()
    initial_vacancy = None
    raw_vid = request.GET.get("vacancy")
    if raw_vid and raw_vid.isdigit():
        initial_vacancy = vacancies_qs.filter(pk=int(raw_vid)).first()

    if request.method == "POST":
        form = ApplicationForm(
            request.POST,
            request.FILES,
            vacancy_queryset=vacancies_qs,
        )
        if form.is_valid():
            form.save()
            return redirect(reverse("vacancies:application_success"))
    else:
        initial = {}
        if initial_vacancy:
            initial["vacancy"] = initial_vacancy.pk
        form = ApplicationForm(
            vacancy_queryset=vacancies_qs,
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
        },
    )


def application_success(request):
    return render(
        request,
        "vacancies/application_success.html",
        {"nav_active": "apply"},
    )
