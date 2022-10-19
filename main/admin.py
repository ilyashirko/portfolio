from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.utils.html import format_html

from main.models import (HardSkill, HigherEducation, Person, PlaceOfWork,
                         Resume, SoftSkill, Recomendation, Photo, Visitor, Project, ProjectImage, BiographyChapter)


class PersonImageInline(SortableStackedInline):
    model = Photo
    readonly_fields = ('preview', )
    fields = ['id', 'image', 'preview', ]
    extra = 0

    def preview(self, obj):
        return format_html(
            '<img src="{}" height=200 />',
            obj.image.url
        )

class ProjectImageInline(SortableStackedInline):
    model = ProjectImage
    readonly_fields = ('preview', )
    fields = ['id', 'image', 'preview', ]
    extra = 0

    def preview(self, obj):
        return format_html(
            '<img src="{}" height=200 />',
            obj.image.url
        )

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        PersonImageInline,
    ]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    raw_id_fields = ('soft_skills', 'hard_skills', 'places_of_work')


@admin.register(HardSkill)
class HardSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceOfWork)
class PlaceOfWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(HigherEducation)
class HigherEducationAdmin(admin.ModelAdmin):
    pass


@admin.register(Recomendation)
class RecomendationAdmin(admin.ModelAdmin):
    pass

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    pass

@admin.register(BiographyChapter)
class BiographyChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ProjectImageInline,
    ]
    raw_id_fields = ('develop_stack',)