from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class InstitutionType(models.TextChoices):
    HIGHER = "higher", "Oliy ta'lim"
    PROFESSIONAL = "professional", "Kasbiy ta'lim"


class ApplicationStatus(models.TextChoices):
    SUBMITTED = "submitted", "Yuborilgan"
    UNDER_REVIEW = "under_review", "Ko‘rib chiqilmoqda"
    SHORTLISTED = "shortlisted", "Tanlov ro‘yxatida"
    REJECTED = "rejected", "Rad etilgan"
    ACCEPTED = "accepted", "Qabul qilingan"


class EducationLevel(models.TextChoices):
    VOCATIONAL = "vocational", "Kasb-hunar / texnik diplom"
    BACHELOR = "bachelor", "Bakalavr darajasi"
    MASTER = "master", "Magistr darajasi"
    PHD = "phd", "Doktorlik darajasi (PhD yoki unga teng)"


class Vacancy(models.Model):
    title = models.CharField("Ish nomi", max_length=255)
    institution = models.CharField("Muassasa", max_length=255, default="Toshkent kimyo-texnologiya instituti")
    institution_type = models.CharField(
        "Ta'lim turi",
        max_length=20,
        choices=InstitutionType.choices,
        db_index=True,
    )
    department = models.CharField("Bo‘lim",max_length=255)
    employment = models.CharField("Ish turi",max_length=120)
    location = models.CharField("Manzil",max_length=120)
    deadline = models.DateField("Ariza muddati")
    description = models.TextField("Tavsif")
    is_active = models.BooleanField("Faol",default=True, db_index=True)
    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "title"]
        verbose_name = "Vakansiyalar"
        verbose_name_plural = "Vakansiyalar"

    def __str__(self) -> str:
        return f"{self.title} — {self.institution}"


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vacancy_applications",
        null=True,
        blank=True,
        verbose_name="Foydalanuvchi",
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(
        "Holat",
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SUBMITTED,
        db_index=True,
    )
    full_name = models.CharField("To‘liq ism", max_length=255)
    email = models.EmailField()
    phone = models.CharField("Telefon raqam", max_length=40)
    education = models.CharField("Ta’lim darajasi", max_length=20, choices=EducationLevel.choices)
    experience = models.TextField("Ish tajribasi")
    cover_letter = models.TextField("Motivatsion xat")
    cv = models.FileField(
        upload_to="applications/cv/%Y/%m/",
        blank=True,
        null=True,
        help_text="PDF, DOC, or DOCX. Maximum size is enforced on the public application form.",
        validators=[
            FileExtensionValidator(allowed_extensions=("pdf", "doc", "docx")),
        ],
    )
    consent = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Arizalar"
        verbose_name_plural = "Arizalar"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vacancy"],
                condition=models.Q(user__isnull=False),
                name="uniq_application_user_per_vacancy",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} → {self.vacancy.title}"
