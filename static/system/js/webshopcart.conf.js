$(function(){
    var settings = {
        mainClass: '.product-add_to_cart',
        actionClass: '.add-to-cart',
        buttonCartClass: '.product-button_cart',
        cartPreviewClass: '.web_shop_cart-preview',
        cartTotalPriceClass: '.web_shop_cart-total_price',
        cartTotalCountClass: '.web_shop_cart-total_count',
        cartClearClass: '.web_shop_cart-clear_all',
        cartFormOrderClass: '.web_shop_cart-form_order',
        cartFormProductHiddenClass: '.web_shop_cart-product_hidden_field',
        priceCorrectorCheckInput: '.product-price_corrector input[type="radio"]',
        priceCorrectorCheckClass: '.product-price_corrector',
        priceCorrectorPrintClass: '.product-price_corrector_print',
        productCountItemClass: '.product_count-in_cart',
        productAddItemClass: '.product_count-add_cart',
        productDeleteItemClass: '.product_count-delete_cart',
        productRemoveClass: '.product_remove',
        productShowModal: '.product_show_modal',
        buttonValueDefault: 'В корзину',
        buttonValueAdded: 'Добавить',
        buttonCountClass: '.button-lable_count'
    };

    var data_fields = {
        id: 'p',
        url: 'url',
        id_corrector: 'c',
        price: 'price',
        count: 'count'
    };

    var WebShopCart = new CartObject(settings, data_fields);

    // Catalogue - product modal:
    if ($(WebShopCart.settings.productShowModal).length > 0){
        $(WebShopCart.settings.productShowModal).click(function () {
            WebShopCart.getProductModal(this);
        });
    }

    // Catalogue - add to cart:
    if($(WebShopCart.settings.actionClass).length > 0) {
        $(WebShopCart.settings.actionClass).click(function () {
            WebShopCart.addProduct(this);
        });
    }

    // Catalogue - increment product count:
    if($(WebShopCart.settings.mainClass +' '+ WebShopCart.settings.productAddItemClass).length > 0) {
        $(WebShopCart.settings.mainClass +' '+ WebShopCart.settings.productAddItemClass).click(function () {
            WebShopCart.addCountProduct(this);
        });
    }

    // Catalogue - decrement product count:
    if($(WebShopCart.settings.mainClass +' '+ WebShopCart.settings.productDeleteItemClass).length > 0) {
        $(WebShopCart.settings.mainClass +' '+ WebShopCart.settings.productDeleteItemClass).click(function () {
            WebShopCart.deleteCountProduct(this);
        });
    }

    // Catalogue - change price correctors:
    if($(WebShopCart.settings.priceCorrectorCheckClass).length > 0) {
        $(WebShopCart.settings.priceCorrectorCheckInput).click(function () {
            WebShopCart.setPriceCorrector(this);
        });
        for(var i=0; i<$(WebShopCart.settings.priceCorrectorCheckClass).length; i++)
        {
            $(WebShopCart.settings.priceCorrectorCheckClass).eq(i).find('input[type="radio"]').first().click();
        }
    }

    // Cart preview - clear cart:
    if($(WebShopCart.settings.cartClearClass).length > 0) {
        $(WebShopCart.settings.cartClearClass).click(function () {
            WebShopCart.clearCart();
        });
    }

    // Cart preview - increment product count:
    if($(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productAddItemClass).length > 0) {
        $(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productAddItemClass).click(function () {
            WebShopCart.addCountProduct(this);
        });
    }

    // Cart preview - decrement product count:
    if($(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productDeleteItemClass).length > 0) {
        $(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productDeleteItemClass).click(function () {
            WebShopCart.deleteCountProduct(this);
        });
    }

    // Cart preview - product remove:
    if($(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productRemoveClass).length > 0) {
        $(WebShopCart.settings.cartPreviewClass +' '+ WebShopCart.settings.productRemoveClass).click(function () {
            WebShopCart.removeProduct(this);
        });
    }



    if($(WebShopCart.settings.cartFormClass).length > 0) {
        WebShopCart.renderOrderForm();
    }
});