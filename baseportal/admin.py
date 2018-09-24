from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from baseportal.models import PublishedJournal, Volume

# Register your models here.

admin.site.site_header = 'Ejournal administration'

admin.site.unregister(User)


def send_activated_email(request, user):
    subject = "Your application has been accepted"
    authorurl = request.build_absolute_uri(reverse("paperauthor:addpaper"))
    reviewurl = request.build_absolute_uri(reverse("paperreviewer:portal"))
    message = render_to_string("email/activate_user.txt", {"user": user, "authorurl": authorurl, "reviewurl":
        reviewurl})
    send_mail(subject, message, settings.ADMIN_EMAIL, [user.email])


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    actions = ['activate_user', 'deactivate_user']

    def activate_user(self, request, queryset):
        queryset.update(is_active=True)
        for user in queryset:
            send_activated_email(request, user)

    activate_user.short_description = "Activate selected Users"

    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_user.short_description = "Deactivate selected Users"


class PublishedJournalInline(admin.StackedInline):
    model = PublishedJournal
    extra = 0


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    inlines = [PublishedJournalInline]


@admin.register(PublishedJournal)
class PublishedJournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'published_date',)
