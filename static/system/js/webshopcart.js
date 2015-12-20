/* Assigen CartTmpObject */

function CartObject(settings, data_fields)
{
    this.settings = settings;
    this.data = data_fields;
    this.csrftoken = this.getCsrftoken('csrftoken');
}
CartObject.prototype = Object.create(CartTmpObject.prototype);
CartObject.prototype.constructor = CartObject;



CartObject.prototype.getCsrftoken = function(context)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '')
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++)
        {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, context.length + 1) == (context + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(context.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

CartObject.prototype.getDataFields = function(context)
{
    var data = {};
    var t = context.attributes;
    for (var i=0; i < t.length; i++)
    {
        if(t[i].name.substring(0, 5) == 'data-') {
            data[t[i].name.substring(5, t[i].name.length)] = t[i].value;
        }
    }
    return data;
};

CartObject.prototype.getProducts = function()
{
    var csrftoken = this.csrftoken;
    var products = {};
    $.ajax({
        url: '/api/get_products',
        async: false,
        type: 'POST',
        data:
        {
            'csrfmiddlewaretoken': csrftoken
        },
        success: function (data)
        {
            products = data;
        }
    });
    return products;
};

CartObject.prototype.getPreview = function(context)
{
    if (!context)
    {
        return false;
    }

    var keys = [];
    for (var obj in context)
    {
        if ((obj != 't_price') && (obj != 't_count'))
        {
            keys.push(obj);
        }
    }
    keys = keys.sort();

    var html = '';
    for (var i=0; i<keys.length; i++)
    {
        var c = context[keys[i]];
        html += this.getPreviewTmp({
            'img': c['img_url'],
            'name': c['p_name'],
            'url': c['p_url'],
            'id': c['p'],
            'idc': (c['c'] == null)?'': c['c'],
            'count': c['p_count'],
            'price': c['price']
        });
    }

    $(this.settings.cartPreviewClass).html(html);

    var CO = this;
    $(this.settings.cartPreviewClass).find(this.settings.productDeleteItemClass).click(function(){
        CO.deleteCountProduct(this);
    });

    $(this.settings.cartPreviewClass).find(this.settings.productAddItemClass).click(function(){
        CO.addCountProduct(this);
    });

    $(this.settings.cartPreviewClass).find(this.settings.productRemoveClass).click(function(){
        CO.removeProduct(this);
    });

    if ($(this.settings.cartFormOrderClass).find(this.settings.cartFormProductHiddenClass).length > 0)
    {
        this.renderOrderForm();
    }

    this.getTotalCount(context);
    this.getTotalPrice(context);

    return true;
};

CartObject.prototype.getProductModal = function(context)
{
    var thisObj = this;
    var url = $(context).attr('data-'+thisObj.data.url);
    $.post('/api/products_modal/' + url,
    {
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(p)
    {
        var t = thisObj.getProductModalTmp({
            'product': p.product,
            'product_images': p.product_images,
            'product_in_cart': p.product_in_cart,
            'product_parameters': (p.product_parameters.length === 0)?null:p.product_parameters,
            'product_price_corrector': (p.product_price_corrector.length === 0)?null:p.product_price_corrector
        });
        console.log(t);
    })
};

CartObject.prototype.getTotalPrice = function(context)
{
    if (context['t_price'] == undefined)
    {
        $(this.settings.cartTotalPriceClass).html('');
    }
    else
    {
        $(this.settings.cartTotalPriceClass).html(context['t_price']);
    }
};

CartObject.prototype.getTotalCount = function(context)
{
    if (context['t_price'] == undefined)
    {
        $(this.settings.cartTotalCountClass).html('');
    }
    else
    {
        $(this.settings.cartTotalCountClass).html(context['t_count']);
    }
};

CartObject.prototype.setButtonCart = function(products, product)
{
    var p = $(this.settings.mainClass + ' ' + this.settings.buttonCartClass + ' ' + this.settings.productAddItemClass).filter('[data-'+this.data.id+'="'+product['p']+'"]');

    if (p.length > 0)
    {
        if (products[product['p']])
        {
            p.closest(this.settings.mainClass).find(this.settings.productCountItemClass).html(products[product['p']]['p_count']);
        }
        if (products[product['p']+'_'+product['c']])
        {
            var p_c = p.closest(this.settings.mainClass).find(this.settings.productAddItemClass).attr('data-'+this.data.id_corrector);
            if(p_c == product['c'])
            {
                p.closest(this.settings.mainClass).find(this.settings.productCountItemClass).html(products[product['p']+'_'+product['c']]['p_count']);
            }
        }
    }
};

CartObject.prototype.setPriceCorrector = function(context)
{
    var data_field = $(context).closest(this.settings.mainClass).find(
        this.settings.actionClass +', '+
        this.settings.productAddItemClass +', '+
        this.settings.productDeleteItemClass
    );

    data_field.attr('data-' + this.data.price, $(context).val());
    data_field.attr('data-' + this.data.id_corrector, $(context).attr('data-' + this.data.id_corrector));

    $(context).closest(this.settings.mainClass).find(this.settings.priceCorrectorPrintClass).html($(context).val());

    if ($(context).closest(this.settings.mainClass).find(this.settings.productCountItemClass).length > 0)
    {
        var products = this.getProducts();
        var t = $(context).attr('data-'+this.data.id)+'_'+$(context).attr('data-'+this.data.id_corrector);
        if (products[t])
        {
            this.setButtonCart(products, {'c': products[t]['c'],'p': products[t]['p'], 'price': products[t]['price']});
        }
        else
        {
            $(context).closgetPreviewTmpest(this.settings.mainClass).find(this.settings.productCountItemClass).html(0);
        }
    }
};

CartObject.prototype.addProduct = function(context)
{
    var new_product = this.getDataFields(context);
    var thisObj = this;
    $.post("/api/add_product",
    {
        'p':new_product[this.data.id],
        'c':new_product[this.data.id_corrector],
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(data)
    {
        thisObj.getPreview(data);
        if (context)
        {
            var p = thisObj.getDataFields(context);
            var buttonCart = $(context).closest(thisObj.settings.mainClass);
            buttonCart.find(thisObj.settings.buttonCartClass).html(thisObj.getButtonInCartTmp({
                'id': p.p,
                'idc': (!p.c)?'': p.c
            }));

            if(p['c'])
            {
                var data_field = buttonCart.find(
                    thisObj.settings.buttonCartClass+' '+thisObj.settings.productAddItemClass+', '+
                    thisObj.settings.buttonCartClass+' '+thisObj.settings.productDeleteItemClass
                );
                data_field.attr('data-' + thisObj.data.price, p['price']);
                data_field.attr('data-' + thisObj.data.id_corrector, p['c']);
            }

            buttonCart.find(thisObj.settings.productAddItemClass).click(function(){
                thisObj.addCountProduct(this);
            });

            buttonCart.find(thisObj.settings.productDeleteItemClass).click(function(){
                thisObj.deleteCountProduct(this);
            });
        }
    })
};

CartObject.prototype.addCountProduct = function(context)
{
    var new_product = this.getDataFields(context);
    var thisObj = this;
    $.post("/api/add_product",
    {
        'p':new_product[this.data.id],
        'c':new_product[this.data.id_corrector],
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(data)
    {
        thisObj.getPreview(data);
        thisObj.setButtonCart(data, thisObj.getDataFields(context));
    })
};

CartObject.prototype.deleteCountProduct = function(context)
{
    var thisObj = this;
    var prod_del = this.getDataFields(context);
    $.post("/api/del_product",
    {
        'p':prod_del[thisObj.data.id],
        'c':prod_del[thisObj.data.id_corrector],
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(data)
    {
        thisObj.getPreview(data);
        thisObj.setButtonCart(data, thisObj.getDataFields(context));
    });
    return true;
};

CartObject.prototype.removeProduct = function(context)
{
    var thisObj = this;
    var prod_del = this.getDataFields(context);
    $.post("/api/rem_product",
    {
        'p':prod_del[thisObj.data.id],
        'c':prod_del[thisObj.data.id_corrector],
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(data)
    {
        thisObj.getPreview(data);

        var p = $(thisObj.settings.mainClass + ' ' + thisObj.settings.buttonCartClass + ' ' + thisObj.settings.productAddItemClass).filter('[data-'+thisObj.data.id+'="'+prod_del['p']+'"]');

        if (p.length > 0)
        {
            if (!prod_del['c'])
            {
                var t = p.closest(thisObj.settings.buttonCartClass);
                t.html(thisObj.getButtonDefaultCartTmp({
                    'id': prod_del['p'],
                    'idc': (!prod_del['c'])?'': prod_del['c']
                }));
                t.find(thisObj.settings.actionClass).click(function () {
                    thisObj.addProduct(this);
                });
                return true;
            }
            if (prod_del['c'])
            {
                var flag = true;
                for(var product in data)
                {
                    if(data[product]['p'] == prod_del['p'])
                    {
                        flag = false;
                        break;
                    }
                }
                if (flag)
                {
                    var t = p.closest(thisObj.settings.buttonCartClass);
                    t.html(thisObj.getButtonDefaultCartTmp({
                        'id': prod_del['p'],
                        'idc': (!prod_del['c'])?'': prod_del['c']
                    }));
                    t.find(thisObj.settings.actionClass).click(function () {
                        thisObj.addProduct(this);
                    });
                }
                if ((prod_del['p'] == p.attr('data-'+thisObj.data.id)) && (prod_del['c'] == p.attr('data-'+thisObj.data.id_corrector)))
                {
                    p.closest(thisObj.settings.buttonCartClass).find(thisObj.settings.productCountItemClass).html('0');
                }
                return true;
            }
        }
        return false;
    });
    return true;
};

CartObject.prototype.clearCart = function()
{
    var thisObj = this;
    $.post("/api/clear_cart",
    {
        'csrfmiddlewaretoken':thisObj.csrftoken
    },
    function(data)
    {
        thisObj.getPreview(data);
    });
    return true;
};

CartObject.prototype.renderOrderForm = function()
{
    var products = this.getProducts();
    var html = '';
    for(var p in products)
    {
        if ((p != 't_count') && (p != 't_price'))
        {
            if (products[p]['c'] != null)
            {
                html += '<input type="hidden" name="product_positions" value="' +
                    products[p]['p'] + ';' +
                    products[p]['p_count'] + ';' +
                    products[p]['c'] +
                '">';
            }
            else
            {
                html += '<input type="hidden" name="product_positions" value="' +
                    products[p]['p'] + ';' +
                    products[p]['p_count'] +
                '">';
            }

        }
    }
    html += '<input type="hidden" name="total_price" value="'+ ((products['t_price'] == undefined)?'0':products['t_price']) +'">';
    $(this.settings.cartFormProductHiddenClass).html(html);
};