from django.contrib import admin

from .models import Application, Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "institution",
        "institution_type",
        "deadline",
        "is_active",
    )
    list_filter = ("institution_type", "is_active")
    search_fields = ("title", "institution", "department")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "email",
        "vacancy",
        "status",
        "cv",
        "submitted_at",
    )
    list_filter = ("status", "submitted_at")
    search_fields = ("full_name", "email", "vacancy__title", "user__username")
    readonly_fields = ("submitted_at",)
    fieldsets = (
        (None, {"fields": ("user", "vacancy", "status", "full_name", "email", "phone", "education")}),
        ("Application", {"fields": ("experience", "cover_letter", "cv", "consent")}),
        ("Meta", {"fields": ("submitted_at",)}),
    )
