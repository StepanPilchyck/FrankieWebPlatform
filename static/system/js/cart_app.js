// init module webshopcart
var Cart = angular.module('webshopcart', ['ngCookies']);

// init staticObject custom object
Cart.staticObject = new SystemObject();

// set config default
Cart.config(function($interpolateProvider, $cookiesProvider) {
	$interpolateProvider.startSymbol('!{');
	$interpolateProvider.endSymbol('}!');
	$cookiesProvider.defaults = {
		path: '/',
	};
});

// registration controllers
Cart.controller('GetProductsInCartController', function($scope, $http, $cookies){

	$scope.totalCount = 0;
	$scope.totalPrice = 0;

    var getCart = Cart.staticObject.getCookies($cookies);
    var ids = '';
    if (getCart){
        for(var i=0; i<getCart.products.length; i++){
            ids += getCart.products[i].id.toString();
            if (getCart.products[i].data.price_correctors.length > 0){
                for (var j=0; j<getCart.products[i].data.price_correctors.length; j++){
                    if (j == 0){
                        ids += '_' + getCart.products[i].data.price_correctors[j].id.toString();
                    }else{
                        ids += '+' + getCart.products[i].data.price_correctors[j].id.toString();
                    }
                }
            }
            if (i < (getCart.products.length - 1)){
                ids += '.';
            }
        }
    }
	var response = $http.get('/cart/api/' + ids);

	response.success(function(data, status, headers, config) {
		var products = data.products;

		if (products.length > 0) {
			$scope.totalCount = Cart.staticObject.productGetTotalCount(getCart);
			$scope.totalPrice = Cart.staticObject.productGetTotalPrice(getCart);
		}

		$scope.products = products;
	});

	response.error(function(data, status, headers, config) {
		console.log('ERROR: AJAX failed!');
		console.log(status);
	});
});

Cart.controller('ActionCartController', function($scope, $cookies, $document){

	$scope.count = 1;

	$scope.productIncCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var new_count = (1 * count) + 1;
			$scope.count = new_count;
			var getCart = Cart.staticObject.getCookies($cookies);
			var json = Cart.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			Cart.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productDecCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 1){
			var new_count = (1 * count) - 1;
			$scope.count = new_count;
			var getCart = Cart.staticObject.getCookies($cookies);
			var json = Cart.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			Cart.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productChangeCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var getCart = Cart.staticObject.getCookies($cookies);
			var json = Cart.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: count},
				getCart
			);
			Cart.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productDeleteInCart = function(id, corrector_id, price){
		var getCart = Cart.staticObject.getCookies($cookies);
		var json = Cart.staticObject.productDelete(
			{id: id, corrector_id: corrector_id, price: price},
			getCart
		);
		Cart.staticObject.setCookies($cookies, json);
		var id_block = '_' + id.toString() + '_' + corrector_id.toString();
		angular.element(document.getElementById(id_block)).remove();
	};

	$scope.initProductCount = function(product_id, corrector_id){
		var getCart = Cart.staticObject.getCookies($cookies);
		if (getCart){
			if ((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (getCart.corrector_ids.indexOf(corrector_id.toString()) >= 0)){
				$scope.count = Cart.staticObject.productGetCount(product_id, corrector_id, getCart);
			}
			if ((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (corrector_id === '')){
				$scope.count = Cart.staticObject.productGetCount(product_id, false, getCart);
			}
		}
	};
});