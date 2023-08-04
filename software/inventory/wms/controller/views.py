from django.shortcuts import render
from datetime import datetime
from django.http import HttpRequest
from controller.models import Layout, Slot, Product, Order, Carrier
from controller.templatetags.controller_tags import get_attr

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'controlpanel.html',
        {
            'name': 'Control panel',
            'year': datetime.now().year,
        }
    )
def layout(request):
    """Renders the layout page."""
    assert isinstance(request, HttpRequest)
    table = Layout.objects.all()
    columns = [field.name for field in Layout._meta.fields]
    rows = table
    return render(
        request,
        'tabledb.html',
        {
            'name': 'Layout db',
            'columns': columns,
            'rows': rows,
            'get_attr': get_attr,
            'year': datetime.now().year,
        }
    )

def slot(request):
    """Renders the slot page."""
    assert isinstance(request, HttpRequest)
    table = Slot.objects.all()
    columns = [field.name for field in Slot._meta.fields]
    rows = table
    return render(
        request,
        'tabledb.html',
        {
            'name': 'Slot db',
            'columns': columns,
            'rows': rows,
            'get_attr': get_attr,
            'year': datetime.now().year,
        }
    )

def product(request):
    """Renders the product page."""
    assert isinstance(request, HttpRequest)
    table = Product.objects.all()
    columns = [field.name for field in Product._meta.fields]
    rows = table
    return render(
        request,
        'tabledb.html',
        {
            'name': 'Product db',
            'columns': columns,
            'rows': rows,
            'get_attr': get_attr,
            'year': datetime.now().year,
        }
    )

def order(request):
    """Renders the order page."""
    assert isinstance(request, HttpRequest)
    table = Order.objects.all()
    columns = [field.name for field in Order._meta.fields]
    rows = table
    return render(
        request,
        'tabledb.html',
        {
            'name': 'Order db',
            'columns': columns,
            'rows': rows,
            'get_attr': get_attr,
            'year': datetime.now().year,
        }
    )

def carrier(request):
    """Renders the carrier page."""
    assert isinstance(request, HttpRequest)
    table = Carrier.objects.all()
    columns = [field.name for field in Carrier._meta.fields]
    rows = table
    return render(
        request,
        'tabledb.html',
        {
            'name': 'Carrier db',
            'columns': columns,
            'rows': rows,
            'get_attr': get_attr,
            'year': datetime.now().year,
        }
    )