from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def home_page (request):
    return render (request, "home.html")

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def dashboard_view (request):
    return render (request, "dashboard.html")