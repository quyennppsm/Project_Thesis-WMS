from django.shortcuts import render
from datetime import datetime
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'home.html',
        {
            'title': 'Home',
            'heading': 'Thesis Landing',
            'message': '"Belore`dorei, Andu-falah-dor!"',
            'content': 'Grata pagina documenti...',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'about.html',
        {
            'title': 'About',
            'heading': 'Abstract',
            'message': '"Listen to become a Legend!"',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact.html',
        {
            'title': 'Contact',
            'heading': 'Contact',
            'message': '"Mae govannen!"',
            'content': '',
            'year':datetime.now().year,
        }
    )