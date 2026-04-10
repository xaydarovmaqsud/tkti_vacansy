from django import forms
from django.core.exceptions import ValidationError

from .models import Application, EducationLevel, Vacancy

CV_MAX_MB = 5


class ApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label=(
            "Men o‘z shaxsiy ma’lumotlarimning ishga qabul qilish maqsadida tegishli "
            "ma’lumotlarni himoya qilish qonunlariga muvofiq qayta ishlanishiga roziman."
        ),
        widget=forms.CheckboxInput(attrs={"style": "margin-top: 0.35rem"}),
    )

    class Meta:
        model = Application
        fields = [
            "vacancy",
            "full_name",
            "email",
            "phone",
            "education",
            "experience",
            "cover_letter",
            "cv",
            "consent",
        ]
        widgets = {
            "vacancy": forms.Select(attrs={"id": "vacancy-select"}),
            "full_name": forms.TextInput(
                attrs={
                    "id": "fullName",
                    "autocomplete": "name",
                    "placeholder": "Rasmiy hujjatlardagi kabi",
                }
            ),
            "email": forms.EmailInput(attrs={"id": "email", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"id": "phone", "autocomplete": "tel"}),
            "education": forms.Select(attrs={"id": "education"}),
            "experience": forms.Textarea(
                attrs={
                    "id": "experience",
                    "rows": 5,
                    "placeholder": "O‘qituvchilik, ilmiy tadqiqot, sanoat amaliyoti, ma’muriy vazifalar…",
                }
            ),
            "cover_letter": forms.Textarea(
                attrs={
                    "id": "coverLetter",
                    "rows": 6,
                    "placeholder": "Nima uchun aynan ushbu muassasa va ish o‘rnini tanladingiz, shuningdek talabalar va hamkasblarga nimalarni taqdim eta olasiz.",
                }
            ),
            "cv": forms.ClearableFileInput(
                attrs={
                    "id": "cv",
                    "accept": ".pdf,.doc,.docx,application/pdf,application/msword,"
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        vacancy_queryset = kwargs.pop("vacancy_queryset", None)
        self.applicant_user = kwargs.pop("applicant_user", None)
        super().__init__(*args, **kwargs)
        if vacancy_queryset is not None:
            self.fields["vacancy"].queryset = vacancy_queryset
        self.fields["vacancy"].empty_label = "— Ish o‘rnini tanlang —"
        self.fields["education"].choices = [("", "— Tanlang —")] + list(EducationLevel.choices)
        self.fields["cv"].label = "CV (rezyume) fayl"
        self.fields["cv"].required = True

    def clean_vacancy(self):
        vacancy = self.cleaned_data.get("vacancy")
        if vacancy is None:
            return vacancy
        user = self.applicant_user
        if user and user.is_authenticated:
            if Application.objects.filter(user=user, vacancy=vacancy).exists():
                raise ValidationError(
                    "Siz ushbu ish o‘rniga allaqachon ariza yuborgansiz. Har bir ish o‘rniga faqat bir marta ariza berish mumkin."
                )
        return vacancy

    def clean_full_name(self):
        name = self.cleaned_data["full_name"].strip()
        if len(name) < 3:
            raise ValidationError("To‘liq ismingizni kiriting (kamida 3 ta belgi).")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].replace(" ", "")
        if len(phone) < 8:
            raise ValidationError("Iltimos, to‘g‘ri telefon raqamini kiriting.")
        return self.cleaned_data["phone"].strip()

    def clean_experience(self):
        text = self.cleaned_data["experience"].strip()
        if len(text) < 20:
            raise ValidationError("Tajribangizni qisqacha tasvirlab bering (kamida 20 ta belgi).")
        return text

    def clean_cover_letter(self):
        text = self.cleaned_data["cover_letter"].strip()
        if len(text) < 50:
            raise ValidationError("Sizning motivatsion xatingiz kamida 50 ta belgidan iborat bo‘lishi kerak.")
        return text

    def clean_cv(self):
        f = self.cleaned_data.get("cv")
        if not f:
            raise ValidationError("Iltimos, rezyumeni yuklang (PDF, DOC yoki DOCX formatida).")
        limit = CV_MAX_MB * 1024 * 1024
        if f.size > limit:
            raise ValidationError(f"Fayl hajmi maksimal {CV_MAX_MB} MB bo‘lishi kerak.")
        return f
