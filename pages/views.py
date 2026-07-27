from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page (request):
    return HttpResponse('<html><title>Horse Owner</title><h1>Horse Owner</h1></html>')