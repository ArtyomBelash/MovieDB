from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .forms import CustomUserCreationForm, CustomUserLoginForm


def index(request):
    return HttpResponse(f'User {request.user.username}')


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LoginUser(FormView):
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
