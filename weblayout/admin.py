from django.contrib import admin

# Models
from weblayout.models import *

# Import / Export
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# MPTT Tree View
from django_mptt_admin.admin import DjangoMpttAdmin


class MainMenuItemDataInline(admin.TabularInline):
    model = MainMenuItemData


class MainMenuAdmin(DjangoMpttAdmin):
    inlines = (MainMenuItemDataInline, )


class ExtraMenuItemDataInline(admin.TabularInline):
    model = ExtraMenuItemData


class ExtraMenuAdmin(DjangoMpttAdmin):
    inlines = (ExtraMenuItemDataInline, )


class AdditionalMenuItemDataInline(admin.TabularInline):
    model = AdditionalMenuItemData


class AdditionalMenuAdmin(DjangoMpttAdmin):
    inlines = (AdditionalMenuItemDataInline, )


class TemplateResources(resources.ModelResource):
    class Meta:
        model = Template
        fields = ('id', 'name', 'path', 'creation_date', 'last_edit_date', )
        exclude = ('creation_date', 'last_edit_date', )
        export_order = ('id', 'path', 'name', )


class TemplateAdmin(ImportExportModelAdmin):
    resource_class = TemplateResources


admin.site.register(Template, TemplateAdmin)
admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(AdditionalMenu, AdditionalMenuAdmin)
admin.site.register(ExtraMenu, ExtraMenuAdmin)
admin.site.register(SystemElement)
admin.site.register(Language)
