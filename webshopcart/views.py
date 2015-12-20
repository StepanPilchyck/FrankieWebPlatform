from django.shortcuts import render
import json
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse

import weblayout.models as wlm
import website.models as wsm
import webshopcart.models as wshcm
import webshop.models as wshm
import webform.forms as wff


class Product:
    def __init__(self, product_id, url, name, price, image, corrector_id=None):
        self.product_id = product_id
        self.corrector_id = corrector_id
        self.url = url
        self.name = name
        self.price = price
        self.image = image


class _Product:
    def __init__(self, product_id, count, price_corrector_id=None):
        self.product_id = product_id
        self.count = count
        self.price_corrector_id = price_corrector_id


class ProductOrder:
    def __init__(self, name, count, price):
        self.name = name
        self.count = count
        self.price = price
        self.sum = (float(count) * price)


def put_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None

        if 'cart' not in request.session:
            request.session['cart'] = []

        flag = True

        for i in range(0, request.session['cart'].__len__()):
            if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                request.session['cart'][i]['count'] += 1
                flag = False
                break
        if flag:
            request.session['cart'].append({'p': product_id, 'c': corrector_id, 'count': 1})

        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.get_new_price
            else:
                p = product_m.get_default_price
            t_price += p * prod['count']

        return get_products(request)
    return HttpResponse("{}", content_type="application/json")


def del_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None

        if 'cart' in request.session:
            for i in range(0, request.session['cart'].__len__()):
                if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                    if request.session['cart'][i]['count'] > 1:
                        request.session['cart'][i]['count'] -= 1
                    break
        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.get_new_price
            else:
                p = product_m.get_default_price
            t_price += p * prod['count']

        return get_products(request)
    return HttpResponse("{}", content_type="application/json")


def rem_product(request):
    if request.POST:
        product_post = request.POST
        product_id = int(product_post['p'])
        if product_post['c'].strip().__len__() > 0:
            corrector_id = int(product_post['c'])
        else:
            corrector_id = None

        if 'cart' in request.session:
            for i in range(0, request.session['cart'].__len__()):
                if request.session['cart'][i]['p'] == product_id and request.session['cart'][i]['c'] == corrector_id:
                    request.session['cart'].__delitem__(i)
                    break

        t_count = 0
        t_price = 0
        for prod in request.session['cart']:
            t_count += prod['count']
            product_m = wshm.Product.objects.filter(id=prod['p']).first()
            price_c = wshm.ProductPriceCorrector.objects.filter(product=product_m, id=prod['c']).first()
            if price_c:
                p = price_c.get_new_price
            else:
                p = product_m.get_default_price
            t_price += p * prod['count']

        return get_products(request)
    return HttpResponse("{}", content_type="application/json")


def product_sorted(products):
    keys = sorted(products)
    print(keys)
    new_products = {}
    for key in keys:
        new_products[key] = products[key]
    return new_products


def get_products(request):
    if request.POST:
        products = {}
        items = {}
        t_price = 0
        t_count = 0
        if 'cart' in request.session:
            for prod in request.session['cart']:
                product = wshm.Product.objects.filter(id=prod['p']).first()
                img_url = wshm.ProductImagePosition.objects.filter(product=product).order_by('weight').first()
                if img_url:
                    img_url = img_url.small_image()
                price_corrector = wshm.ProductPriceCorrector.objects.filter(id=prod['c']).first()
                if price_corrector:
                    price = price_corrector.get_new_price
                else:
                    price = product.get_default_price
                t_count += prod['count']
                t_price += prod['count'] * price
                if price_corrector:
                    items[product.id.__str__() + '_' + price_corrector.id.__str__()] = {'p': product.id,
                                                                                        'c': price_corrector.id,
                                                                                        'img_url': img_url,
                                                                                        'p_name': product.name,
                                                                                        'p_url': product.url,
                                                                                        'p_count': prod['count'],
                                                                                        'price': price}
                else:
                    items[product.id.__str__()] = {'p': product.id,
                                                   'c': None,
                                                   'img_url': img_url,
                                                   'p_name': product.name,
                                                   'p_url': product.url,
                                                   'p_count': prod['count'],
                                                   'price': price}

            products = product_sorted(items)

            products['t_price'] = t_price
            products['t_count'] = t_count

        serialized = json.dumps(products)
        return HttpResponse(serialized, content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def clear_cart(request):
    if request.POST:
        if 'cart' in request.session:
            request.session.__delitem__('cart')
    return HttpResponse("{}", content_type="application/json")


def get_products_in_cart(request):
    products = {}
    items = {}
    t_price = 0
    t_count = 0
    if 'cart' in request.session:
        for prod in request.session['cart']:
            product = wshm.Product.objects.filter(id=prod['p']).first()
            img_url = wshm.ProductImagePosition.objects.filter(product=product).order_by('weight').first()
            if img_url:
                img_url = img_url.small_image()
            price_corrector = wshm.ProductPriceCorrector.objects.filter(id=prod['c']).first()
            if price_corrector:
                price = price_corrector.get_new_price
            else:
                price = product.get_default_price
            t_count += prod['count']
            t_price += prod['count'] * price
            if price_corrector:
                items[product.id.__str__() + '_' + price_corrector.id.__str__()] = {
                    'p': product.id,
                    'c': price_corrector.id,
                    'img_url': img_url,
                    'p_name': product.name,
                    'p_url': product.url,
                    'p_count': prod['count'],
                    'p_price': prod['count'] * price,
                    'price': price
                }
            else:
                items[product.id.__str__()] = {
                    'p': product.id,
                    'c': '',
                    'img_url': img_url,
                    'p_name': product.name,
                    'p_url': product.url,
                    'p_count': prod['count'],
                    'p_price': prod['count'] * price,
                    'price': price
                }

        products['product'] = product_sorted(items)

        products['t_price'] = t_price
        products['t_count'] = t_count

    return products


def _cart_page(request):
    # try:
        if request.POST:
            products = []
            products_post = request.POST.getlist('product_positions')
            for product in products_post:
                product_tmp = product.split(';')
                if product_tmp.__len__() == 3:
                    products.append(Product(product_tmp[0], product_tmp[1], product_tmp[2]))
                elif product_tmp.__len__() == 2:
                    products.append(Product(product_tmp[0], product_tmp[1]))
                else:
                    pass
            cart_order = wshcm.ProductCart()
            cart_order.username = request.POST['user_name']
            cart_order.email = request.POST['user_email']
            cart_order.fixed_sum = float(request.POST['total_price'])
            cart_order.phone = request.POST['user_phone']
            cart_order.save()
            for product in products:
                product_tmp = wshcm.ProductInCart()
                product_tmp.product_id = product.product_id
                product_tmp.cart = cart_order
                product_tmp.count = product.count
                if product.price_corrector_id:
                    product_tmp.price_correction = wshm.ProductPriceCorrector.objects.filter(
                        id=product.price_corrector_id).first()
                product_tmp.save()
            clear_cart(request)

            # Send mail reports:
            products_order = []
            for p in products:
                tmp = wshm.Product.objects.filter(id=p.product_id).first()
                if p.price_corrector_id:
                    price = wshm.ProductPriceCorrector.objects.filter(
                        id=p.price_corrector_id).first()
                    products_order.append(ProductOrder(tmp.name, p.count, price.get_new_price))
                else:
                    products_order.append(ProductOrder(tmp.name, p.count, tmp.get_default_price))
            wff.OrderSendAdmin(request, products_order)
            wff.OrderSendUser(request, products_order)
            return HttpResponseRedirect('/thanks_order')

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        # Total sum price:
        total_price = 0
        cp = get_products_in_cart(request)
        if cp:
            total_price = cp['t_price']

        print(cp)

        return render(request, 'cart.html', {
            'main_menu': {'menu': wlm.MainMenu.objects.all(), 'url': request.path},
            'additional_menu': {'menu': wlm.AdditionalMenu.objects.all(), 'url': request.path},
            'extra_menu': {'menu': wlm.ExtraMenu.objects.all(), 'url': request.path},
            'banners': image_positions,
            'products_in_cart': cp,
            'total_price': total_price,
            'language_list': wlm.Language.objects.all(),
            'language_id': request.session['language']
        })
    # except:
    #     raise Http404('Page not found')


def cart_page_json(request, ids):

    if ids:
        ids_dict = ids.split('.')
        products_and_correctors = {}
        products_id = []
        correctors_id = []
        for item in ids_dict:
            item_correctors_id = []
            if item.find('_') > -1:
                product_id_dict = item.split('_')
                product_id = int(product_id_dict[0])
                correctors_id_dict = product_id_dict[1].split('+')
                for subitem in correctors_id_dict:
                    item_correctors_id.append(subitem)
                    correctors_id.append(subitem)
            else:
                product_id = int(item)
            products_id.append(product_id)
            products_and_correctors[product_id] = {
                'correctors_id': item_correctors_id
            }

        products_in_cart = wshm.Product.objects.filter(id__in=products_id)
        correctors_in_cart = wshm.ProductPriceCorrector.objects.filter(id__in=correctors_id)
        images_from_products = wshm.ProductImagePosition.objects.filter(product__in=products_in_cart)

        products = []
        for product_id in products_and_correctors:
            product = products_in_cart.filter(id=product_id).first()
            image = None
            if images_from_products.filter(product=product_id):
                image = images_from_products.filter(product=product_id).first().image_small
            if products_and_correctors[product_id]['correctors_id'].__len__() > 0:
                for corrector_id in products_and_correctors[product_id]['correctors_id']:
                    corrector = correctors_in_cart.filter(id=corrector_id, product=product_id).first()
                    products.append({
                        'product_id': product.id,
                        'corrector_id': corrector.id,
                        'corrector_name': corrector.name,
                        'url': product.url,
                        'name': product.name,
                        'price': corrector.get_new_price,
                        'image': image,
                    })
            else:
                products.append({
                    'product_id': product.id,
                    'corrector_id': '',
                    'corrector_name': '',
                    'url': product.url,
                    'name': product.name,
                    'price': product.get_default_price,
                    'image': image,
                })
        products_json = {'products': products}
    else:
        products_json = {'products': []}
    return JsonResponse(products_json, charset='utf-8')


def cart_page(request):
    # try:
        if request.POST:
            return HttpResponseRedirect('/thanks_order')

        return render(request, 'cart_async.html', {

        })
    # except:
    #     raise Http404('Page not found')