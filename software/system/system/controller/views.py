from django.http import HttpResponse
from django.shortcuts import render
import sqlite3

def index(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM controller_product')
    rows = cursor.fetchall()
    conn.close()
    return render(request, 'controller/index.html', {'rows': rows})