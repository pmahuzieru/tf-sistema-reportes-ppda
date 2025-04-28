from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import json
from pathlib import Path

from accounts.models import CustomUser
from management.models import (
    Body, EnvironmentalPlan, Measure,
    MeasureReport, ReportFile, BodyMeasure
)
from reporting.models import ProgressReport, ProgressReportData

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"

class Command(BaseCommand):
    help = 'Populate the database with realistic test data for the PPDA reporting system'

    def handle(self, *args, **kwargs):
        print("\n Starting to populate the database with realistic test data...")

        first_user = CustomUser.objects.first()
        if not first_user:
            print(" No users found in database. Please create at least one user.")
            return

        # 1. Bodies (ensure they exist before assigning users)
        bodies_by_name = {}
        bodies_path = FIXTURE_DIR / "bodies.json"
        if bodies_path.exists():
            with open(bodies_path, "r", encoding="utf-8") as f:
                bodies = json.load(f)
                for b in bodies:
                    body, _ = Body.objects.get_or_create(name=b["name"], defaults={"created_by": first_user})
                    bodies_by_name[body.name] = body

        # 2. Users from JSON
        users_path = FIXTURE_DIR / "users.json"
        if not users_path.exists():
            print(f" File {users_path} not found.")
            return

        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)

        for u in users:
            body = bodies_by_name.get(u.get("body")) if u.get("body") else None
            CustomUser.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email": u["email"],
                    "is_superuser": u.get("is_superuser", False),
                    "is_staff": u.get("is_staff", False),
                    "body": body,
                    "password": "pbkdf2_sha256$260000$demo$demo"
                }
            )

        # 3. Environmental plans from JSON
        plans_path = FIXTURE_DIR / "environmentalplans.json"
        if plans_path.exists():
            with open(plans_path, "r", encoding="utf-8") as f:
                plans = json.load(f)
                for p in plans:
                    plan, created = EnvironmentalPlan.objects.get_or_create(
                        short_name=p["short_name"],
                        defaults={
                            "name": p["name"],
                            "type": p["type"],
                            "created_by": first_user
                        }
                    )
                    if not created and not plan.created_by:
                        plan.created_by = first_user
                        plan.save()

        # 4. Measures from JSON (match by reference_plan_short_name)
        plans_by_shortname = {
            p.short_name: p for p in EnvironmentalPlan.objects.all()
        }
        medidas_path = FIXTURE_DIR / "measures.json"
        if not medidas_path.exists():
            print(f" File {medidas_path} not found.")
            return

        with open(medidas_path, "r", encoding="utf-8") as f:
            medidas = json.load(f)

        for m in medidas:
            try:
                plan = plans_by_shortname.get(m["reference_plan_short_name"])
                if not plan:
                    print(f" No se encontró plan '{m['reference_plan_short_name']}' para medida '{m['short_name']}'")
                    continue

                Measure.objects.get_or_create(
                    short_name=m["short_name"],
                    reference_PDA=plan,
                    defaults={
                        "measure_type": m["measure_type"],
                        "indicator": m["indicator"],
                        "calculation_formula": m["calculation_formula"],
                        "reporting_frequency": m["reporting_frequency"],
                        "verification_methods": m["verification_methods"],
                        "created_by": first_user,
                        "is_regulatory": m["is_regulatory"],
                    }
                )
            except Exception as e:
                print(f" Error inserting measure {m['short_name']}: {e}")

        # 5. BodyMeasure from JSON
        bodymeasures_path = FIXTURE_DIR / "bodymeasures.json"
        if bodymeasures_path.exists():
            with open(bodymeasures_path, "r", encoding="utf-8") as f:
                bodymeasures = json.load(f)
                for bm in bodymeasures:
                    try:
                        measure = Measure.objects.get(
                            short_name=bm["measure_short_name"],
                            reference_PDA__short_name=bm["reference_plan_short_name"]
                        )
                        body = Body.objects.get(name=bm["body_name"])
                        BodyMeasure.objects.get_or_create(
                            fk_measure=measure,
                            fk_body=body,
                            defaults={"is_reporter": bm.get("is_reporter", True), "created_by": first_user}
                        )
                    except (Measure.DoesNotExist, Body.DoesNotExist, KeyError) as e:
                        print(f" Error: {e}")

        # 6. MeasureReports from JSON
        measurereports_path = FIXTURE_DIR / "measurereports.json"
        if measurereports_path.exists():
            with open(measurereports_path, "r", encoding="utf-8") as f:
                reports = json.load(f)
                for r in reports:
                    try:
                        measure = Measure.objects.get(
                            short_name=r["measure_short_name"],
                            reference_PDA__short_name=r["reference_plan_short_name"]
                        )
                        user = CustomUser.objects.get(username=r["created_by"])
                        MeasureReport.objects.get_or_create(
                            measure=measure,
                            created_by=user,
                            defaults={"reported_value": r["reported_value"]}
                        )
                    except (Measure.DoesNotExist, CustomUser.DoesNotExist) as e:
                        print(f" Error: {e}")

        # 7. ReportFiles from JSON
        reportfiles_path = FIXTURE_DIR / "reportfiles.json"
        if reportfiles_path.exists():
            with open(reportfiles_path, "r", encoding="utf-8") as f:
                files = json.load(f)
                for fdata in files:
                    try:
                        measure = Measure.objects.get(
                            short_name=fdata["measure_short_name"],
                            reference_PDA__short_name=fdata["reference_plan_short_name"]
                        )
                        report = MeasureReport.objects.filter(measure=measure).first()
                        if report:
                            ReportFile.objects.get_or_create(
                                report=report,
                                description=fdata["description"],
                                defaults={
                                    "file": ContentFile(b"Dummy content", name="dummy.txt"),
                                    "created_by": report.created_by
                                }
                            )
                    except (Measure.DoesNotExist, KeyError) as e:
                        print(f" Error: {e}")

        # 8. Progress Reports from JSON
        progress_path = FIXTURE_DIR / "progressreports.json"
        if progress_path.exists():
            with open(progress_path, "r", encoding="utf-8") as f:
                progress = json.load(f)
                for pr in progress:
                    try:
                        plan = EnvironmentalPlan.objects.get(short_name=pr["environmental_plan_short_name"])
                        user = CustomUser.objects.get(username=pr["created_by"])
                        ProgressReport.objects.get_or_create(
                            name=pr["name"],
                            environmental_plan=plan,
                            defaults={
                                "publication_date": pr["publication_date"],
                                "created_by": user
                            }
                        )
                    except (EnvironmentalPlan.DoesNotExist, CustomUser.DoesNotExist) as e:
                        print(f"❌ Error: {e}")

        # 9. ProgressReportData from JSON
        progress_data_path = FIXTURE_DIR / "progressdata.json"
        if progress_data_path.exists():
            with open(progress_data_path, "r", encoding="utf-8") as f:
                data_entries = json.load(f)
                for entry in data_entries:
                    try:
                        report = ProgressReport.objects.get(name=entry["progress_report_name"])
                        ProgressReportData.objects.update_or_create(
                            progress_report=report,
                            defaults={"data": entry["data"]}
                        )
                    except ProgressReport.DoesNotExist as e:
                        print(f" Error: {e}")

        print("\n All fixture data loaded successfully.")
