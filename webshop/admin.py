from django.contrib import admin
from webshop.models import *
from image_cropping import ImageCroppingMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductParametersInline(admin.TabularInline):
    model = ProductParameterValue


class ProductParameterAvailableValueInline(admin.TabularInline):
    model = ProductParameterAvailableValue
    exclude = ['category']
    show_change_link = True


class ProductRatingsInline(admin.StackedInline):
    model = ProductRating
    show_change_link = True
    extra = 0


class ProductParametersCategoryInline(admin.TabularInline):
    model = ProductParameter
    show_change_link = True


class ProductParameterResources(resources.ModelResource):
    class Meta:
        model = ProductParameter
        filter = ('id', 'name', 'sort_as', 'category', 'prefix', 'suffix', 'weight', )
        exclude = ('first_image', 'second_image', )
        export_order = ('id', 'category', 'name', 'weight', 'prefix', 'suffix', 'sort_as', )


class ProductParameterAdmin(ImportExportModelAdmin):
    inlines = (ProductParameterAvailableValueInline, )
    resource_class = ProductParameterResources


class ProductParameterAvailableValueResources(resources.ModelResource):
    class Meta:
        model = ProductParameterAvailableValue
        filter = ('id', 'product_parameter', 'value', 'weight', )
        exclude = ('first_image', 'second_image', )
        export_order = ('id', 'product_parameter', 'value', 'weight', )


class ProductParameterAvailableValueAdmin(ImportExportModelAdmin):
    resource_class = ProductParameterAvailableValueResources


class ProductInline(admin.TabularInline):
    model = Product
    show_change_link = True
    extra = 0

    exclude = ('first_text', 'second_text', 'h1', 'description', 'meta_robots', 'meta_canonical', 'meta_description',
               'sale', 'margin', 'special_proposition', 'title')


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'url', 'title', 'first_text', 'second_text', 'meta_description', 'meta_canonical',
                  'meta_robots', 'h1', 'description', 'template', 'title_generation_rule',
                  'meta_description_generation_rule', 'h1_generation_rule', )
        exclude = ('first_image', 'second_image', 'creation_date', 'last_edit_date', 'first_text', 'second_text', )
        export_order = ('id', 'template', 'name', 'url', 'title', 'description', 'h1',
                        'meta_description', 'meta_canonical', 'meta_robots',
                        'title_generation_rule', 'h1_generation_rule', 'meta_description_generation_rule', )


class CategoryAdmin(ImportExportModelAdmin):
    inlines = (ProductParametersCategoryInline, ProductInline)
    list_display = ('name', 'url')
    resource_class = CategoryResources
    class Media:
        js = (
            'system/js/admin-transliteration.js',
            'system/js/admin-webshop_category.js',
        )



class ProductImagePositionAdminInline(admin.TabularInline):
    model = ProductImagePosition
    exclude = ('cropping_large', 'cropping_small', 'cropping_medium', 'active', 'description', 'title')
    extra = 0
    show_change_link = True


class ProductPriceCorrectorInline(admin.TabularInline):
    model = ProductPriceCorrector
    extra = 0


class HasNewCommentsListFilter(admin.SimpleListFilter):
    title = 'Has new comments'
    parameter_name = 'comments_num'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('with_new', 'With new comments'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'with_new':
            products_ratings = ProductRating.objects.filter(state=False).all()
            products = []
            for rating in products_ratings:
                products.append(rating.product.id)
            return queryset.filter(id__in=products).all()


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'url', 'title', 'default_price', 'active', 'first_text', 'second_text',
                  'meta_description', 'meta_canonical', 'meta_robots', 'h1', 'description', 'template',
                  'special_proposition', 'creation_date', 'last_edit_date', 'provider', 'category', 'weight', 'mass',
                  'sale', 'margin', )
        exclude = ('creation_date', 'last_edit_date', 'first_text', 'second_text', )
        export_order = ('id', 'category', 'template', 'provider', 'name', 'code', 'url', 'title', 'default_price',
                        'active', 'weight', 'description', 'sale', 'margin',
                        'h1', 'meta_description', 'meta_canonical', 'meta_robots',
                        'mass', 'special_proposition', )


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'url', 'gen_title', 'gen_meta_description', 'gen_h1', 'get_delivery_price',
                    'get_avg_rating', 'get_new_comments')
    inlines = (ProductParametersInline, ProductImagePositionAdminInline, ProductPriceCorrectorInline,
               ProductRatingsInline)
    resource_class = ProductResources
    list_filter = ('category', HasNewCommentsListFilter)

    class Media:
        js = (
            'system/js/admin-transliteration.js',
            'system/js/admin-webshop_product.js',
        )


class PreFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'original_url')


class ProductImageResources(resources.ModelResource):
    class Meta:
        model = ProductImagePosition
        fields = ('id', 'image_original', 'cropping_large', 'cropping_medium', 'cropping_small', 'name', 'title',
                  'creation_date', 'last_edit_date', 'weight', 'active', 'description', 'product', )
        exclude = ('creation_date', 'last_edit_date', )
        export_order = ('id', 'product', 'name', 'image_original', 'cropping_large', 'cropping_medium',
                        'cropping_small', 'title', 'weight', 'active', 'description', )


class ProductImageAdmin(ImageCroppingMixin, ImportExportModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('product',)
    resource_class = ProductImageResources


class ProviderResources(resources.ModelResource):
    class Meta:
        model = Provider
        export_order = ('id', 'currency', 'name', 'coefficient', )


class ProviderAdmin(ImportExportModelAdmin):
    resource_class = ProviderResources


class CurrencyResources(resources.ModelResource):
    class Meta:
        model = Currency


class CurrencyAdmin(ImportExportModelAdmin):
    resource_class = CurrencyResources


class ProductParameterValueResources(resources.ModelResource):
    class Meta:
        model = ProductParameterValue
        fields = ('id', 'product', 'category', 'product_parameter', 'value', 'custom_value', )
        export_order = ('id', 'product', 'category', 'product_parameter', 'value', 'custom_value', )


class ProductParameterValueAdmin(ImportExportModelAdmin):
    resource_class = ProductParameterValueResources


admin.site.register(ProductImagePosition, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(ProductParameterValue, ProductParameterValueAdmin)
admin.site.register(ProductParameterAvailableValue, ProductParameterAvailableValueAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SpecialProposition)
admin.site.register(PreFilter, PreFilterAdmin)
admin.site.register(DeliveryRule)
admin.site.register(Margin)
admin.site.register(Sale)
