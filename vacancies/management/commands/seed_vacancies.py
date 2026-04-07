from datetime import date

from django.core.management.base import BaseCommand

from vacancies.models import InstitutionType, Vacancy


SEED = [
    {
        "title": "Associate Professor of Computer Science",
        "institution": "Northern State Technical University",
        "institution_type": InstitutionType.HIGHER,
        "department": "Faculty of Information Technologies",
        "employment": "Full-time",
        "location": "Regional center",
        "deadline": date(2026, 5, 15),
        "description": (
            "Teaching undergraduate and graduate courses, supervising theses, and participating "
            "in research projects in software engineering and data science."
        ),
    },
    {
        "title": "Senior Lecturer in Economics",
        "institution": "Institute of Business and Law",
        "institution_type": InstitutionType.HIGHER,
        "department": "School of Economics",
        "employment": "Full-time",
        "location": "Capital city",
        "deadline": date(2026, 4, 30),
        "description": (
            "Deliver courses in macroeconomics and econometrics; curriculum development; engagement "
            "with industry partners for student placements."
        ),
    },
    {
        "title": "Workshop Instructor — Electrical Installations",
        "institution": "Polytechnic College No. 12",
        "institution_type": InstitutionType.PROFESSIONAL,
        "department": "Electrical Engineering Department",
        "employment": "Full-time",
        "location": "Industrial district",
        "deadline": date(2026, 4, 20),
        "description": (
            "Practical training for vocational students, maintenance of lab equipment, and "
            "participation in occupational safety programs."
        ),
    },
    {
        "title": "Deputy Director for Academic Affairs",
        "institution": "Regional Medical College",
        "institution_type": InstitutionType.PROFESSIONAL,
        "department": "Administration",
        "employment": "Full-time",
        "location": "Regional center",
        "deadline": date(2026, 5, 1),
        "description": (
            "Strategic planning of educational programs, accreditation preparation, and coordination "
            "of teaching staff development."
        ),
    },
    {
        "title": "Research Fellow — Materials Science",
        "institution": "National Research University",
        "institution_type": InstitutionType.HIGHER,
        "department": "Institute of Nanotechnology",
        "employment": "Contract (2 years)",
        "location": "Science campus",
        "deadline": date(2026, 6, 10),
        "description": (
            "Laboratory research, publication, grant writing, and optional co-supervision of PhD students."
        ),
    },
    {
        "title": "Master Trainer — Welding Technologies",
        "institution": 'Vocational Training Center "Prometheus"',
        "institution_type": InstitutionType.PROFESSIONAL,
        "department": "Metalworking",
        "employment": "Part-time",
        "location": "Suburbs",
        "deadline": date(2026, 4, 25),
        "description": (
            "Kattalar uchun qisqa muddatli va davomiy ta’lim kurslari; sertifikat imtihonlariga tayyorgarlik."
        ),
    },
]


class Command(BaseCommand):
    help = "Create sample vacancies (skips if rows already exist)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Create seed vacancies even if some already exist.",
        )

    def handle(self, *args, **options):
        if Vacancy.objects.exists() and not options["force"]:
            self.stdout.write(self.style.WARNING("Vacancies already exist; use --force to add duplicates."))
            return
        for row in SEED:
            Vacancy.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Created {len(SEED)} vacancies."))
