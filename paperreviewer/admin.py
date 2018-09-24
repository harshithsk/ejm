from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from paperauthor.models import Paper
from paperreviewer.models import PaperReview, PaperReviewRequest


def send_review_complete_email(request, paper, paperreview):
    subject = "Review Completed"
    visiturl = request.build_absolute_uri(reverse("paperreviewer:showpaper", kwargs={"paperslug": paper.slug}))
    message = render_to_string("email/review_complete.txt",
                               {"paper": paper, "paperreview": paperreview, "visiturl": visiturl})
    author_email = paper.author.email
    send_mail(subject, message, settings.ADMIN_EMAIL, [author_email])

def send_review_request_email(request, reviewrequest):
    paper=reviewrequest.paper
    subject="Request to review"
    visiturl = request.build_absolute_uri(reverse("paperreviewer:reviewrequest", kwargs={"paperid": reviewrequest.id}))
    message = render_to_string("email/review_request.txt",
                               {"paper": paper, "reviewrequest": reviewrequest, "visiturl": visiturl})
    reviewer_email = reviewrequest.reviewer.email

    send_mail(subject, message, settings.ADMIN_EMAIL, [reviewer_email])


# Register your models here.
@admin.register(PaperReview)
class PaperReviewAdmin(admin.ModelAdmin):
    list_display = ("paper", "review_status", "review_complete")
    search_fields = ("paper__title",)
    actions = ["complete_review", "undo_complete_review"]

    def complete_review(self, request, queryset):
        Paper.objects.filter(paperreview__in=queryset).update(review_complete=True)
        for paperreview in queryset:
            send_review_complete_email(request,paperreview.paper,paperreview)

    def undo_complete_review(self, request, queryset):
        Paper.objects.filter(paperreview__in=queryset).update(review_complete=False)


@admin.register(PaperReviewRequest)
class PaperReviewRequestAdmin(admin.ModelAdmin):
    exclude = ('status',)
    list_display = ('paper', 'reviewer', 'status')

    def save_model(self, request, obj, form, change):
        super(PaperReviewRequestAdmin, self).save_model(request, obj, form, change)
        send_review_request_email(request, obj)
