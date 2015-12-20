from django.shortcuts import render
from django.db import connection
from django.http import Http404
from frankie_web_platform import settings
from webshop.models import *
from django.test.client import RequestFactory
from django.http import JsonResponse


def get_selected_parameters_values(request) -> {int: [int]}:
    res = []
    for key, val in request.GET.items():
        if key == 'price_from' or key == 'price_to':
            pass
        else:
            res.append({'id': int(key), 'values': [int(v) for v in request.GET.getlist(key)]})
    return res


def get_selected_parameters(request) -> [int]:
    res = []
    for key, value in request.GET.items():
        if key == 'price_from' or key == 'price_to':
            pass
        else:
            res.append(int(key))
    return res


def get_selected_values(request) -> [int]:
    res = []
    for key, value in request.GET.items():
        if key == 'price_from' or key == 'price_to':
            pass
        else:
            res.append(int(value))
    return res


def get_price(request) -> (float, float):
    price_from = None
    price_to = None
    for key, value in request.GET.items():
        if key == 'price_from':
            price_from = float(value)
        elif key == 'price_to':
            price_to = float(value)
        else:
            pass
    return price_from, price_to


def list_to_sql_array(value: list) -> str:
    res = "("
    for i in range(value.__len__() - 1):
        res += value[i].__str__() + ', '
    res += value[value.__len__() - 1].__str__() + ")"
    return res


def check_if_param_in_params(param: int, params: [{}]) -> bool:
    for i in params:
        if param == i['id']:
            return True
    return False


def check_if_value_in_values(value: int, param: int, params: [{}]) -> bool:
    for i in params:
        if i['id'] == param and value in i['values']:
            return True
    return False


def get_filter_from_query(selected, parameters):
    filter_structure = {}
    for parameter in parameters:
        filter_structure[parameter[1]] = {'first_image': parameter[2],
                                          'second_image': parameter[3],
                                          'weight': parameter[4],
                                          'id': parameter[0],
                                          }
        filter_structure[parameter[1]]['values'] = []
        for param in parameters:
            if param[1] == parameter[1]:
                if check_if_param_in_params(param[0], selected):
                    if check_if_value_in_values(param[5], param[0], selected):
                        filter_structure[parameter[1]]['values'].append({'value': param[6],
                                                                         'first_image': param[7],
                                                                         'second_image': param[8],
                                                                         'weight': param[9],
                                                                         'id': param[5],
                                                                         'count': param[10],
                                                                         'checked': True})
                    else:
                        filter_structure[parameter[1]]['values'].append({'value': param[6],
                                                                         'first_image': param[7],
                                                                         'second_image': param[8],
                                                                         'weight': param[9],
                                                                         'id': param[5],
                                                                         'count': param[10],
                                                                         'checked': False})
                else:
                    filter_structure[parameter[1]]['values'].append({'value': param[6],
                                                                     'first_image': param[7],
                                                                     'second_image': param[8],
                                                                     'weight': param[9],
                                                                     'id': param[5],
                                                                     'count': param[10],
                                                                     'checked': False})

    filter_structure = sorted(filter_structure.items(), key=lambda x: x[1]['weight'])
    return filter_structure


def get_correctors_for_product(all_correctors, product_id):
    res = []
    for i in all_correctors:

        if i[1] == product_id:
            res.append(i)
    return res


def get_products(filtered_products, order: str):
    conn = connection
    cur = conn.cursor()
    all_correctors = cur.execute("SELECT "
                            "ppc.id, "
                            "ppc.product_id, "
                            "(ppc.new_price * prov.coefficient) as new_price, "
                            "ppc.name FROM product_price_correctors "
                            "AS ppc "
                            "JOIN products AS prod ON ppc.product_id = prod.id "
                            "JOIN providers AS prov ON prod.provider_id = prov.id").fetchall()
    products = {}
    products_ids = []
    img_ids = []
    for product in filtered_products:

        default_price = product[5]
        default_price_new = product[5]
        if product[21] is not None:
            default_price_new = default_price - default_price / 100 * product[21]
        if product[24] is not None:
            default_price_new += default_price / 100 * product[24]
        correctors = []
        images = []
        if product[0] in products:
            correctors = products[product[0]]['price_correctors']
            images = products[product[0]]['images']
        products[product[0]] = {'name': product[1],
                                'code': product[2],
                                'url': product[3],
                                'weight': product[4],
                                'default_new_price': default_price_new,
                                'default_price': default_price,
                                'description': product[7],
                                'mass': product[8],
                                'is_new': product[9],
                                'is_top': product[10],
                                'images': images,
                                'price_correctors': correctors,
                                'sale_name': product[22],
                                'sale_image': product[23],
                                'date_on_add': product[28]}

        if product[0] not in products_ids:
            products_ids.append(product[0])
            for corrector in get_correctors_for_product(all_correctors, product[0]):
                    price = corrector[2]
                    price_new = corrector[2]
                    if price is None:
                        price = product[5]
                        price_new = product[5]
                    if product[21] is not None:
                        price_new = price - price / 100 * product[21]
                    if product[24] is not None:
                        price_new += price / 100 * product[24]

                    products[product[0]]['price_correctors'].append({
                        'id': corrector[0],
                        'name': corrector[3],
                        'price_new': price_new,
                        'price': price})

        for prod in filtered_products:
            if prod[0] == product[0]:
                if prod[14] not in img_ids and prod[14] is not None:
                    img_ids.append(prod[14])
                    products[prod[0]]['images'].append({
                        'id': prod[14],
                        'weight': prod[15],
                        'original': prod[16],
                        'large': prod[17],
                        'medium': prod[18],
                        'small': prod[19]})
                    break

    if order == "price_ASC":
        products = sorted(products.items(), key=lambda x: x[1]['default_price'], reverse=False)
    elif order == "price_DESC":
        products = sorted(products.items(), key=lambda x: x[1]['default_price'], reverse=True)
    elif order == "date_ASC":
        products = sorted(products.items(), key=lambda x: x[1]['date_on_add'], reverse=False)
    elif order == "date_DESC":
        products = sorted(products.items(), key=lambda x: x[1]['date_on_add'], reverse=True)
    elif order == "weight":
        products = sorted(products.items(), key=lambda x: x[1]['weight'], reverse=False)
    else:
        raise Http404('Page not found')
    return products, products_ids


# noinspection SqlResolve
def filter_products(category, values, order: str, product_on_page: str, page: str,
                    price_from: float = None, price_to: float = None):
    conn = connection
    cur = conn.cursor()
    order_str = "prod.weight"
    if order == "price_ASC":
        order_str = "default_price ASC"
    if order == "price_DESC":
        order_str = "default_price DESC"
    if values.__len__() == 1:
        query = str.format(
            "SELECT "
            "prod.id AS prod_id, "  # 0
            "prod.name AS product_name, "  # 1
            "prod.code, "  # 2
            "prod.url, "  # 3
            "prod.weight, "  # 4
            "(prod.default_price * prod_providers.coefficient) AS default_price, "  # 5
            "prod.active, "  # 6
            "prod.description, "  # 7
            "prod.mass, "  # 8
            "prod.is_new, "  # 9
            "prod.is_top, "  # 10
            "prod_price_cor.id AS price_cor_id, "  # 11
            "prod_price_cor.name AS price_cor_name, "  # 12
            "(prod_price_cor.new_price * prod_providers.coefficient) AS new_price, "  # 13
            "prod_image.id AS image_id, "  # 14
            "prod_image.weight AS prod_image_weight, "  # 15
            "prod_image.image_original, "  # 16
            "prod_image.image_large, "  # 17
            "prod_image.image_medium, "  # 18
            "prod_image.image_small, "  # 19
            "prod.category_id, "  # 20
            "prod_sales.percent, "  # 21
            "prod_sales.name, "  # 22
            "prod_sales.image, "  # 23
            "prod_margins.percent, "  # 24
            "prod.provider_id AS provider_id, "  # 25
            "prod_sales.id AS sale_id, "  # 26
            "prod_margins.id AS margin_id, "  # 27
            "prod.date_on_add "  # 28
            "FROM products AS prod "
            "JOIN categories AS cat  ON cat.id = prod.category_id AND cat.name = '{0}' "
            "JOIN product_parameters_values AS prod_val ON prod_val.product_id = prod.id "
            "AND prod_val.value_id IN {1} "
            "JOIN providers AS prod_providers ON prod.provider_id = prod_providers.id "
            "LEFT JOIN sales AS prod_sales ON prod.sale_id = prod_sales.id "
            "LEFT JOIN margins AS prod_margins ON prod.margin_id = prod_margins.id "
            "LEFT JOIN product_price_correctors AS prod_price_cor ON prod.id = prod_price_cor.product_id "
            "LEFT JOIN product_image_positions AS prod_image ON prod.id = prod_image.product_id "
            "WHERE prod.active AND default_price BETWEEN {3} AND {4} ORDER BY {2}, prod_image.weight",
            category, list_to_sql_array(values[0]['values']), order_str, price_from, price_to)
    else:
        query = str.format(
            "SELECT "
            "prod.id AS prod_id, "  # 0
            "prod.name AS product_name, "  # 1
            "prod.code, "  # 2
            "prod.url, "  # 3
            "prod.weight, "  # 4
            "(prod.default_price * prod_providers.coefficient) AS default_price, "  # 5
            "prod.active, "  # 6
            "prod.description, "  # 7
            "prod.mass, "  # 8
            "prod.is_new, "  # 9
            "prod.is_top, "  # 10
            "prod_price_cor.id  AS price_cor_id, "  # 11
            "prod_price_cor.name AS price_cor_name, "  # 12
            "(prod_price_cor.new_price * prod_providers.coefficient) AS new_price, "  # 13
            "prod_image.id AS image_id, "  # 14
            "prod_image.weight AS prod_image_weight, "  # 15
            "prod_image.image_original, "  # 16
            "prod_image.image_large, "  # 17
            "prod_image.image_medium, "  # 18
            "prod_image.image_small, "  # 19
            "prod.category_id, "  # 20
            "prod_sales.percent, "  # 21
            "prod_sales.name, "  # 22
            "prod_sales.image, "  # 23
            "prod_margins.percent AS margin_percent, "  # 24
            "prod.provider_id AS provider_id, "  # 25
            "prod_sales.id AS sale_id, "  # 26
            "prod_margins.id AS margin_id, "  # 27
            "prod.date_on_add "  # 28
            "FROM products AS prod "
            "JOIN categories AS cat ON cat.id = prod.category_id AND cat.name = '{0}' "
            "JOIN product_parameters_values AS prod_val ON prod_val.product_id = prod.id "
            "AND prod_val.value_id IN {1} "
            "JOIN providers AS prod_providers ON prod.provider_id = prod_providers.id "
            "LEFT JOIN sales AS prod_sales ON prod.sale_id = prod_sales.id "
            "LEFT JOIN margins AS prod_margins ON prod.margin_id = prod_margins.id "
            "LEFT JOIN product_price_correctors AS prod_price_cor ON prod.id = prod_price_cor.product_id "
            "LEFT JOIN product_image_positions AS prod_image ON prod.id = prod_image.product_id "
            "WHERE prod.active ORDER BY {2} AND default_price BETWEEN {3} AND {4}, prod_image.weight",
            category, list_to_sql_array(values[0]['values']), order_str, price_from, price_to)
        for val_id in range(1, values.__len__()):
            query = str.format(
                "SELECT "
                "prod.prod_id AS prod_id, "  # 0
                "prod.product_name AS product_name, "  # 1
                "prod.code, "  # 2
                "prod.url, "  # 3
                "prod.weight, "  # 4
                "prod.default_price AS default_price, "  # 5
                "prod.active, "  # 6
                "prod.description, "  # 7
                "prod.mass, "  # 8
                "prod.is_new, "  # 9
                "prod.is_top, "  # 10
                "prod.price_cor_id  AS price_cor_id, "  # 11
                "prod.price_cor_name AS price_cor_name, "  # 12
                "prod.new_price AS new_price, "  # 13
                "prod_image.id AS image_id, "  # 14
                "prod.prod_image_weight AS prod_image_weight, "  # 15
                "prod_image.image_original, "  # 16
                "prod_image.image_large, "  # 17
                "prod_image.image_medium, "  # 18
                "prod_image.image_small, "  # 19
                "prod.category_id, "  # 20
                "prod_sales.percent, "  # 21
                "prod_sales.name, "  # 22
                "prod_sales.image, "  # 23
                "prod.margin_percent, "  # 24
                "prod.provider_id AS provider_id, "  # 25
                "prod.sale_id AS sale_id, "  # 26
                "prod.margin_id AS margin_id, "  # 27
                "prod.date_on_add "  # 28
                "FROM ({0}) AS prod "
                "JOIN categories AS cat  ON cat.id = prod.category_id AND cat.name = '{1}' "
                "JOIN product_parameters_values AS prod_val "
                "ON prod_val.product_id = prod.prod_id AND prod_val.value_id IN {2} "
                "JOIN providers AS prod_providers ON prod.provider_id = prod_providers.id "
                "LEFT JOIN sales AS prod_sales ON prod.sale_id = prod_sales.id "
                "LEFT JOIN margins AS prod_margins ON prod.margin_id = prod_margins.id "
                "LEFT JOIN product_price_correctors AS prod_price_cor ON prod.prod_id = prod_price_cor.product_id "
                "LEFT JOIN product_image_positions AS prod_image ON prod.prod_id = prod_image.product_id "
                "WHERE prod.active ORDER BY {3} AND default_price BETWEEN {4} AND {5}, prod_image.weight", query,
                category, list_to_sql_array(values[val_id]['values']), order_str, price_from, price_to)
    cur.execute(query)
    products_selected = cur.fetchall()
    products, products_ids = get_products(products_selected, order)
    max_page = round(products.__len__() / int(product_on_page))
    products = products[(int(page) - 1) * int(product_on_page): int(page) * int(product_on_page)]
    return products, products_ids, max_page


# noinspection SqlResolve
def catalogue_category_filter(request, category: str, order: str = "weight",
                              product_on_page: str = settings.PRODUCT_ON_PAGE,
                              page: str = 1) -> str:
    conn = connection
    cur = conn.cursor()
    price_min = cur.execute("SELECT MIN(prod.default_price) "
                                "FROM products as prod "
                                "JOIN categories AS cat "
                                "ON prod.category_id = cat.id AND cat.name = %s", [category]).fetchall()[0][0]
    price_max = cur.execute("SELECT MAX(prod.default_price) "
                            "FROM products as prod "
                            "JOIN categories AS cat "
                            "ON prod.category_id = cat.id AND cat.name = %s", [category]).fetchall()[0][0]
    if request.GET:
        values = get_selected_parameters_values(request)
        price_from, price_to = get_price(request)
        if price_from is None:
            price_from = price_min
        if price_to is None:
            price_to = price_max
        products, products_ids, max_page = filter_products(category, values, order, product_on_page, page,
                                                           price_from, price_to)

    else:
        cur.execute(
            str.format("SELECT "
                       "prod.id AS prod_id, "  # 0
                       "prod.name AS product_name, "  # 1
                       "prod.code, "  # 2
                       "prod.url, "  # 3
                       "prod.weight, "  # 4
                       "(prod.default_price * prod_providers.coefficient) AS default_price, "  # 5
                       "prod.active, "  # 6
                       "prod.description, "  # 7
                       "prod.mass, "  # 8
                       "prod.is_new, "  # 9
                       "prod.is_top, "  # 10
                       "prod_price_cor.id  AS price_cor_id, "  # 11
                       "prod_price_cor.name AS price_cor_name, "  # 12
                       "(prod_price_cor.new_price * prod_providers.coefficient) AS new_price, "  # 13
                       "prod_image.id AS image_id, "  # 14
                       "prod_image.weight AS prod_image_weight, "  # 15
                       "prod_image.image_original, "  # 16
                       "prod_image.image_large, "  # 17
                       "prod_image.image_medium, "  # 18
                       "prod_image.image_small, "  # 19
                       "prod.category_id, "  # 20
                       "prod_sales.percent, "  # 21
                       "prod_sales.name, "  # 22
                       "prod_sales.image, "  # 23
                       "prod_margins.percent, "  # 24
                       "prod.provider_id AS provider_id, "  # 25
                       "prod.sale_id AS sale_id, "  # 26
                       "prod.margin_id AS margin_id, "  # 27
                       "prod.date_on_add "  # 28
                       "FROM products AS prod "
                       "JOIN categories AS cat  ON cat.id = prod.category_id AND cat.name = '{0}' "
                       "JOIN providers AS prod_providers ON prod.provider_id = prod_providers.id "
                       "LEFT JOIN sales AS prod_sales ON prod.sale_id = prod_sales.id "
                       "LEFT JOIN margins AS prod_margins ON prod.margin_id = prod_margins.id "
                       "JOIN product_parameters_values AS prod_val ON prod_val.product_id = prod.id "
                       "LEFT JOIN product_price_correctors AS prod_price_cor ON prod.id = prod_price_cor.product_id "
                       "LEFT JOIN product_image_positions AS prod_image ON prod.id = prod_image.product_id "
                       "AND prod.active "
                       "ORDER BY prod.weight, prod_image.weight",
                       category))

        products_selected = cur.fetchall()
        products, products_ids = get_products(products_selected, order)

        max_page = round(products.__len__() / int(product_on_page))
        products = products[(int(page) - 1) * int(product_on_page): int(page) * int(product_on_page)]
    if products_ids.__len__() > 0:
        cur.execute(
            str.format("SELECT "
                       "prod_par.id, "  # 0
                       "prod_par.name, "  # 1
                       "prod_par.first_image, "  # 2
                       "prod_par.second_image, "  # 3
                       "prod_par.weight, "  # 4
                       "val.id AS val_id, "  # 5
                       "val.value, "  # 6
                       "val.first_image AS val_first_image, "  # 7
                       "val.second_image AS val_second_image, "  # 8
                       "val.weight AS val_weight, "  # 9
                       "(SELECT COUNT(id) FROM product_parameters_values "
                       "AS ppv WHERE val.id = ppv.value_id AND ppv.product_id IN {1}) AS count"  # 10
                       " FROM product_parameters AS prod_par JOIN product_parameters_available_value AS val ON "
                       "val.product_parameter_id = prod_par.id JOIN categories AS cat ON cat.id = prod_par.category_id "
                       "AND cat.name = '{0}' "
                       "LEFT JOIN product_parameters_values AS prod_param_val "
                       "ON val.id = prod_param_val.value_id "
                       "GROUP BY prod_par.id, val.id "
                       "ORDER BY prod_par.weight ASC, val.weight ASC", category, list_to_sql_array(products_ids)))
    else:
        cur.execute(
            str.format("SELECT "
                       "prod_par.id, "  # 0
                       "prod_par.name, "  # 1
                       "prod_par.first_image, "  # 2
                       "prod_par.second_image, "  # 3
                       "prod_par.weight, "  # 4
                       "val.id AS val_id, "  # 5
                       "val.value, "  # 6
                       "val.first_image AS val_first_image, "  # 7
                       "val.second_image AS val_second_image, "  # 8
                       "val.weight AS val_weight, "  # 9
                       "(SELECT COUNT(id) FROM product_parameters_values "
                       "AS ppv WHERE val.id = ppv.value_id) "  # 10
                       " FROM product_parameters AS prod_par JOIN product_parameters_available_value AS val ON "
                       "val.product_parameter_id = prod_par.id JOIN categories AS cat ON cat.id = prod_par.category_id "
                       "AND cat.name = '{0}' "
                       "LEFT JOIN product_parameters_values AS prod_param_val "
                       "ON val.id = prod_param_val.value_id "
                       "GROUP BY prod_par.id, val.id "
                       "ORDER BY prod_par.weight ASC, val.weight ASC", category))
    parameters = cur.fetchall()

    values = get_selected_parameters_values(request)
    return {'products': products, 'filter': get_filter_from_query(values, parameters),
            'max_page': max_page, 'price_min': price_min, 'price_max': price_max}


def catalogue_category_filter_json(request, category: str, order: str = "weight",
                                   product_on_page: str = settings.PRODUCT_ON_PAGE,
                                   page: str = 1):
    contents = catalogue_category_filter(request, category, order, product_on_page, page)

    products_data = []
    products = contents['products']
    for key, product in products:
        correctors_data = []
        correctors = product['price_correctors']
        if correctors:
            for corrector in correctors:
                correctors_data.append({
                    'id': corrector['id'],
                    'data': {
                        'name': corrector['name'],
                        'price': corrector['price'],
                        'price_new': corrector['price_new'],
                    },
                })
        images_data = []
        images = product['images']
        if images:
            for image in images:
                images_data.append({
                    'id': image['id'],
                    'data': {
                        'original': image['original'],
                        'large': image['large'],
                        'medium': image['medium'],
                        'small':  image['small'],
                        'weight': image['weight'],
                    },
                })
        products_data.append({
            'id': key,
            'data': {
                'name': product['name'],
                'code': product['code'],
                'url': product['url'],
                'weight': product['weight'],
                'default_new_price': product['default_new_price'],
                'default_price': product['default_price'],
                'description': product['description'],
                'mass': product['mass'],
                'is_new': product['is_new'],
                'is_top': product['is_top'],
                'images': images_data,
                'price_correctors': correctors_data,
                'sale_name': product['sale_name'],
                'sale_image': product['sale_image'],
                'date_on_add': product['date_on_add'],
            },
        })

        contents_data = {
            'products': products_data,
            'max_page': contents['max_page'],
            'price_max': contents['price_max'],
            'price_min': contents['price_min'],
            'filter': contents['filter'],
        }

    return JsonResponse(contents_data, charset='utf-8')


def catalogue_category(request, category: str, order: str = "weight", product_on_page: str = settings.PRODUCT_ON_PAGE,
                       page: str = 1):
    if page is None:
        page = 1
    if product_on_page is None:
        product_on_page = settings.PRODUCT_ON_PAGE
    if order is None:
        order = "weight"

    try:
        category = Category.objects.get(url=category)
    except Exception:
        raise Http404('Page not found')
    template = category.template.path
    return render(request, template, {'category': category})


def catalogue_prefilter(request, category: str, name: str):
    try:
        prefilter = PreFilter.objects.get(url=name)
    except Exception:
        raise Http404('Page not found')
    original_url = prefilter.original_url
    request = RequestFactory().get(prefilter.original_url)
    beg_pos = str.format('/catalogue/{0}/', category).__len__()
    template = prefilter.template.path
    try:
        end_pos = original_url.index('/?', beg_pos)
        order = original_url[beg_pos:end_pos]
        return render(request, template, {'prefilter': prefilter})
    except ValueError:
        products = catalogue_category_filter(request, category)
        return render(request, template, {'prefilter': prefilter})
