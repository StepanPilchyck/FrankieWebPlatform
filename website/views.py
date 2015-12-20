from django.shortcuts import render

from django.http import Http404

import weblayout.models as wlm
import website.models as wsm
import webshop.models as wshm

from webshopcart.views import get_products_in_cart
from weblayout.views import get_language


def page(request, page_url):
    # try:
        # System Elements:
        sys_elem = wlm.SystemElement.objects.all()
        sys_header = sys_elem.filter(name='Header').first()
        sys_footer = sys_elem.filter(name='Footer').first()
        sys_script = sys_elem.filter(name='Script').first()

        # Static Page:
        static_page_all = wsm.StaticPage.objects.all()
        static_page = static_page_all.filter(url=page_url).first()

        # SEO attributes:
        seo = {
            'title': static_page.title,
            'meta_description': static_page.meta_description,
            'meta_canonical': static_page.meta_canonical,
            'meta_robots': static_page.meta_robots,
            'h1': static_page.h1,
        }

        # Galleries:
        gallery = None
        if static_page.gallery:
            gallery = wsm.GalleryImagePosition.objects.order_by('weight').filter(gallery=wsm.Gallery.objects.filter(
                name=static_page.gallery.name).first()).all()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.order_by('weight').filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        # Product in cart
        session = None
        if request.session.has_key('cart'):
            session = request.session['cart']

        # Bread crumbs
        bread_crumbs = []
        if static_page.url != 'index':
            bread_crumbs = [
                {
                    'url': '/',
                    'name': static_page_all.filter(url='index').first().name
                },
                {
                    'url':'',
                    'name': static_page.name
                },
            ]

        return render(request, static_page.template.path, {
            'seo': seo,
            'static_page': static_page,
            'main_menu': {'menu': wlm.MainMenu.objects.all(), 'url': request.path},
            'additional_menu': {'menu': wlm.AdditionalMenu.objects.all(), 'url': request.path},
            'extra_menu': {'menu': wlm.ExtraMenu.objects.all(), 'url': request.path},
            'sys_header': sys_header,
            'sys_footer': sys_footer,
            'sys_script': sys_script,
            'banners': image_positions,
            'gallery': gallery,
            'bread_crumbs': bread_crumbs,
            'cart_preview': get_products_in_cart(request),
            'language_list': wlm.Language.objects.all(),
            'language_id': get_language(request).__str__()
        })
    # except:
    #     raise Http404('Page not found')


def index_page(request):
    return page(request, 'index')
