from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationForm

# Create your views here.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")

class RegisterView(View):
    def get(self, request):
        form=RegistrationForm()
        return render(request, "registration/register.html", {"form":form})

    def post(self, request):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            user.groups.add(form.cleaned_data['user_type'])

            return render(request, "registration/registration_success.html")
        return render(request, "registration/register.html", {"form":form})
