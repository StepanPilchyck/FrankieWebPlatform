from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

# Website App Views
import website.views

# Web shop App Views
import webshop.views

# Web shop cart App Views
import webshopcart.views

# Web rating App Views
import webrating.views

# weblayout
import weblayout.views

urlpatterns = [
    url(r'^$', website.views.index_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^cart/$', webshopcart.views.cart_page),
    url(r'^comments', webrating.views.comments),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^catalogue/(\w+)/(\w+)/(\d+)/(\d+)', webshop.views.catalogue_category),
    url(r'^catalogue/(\w+)$', webshop.views.catalogue_category),
    url(r'^catalogue/(\w+)/(\w+)$', webshop.views.catalogue_prefilter),
    url(r'^catalogue/api/(\w+)', webshop.views.catalogue_category_filter_json),
    url(r'^catalogue/api/(\w+)/(\w+)/(\d+)/(\d+)', webshop.views.catalogue_category_filter_json),
    url(r'^cart/api/(.+)?', webshopcart.views.cart_page_json),
    # url(r'^catalogue/(\w+)', webshop.views.page, name='shop_page'),
    # url(r'^product/(\w+)', webshop.views.product_page, name='product_page'),
    url(r'^(\w+)$', website.views.page, name='page'),
    url(r'^api/add_product$', webshopcart.views.put_product),
    url(r'^api/del_product$', webshopcart.views.del_product),
    url(r'^api/clear_cart$', webshopcart.views.clear_cart),
    url(r'^api/rem_product$', webshopcart.views.rem_product),
    url(r'^api/get_products$', webshopcart.views.get_products),
    # url(r'^api/products_modal/(\w+)', webshop.views.products_modal, name='product_page'),
    url(r'^api/set_language/(\w+)', weblayout.views.set_language, name='language'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
