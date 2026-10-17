from django.conf import settings 
from main.models import Product

class Catr:
    def __init__(self, request):
        self.session = request.session
        catr = self.session.get(settings.CART_SESSION_ID)
        if not catr:
            catr= self.session[settings.CART_SESSION_ID] = {}
        self.catr = catr

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.catr:
            self.catr[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity: 
            self.catr[product_id]['quantity'] = quantity
        else:
            self.catr[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product_id)
        if product_id in self.catr:
            del self.catr[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.catr.keys()
        products = Product.objects.filter(id__in=product_ids)
        catr = self.catr.copy()
        for product in products:
            catr[str(product.id)]['product'] = product 
        for item in catr.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item 
    def __len__(self):
        return sum(item['quantity'] for item in self.catr.values())

    def get_total_price(self):
        return sum(float(item ['price']) * item['quantity'] for item in self.catr.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save
