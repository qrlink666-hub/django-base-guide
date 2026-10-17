
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Product
from .catr import Catr
from .forms import CatrAddProductForm


@require_POST
def catr_add(request, product_id):
    catr = Catr(request)
    product = get_object_or_404(Product, id=product_id)
    form = CatrAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        # Используем имя поля quantity или quantyti
        quantity = cd.get('quantity', cd.get('quantyti'))

        if quantity is not None:
            catr.add(
                product=product,
                quantity=int(quantity),
                override_quantity=cd.get(
                    'override',
                    cd.get('override_quantyti', False)
                )
            )

    return redirect('catr:catr_detail')


@require_POST
def catr_remove(request, product_id):
    catr = Catr(request)
    product = get_object_or_404(Product, id=product_id)
    catr.remove(product)

    return redirect('catr:catr_detail')


def catr_detail(request):
    catr = Catr(request)

    for item in catr:
        item['update_quantity_form'] = CatrAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )

    return render(
        request,
        'catr/catr_detail.html',
        {'catr': catr}
    )
