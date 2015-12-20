from django.contrib import admin
from website.models import *
from image_cropping import ImageCroppingMixin


class GalleryImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image_admin', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('gallery',)


class BannerImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image_admin', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('banner',)


class GalleryImagePositionAdminInline(admin.StackedInline):
    model = GalleryImagePosition
    exclude = ('cropping_large', 'cropping_small', 'cropping_medium', )
    extra = 0
    show_change_link = True


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_image_admin', 'second_image_admin', )
    inlines = (GalleryImagePositionAdminInline, )


class BannerImagePositionAdminInline(admin.StackedInline):
    model = BannerImagePosition
    extra = 0
    show_change_link = True


class BannerAdmin(admin.ModelAdmin):
    inlines = (BannerImagePositionAdminInline, )


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    class Media:
        js = (
            'system/js/admin-transliteration.js',
            'system/js/admin-webshop_staticpage.js',
        )

admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(GalleryImagePosition, GalleryImageAdmin)
admin.site.register(BannerImagePosition, BannerImageAdmin)
