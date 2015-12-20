// init module webshopcart
var Catalogue = angular.module('webshopcart', ['ngCookies']);

// init staticObject custom object
Catalogue.staticObject = new SystemObject();

// set config default
Catalogue.config(function($interpolateProvider, $cookiesProvider) {
	$interpolateProvider.startSymbol('!{');
	$interpolateProvider.endSymbol('}!');
	$cookiesProvider.defaults = {
		path: '/',
	};
});

// init factory service
Catalogue.factory('TotalCountAndPriceFactory', function($cookies){
	var getCart = Catalogue.staticObject.getCookies($cookies);
	if (getCart){
		return {
			totalCount: Catalogue.staticObject.productGetTotalCount(getCart),
			totalPrice: Catalogue.staticObject.productGetTotalPrice(getCart)
		}
	}
	return {
		totalCount: 0,
		totalPrice: 0
	};
});

// registration controllers
Catalogue.controller('GetProductsFromCategoryController', function($scope, $http){

	var category_name = 'test';

	var response = $http.get('/catalogue/api/' + category_name + '/');

	response.success(function(data, status, headers, config) {
		var products = data.products;
		$scope.products = products;
		$scope.filter = data.filter;
		$scope.price_min = data.price_min;
		$scope.price_max = data.price_max;
		$scope.max_page = data.max_page;
	});

	response.error(function(data, status, headers, config) {
		console.log('ERROR: AJAX failed!');
		console.log(status);
	});
});

Catalogue.controller('ActionCartController', function($scope, $cookies, TotalCountAndPriceFactory){

	$scope.count = 1;
	$scope.productInCart = false;

	$scope.productAddToCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var getCart = Catalogue.staticObject.getCookies($cookies);
			var json = Catalogue.staticObject.productSetCart(
				{id: id, corrector_id: corrector_id, price: price, count: count},
				getCart
			);

			Catalogue.staticObject.setCookies($cookies, json);

			$scope.count = count;
			$scope.productInCart = true;

			$scope.totalCount = TotalCountAndPriceFactory.totalCount;
			$scope.totalPrice = TotalCountAndPriceFactory.totalPrice;
		}
	};

	$scope.productIncCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var new_count = (1 * count) + 1;
			$scope.count = new_count;
			var getCart = Catalogue.staticObject.getCookies($cookies);
			var json = Catalogue.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			Catalogue.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productDecCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 1){
			var new_count = (1 * count) - 1;
			$scope.count = new_count;
			var getCart = Catalogue.staticObject.getCookies($cookies);
			var json = Catalogue.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: new_count},
				getCart
			);
			Catalogue.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productChangeCountCart = function(id, corrector_id, price, count){
		if (!isNaN(parseFloat(count)) && isFinite(count) && count > 0){
			var getCart = Catalogue.staticObject.getCookies($cookies);
			var json = Catalogue.staticObject.productSetCount(
				{id: id, corrector_id: corrector_id, price: price, count: count},
				getCart
			);
			Catalogue.staticObject.setCookies($cookies, json);
		}
	};

	$scope.productDeleteInCart = function(id, corrector_id, price, count){

	};

	$scope.initButtonCart = function(product_id, corrector_id){
		var getCart = Catalogue.staticObject.getCookies($cookies);
		if (getCart){
			if (
				((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (getCart.corrector_ids.indexOf(corrector_id.toString()) >= 0)) ||
				((getCart.product_ids.indexOf(product_id.toString()) >= 0) && (corrector_id === false))
			){
				$scope.count = Catalogue.staticObject.productGetCount(product_id, corrector_id, getCart);
				$scope.productInCart = true;
			}
		}
	};
});

Catalogue.controller('CartPreviewController', function($scope, $cookies, TotalCountAndPriceFactory){
	$scope.totalCount = TotalCountAndPriceFactory.totalCount;
	$scope.totalPrice = TotalCountAndPriceFactory.totalPrice;
});