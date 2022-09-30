from . import models

# We can clearly see here that there is some code proceeding every view
# activation, which happens when the get_response() method is called.
# This middleware depaends on the session middleware
# We need to add this middleware to the settings 'main.middlewares.basket_middleware',


def basket_middleware(get_response):
    def middleware(request):
        if 'basket_id' in request.session:
            basket_id = request.session['basket_id']
            basket = models.Basket.objects.get(id=basket_id)
            request.basket = basket
        else:
            request.basket = None

        response = get_response(request)
        return response
    return middleware
