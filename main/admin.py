from django.contrib import admin

from main.models import HardSkill, Person, PlaceOfWork, Resume, SoftSkill


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    raw_id_fields = ('soft_skills', 'hard_skills')

@admin.register(HardSkill)
class HardSkillAdmin(admin.ModelAdmin):
    pass

@admin.register(PlaceOfWork)
class PlaceOfWorkAdmin(admin.ModelAdmin):
    pass

@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    pass
