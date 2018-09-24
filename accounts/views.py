from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationForm
from paperauthor.models import Paper
from baseportal.models import PublishedJournal

def send_user_register_email(request, user):
    subject = "Registered User"
    message = render_to_string("email/user_register_user.txt", {"user": user})
    user_email = user.email
    send_mail(subject, message, settings.ADMIN_EMAIL, [user_email])
    message = render_to_string("email/user_register_editor.txt", {"user": user})
    editor_email = User.objects.get(is_superuser=True).email
    send_mail(subject, message, settings.ADMIN_EMAIL, [editor_email])


# Create your views here.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        a=Paper.objects.filter(author=request.user)
        b=PublishedJournal.objects.all()[:3]
        return render(request, "accounts/profile.html", {"a":a, "b":b})

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
            send_user_register_email(request, user)

            return render(request, "registration/registration_success.html")
        return render(request, "registration/register.html", {"form":form})
