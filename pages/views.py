from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page (request):
    return render (request, "home.html")

def welcome_user (request):
    return HttpResponse('<html><title>Horse Owner</title><body><h1>Horse Owner</h1>Witaj Tester :)</body></html>')