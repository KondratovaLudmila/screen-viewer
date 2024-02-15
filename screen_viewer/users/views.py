from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator


from .forms import UserAddForm, SigninForm, VerifyForm, DeleteForm, UserEditForm
from .models import User, Profile
from viewer.models import Location
from .decorators import superuser_required
from services.otp_handler import totp_handler


# Create your views here.

@method_decorator(superuser_required, name='dispatch')
class UserAddView(CreateView):
    template_name = "user.html"
    form_class = UserAddForm
    success_url = reverse_lazy("users:users")


@method_decorator(superuser_required, name='dispatch')
class UserEditView(UpdateView):
    template_name = "user_edit.html"
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("users:users")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['profile_locations'] = Profile.objects\
                                        .filter(user=context['user'])\
                                        .values_list('locations__id', flat=True)
        context['user'] = self.request.user
        return context


@method_decorator(superuser_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("users:users")
    form_class = DeleteForm
    template_name = "user_delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        return context

@method_decorator(superuser_required, 'dispatch')
class UsersView(ListView):
    template_name = "users.html"
    model = User
    
    
class LogsView(TemplateView):
    template_name = "logs.html"

    @superuser_required
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        users = User.objects.get()
        return render(request, self.template_name, context={"users": users})
    


class SigninView(LoginView):
    template_name = 'signin.html'
    form_class = SigninForm
    verify_template_name = "verify.html"

        
    def post(self, request):
        message = ''
        form = self.form_class(request.POST, data=request.POST)
        
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                if user.profile.verified:
                    login(request, user)
                    return redirect('viewer:viewer')
                else:
                    totp_handler.get_qrcode(user.profile.otp_key, user.username)
                    name = user.username
                    return render(request, self.verify_template_name, context={'username': name, "message": message})
                
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
    

class VerifyUser(FormView):
    template_name = 'verify.html'
    form_class = VerifyForm

    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                verify=True
            )
            if user is not None:
                user.profile.verified = True
                user.profile.save()
                login(request, user)
                return redirect('viewer:viewer')
                
        message = 'Login failed!'
        name = request.POST.get("username")
        return render(request, self.template_name, context={'username': name, 'message': message})
    
