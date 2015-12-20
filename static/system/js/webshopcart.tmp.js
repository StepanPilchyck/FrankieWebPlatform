function CartTmpObject()
{
}



CartTmpObject.prototype.getPreviewTmp = function(p)
{
    /*
    p.img - image url,
    p.name - product name,
    p.url - product url,
    p.id - product id,
    p.idc - price corrector,
    p.count - product count,
    p.price - product price,
    */

    return '<div class="row body-cart">'+
                '<div class="col-sm-4 body-cart-cust-1">'+
                    '<img src="'+ p.img +'" alt="alt">'+
                    '<p class="product_name">'+ p.name +'</p>'+
                '</div>'+
                '<div class="col-sm-3 text-center call-1">'+
                    '<img class="product_count-delete_cart" data-p="'+ p.id +'" data-c="'+ p.idc +'" src="/static/images/add-good.png" alt="Delete">'+
                    '<span class="all-good-cart count"> '+ p.count +' </span>'+
                    '<img class="product_count-add_cart" data-p="'+ p.id +'" data-c="'+ p.idc +'" src="/static/images/rgood.png" alt="Add">'+
                '</div>'+
                '<div class="col-sm-2 price-cart-tr text-center">'+
                    '<p><span class="price">'+ p.price +'</span> грн</p>'+
                '</div>'+
                '<div class="col-sm-3 price-cart-tr">'+
                    '<p>' + (p.price * p.count) + ' грн '+
                    '<img src="/static/images/delete_icon.png" class="product_remove" data-p="'+ p.id +'" data-c="'+ p.idc +'" alt="Remove">'+
                    '</p>'+
                '</div>'+
            '</div>';
};

CartTmpObject.prototype.getButtonInCartTmp = function(p)
{
    /*
    p.id - product id,
    p.idc - price corrector,
    */

    return '<input class="product_count-add_cart" value="+" data-p="'+ p.id +'" data-c="'+ p.idc +'" type="button">'+
        '<span class="product_count-in_cart">1</span>'+
        '<input class="product_count-delete_cart" value="-" data-p="'+ p.id +'" data-c="'+ p.idc +'" type="button">';
};

CartTmpObject.prototype.getButtonDefaultCartTmp = function(p)
{
    /*
    p.id - product id,
    p.idc - price corrector,
    */

    return '<input type="button" class="add-to-cart" value="Add to cart" name="Add" data-p="'+ p.id +'" data-c="'+ p.idc +'" />';
};

CartTmpObject.prototype.getProductModalTmp = function(p)
{
    /*
    product
     |--- id
     |--- name
     |--- url
     |--- default_price
    product_images[]
     |--- large_image
     |--- medium_image
     '--- small_image
    product_in_cart
    product_parameters
    product_price_corrector
     |--- id
     |--- name
     '--- new_price
    */

    var images = '';
    for (var i=0; i< p.product_images.length; i++)
    {
        if (i==0)
        {
            images += '<img src=' + p.product_images[0].small_image + ' alt="' + p.product_images[0].name + '"/>';
        }
    }

    var price_corrector = '';
    if (p.product_price_corrector)
    {
        price_corrector += '<div class="product-price_corrector">';
        for (var i=0; i< p.product_price_corrector.length; i++)
        {
            price_corrector += '<label for="cor_'+ p.product.id +'_'+ p.product_price_corrector[i].id +'">'+ p.product_price_corrector[i].name +'</label>'+
            '<input type="radio" name="product_'+ p.product.id +'" id="cor_'+ p.product.id +'_'+ p.product_price_corrector[i].id +'" value="'+ p.product_price_corrector[i].new_price +'" data-p="'+ p.product.id +'" data-c="'+ p.product_price_corrector[i].id +'">';
        }
        price_corrector += '</div>'+
            '<span class="product-price_corrector_print"></span>';
    }
    else
    {
        price_corrector += '<span class="product-price">'+ p.product.default_price +'</span>';
    }

    var count_in_cart = '';
    if (p.product_in_cart > 0)
    {
        count_in_cart += '<input class="product_count-add_cart" value="+" data-p="'+ p.product.id +'" data-c="" type="button">'+
        '<span class="product_count-in_cart">'+ p.product_in_cart +'</span>'+
        '<input class="product_count-delete_cart" value="-" data-p="'+ p.product.id +'" data-c="" type="button">';
    }
    else
    {
        count_in_cart += '<input type="button" class="add-to-cart" value="Add to cart" name="Add" data-p="'+ p.product.id +'" data-c="" />';
    }

    var html = '<div class="product-add_to_cart">'+
    '<a href="/product/'+ p.product.url +'">'+
        images +
    '</a>'+
    '<br>'+
    '<a href="/product/'+ p.product.url +'">'+
        p.product.name +
    '</a>'+
    '<br>'+
        price_corrector +
    '<br>'+
    '<div class="product-button_cart">'+
        count_in_cart +
    '</div>'+
    '<br>'+
    '</div>';

    return html;
};