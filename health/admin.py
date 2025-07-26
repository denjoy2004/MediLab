# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
# from import_export import resources
# from .models import Doctor,Feedback, Profile, Questions, Symptoms, Disease
# # Register your models here.
# admin.site.register(Doctor)
# admin.site.register(Feedback)
# admin.site.register(Profile)
# admin.site.register(Questions)
# admin.site.register(Symptoms)
# admin.site.register(Disease)





from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Doctor, Feedback, Profile, Questions, Symptoms, Disease,Test,TestRequest

# Define resource classes for import/export
class DoctorResource(resources.ModelResource):
    class Meta:
        model = Doctor

class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class QuestionsResource(resources.ModelResource):
    class Meta:
        model = Questions

class SymptomsResource(resources.ModelResource):
    class Meta:
        model = Symptoms

class TestResource(resources.ModelResource):
    class Meta:
        model = Test

class TestRequestResource(resources.ModelResource):
    class Meta:
        model = TestRequest

class DiseaseResource(resources.ModelResource):
    class Meta:
        model = Disease

    def before_import_row(self, row, **kwargs):
        """Handle JSON fields properly during import"""
        import json
        row["ids_of_selected_symptoms"] = json.loads(row["ids_of_selected_symptoms"]) if row.get("ids_of_selected_symptoms") else []
        row["name_of_selected_symptoms"] = json.loads(row["name_of_selected_symptoms"]) if row.get("name_of_selected_symptoms") else []

# Register models with ImportExportModelAdmin
@admin.register(Doctor)
class DoctorAdmin(ImportExportModelAdmin):
    resource_class = DoctorResource

@admin.register(Feedback)
class FeedbackAdmin(ImportExportModelAdmin):
    resource_class = FeedbackResource

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource

@admin.register(Questions)
class QuestionsAdmin(ImportExportModelAdmin):
    resource_class = QuestionsResource

# @admin.register(Symptoms)
# class SymptomsAdmin(ImportExportModelAdmin):
#     resource_class = SymptomsResource

@admin.register(Disease)
class DiseaseAdmin(ImportExportModelAdmin):
    resource_class = DiseaseResource

@admin.register(Test)
class DiseaseAdmin(ImportExportModelAdmin):
    resource_class = TestResource

@admin.register(TestRequest)
class DiseaseAdmin(ImportExportModelAdmin):
    resource_class = TestRequestResource
