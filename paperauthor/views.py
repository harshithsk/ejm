from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import View
from paperauthor.forms import PaperForm, PaperResubmissionForm, ResubmissionForm, PaperFinalSubmissionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from paperauthor.models import Paper
from django.core.exceptions import PermissionDenied
from sendfile import sendfile
from django.urls import resolve, reverse

from paperreviewer.models import PaperReview


class IsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='author').exists()


def send_add_paper_email(request, paper):
    subject = "Paper has been added"
    visiturl = request.build_absolute_uri(reverse("admin:paperauthor_paper_change", args=[paper.id]))
    message = render_to_string("email/addpaper.txt", {"paper": paper, "visiturl": visiturl})
    editor_email = User.objects.get(is_superuser=True).email
    send_mail(subject, message, settings.ADMIN_EMAIL, [editor_email])
    visiturl = request.build_absolute_uri(reverse("paperauthor:showpaper", args=[paper.slug]))
    message = render_to_string("email/addpaperauthor.txt", {"paper": paper, "visiturl": visiturl})
    send_mail(subject, message, settings.ADMIN_EMAIL, [paper.author.email])

def send_final_submission_email(request, finalsubmit):
    subject = "Final Submission of paper completed"
    paper = finalsubmit.paper
    visiturl = request.build_absolute_uri(reverse("admin:paperauthor_paperfinalsubmission_change", args=[finalsubmit.id]))
    editor_email = User.objects.get(is_superuser=True).email
    message = render_to_string("email/final_submit_complete_admin.txt", {"paper": paper, "visiturl": visiturl})
    send_mail(subject, message, settings.ADMIN_EMAIL, [editor_email])
    visiturl = request.build_absolute_uri(reverse("paperauthor:showpaper", args=[paper.slug]))
    message = render_to_string("email/final_submit_complete_author.txt", {"paper": paper, "visiturl": visiturl})
    send_mail(subject, message, settings.ADMIN_EMAIL, [paper.author.email])

# Create your views here.
class AuthorPortalView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request):
        papers = Paper.objects.filter(author=request.user)
        context = {
            "papers": papers
        }
        return render(request, "paperauthor/portal.html", context)


class AddPaperView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request):
        form = PaperForm()
        return render(request, "paperauthor/addpaper.html", {"form": form})

    def post(self, request):
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            send_add_paper_email(request, paper)
            return redirect('paperauthor:portal')
        return render(request, "paperauthor/addpaper.html", {"form": form})


class ResubmitPaperView(IsAuthorMixin, LoginRequiredMixin, View):
    resubmit_allow = [PaperReview.ACCEPTED_WITH_MINOR_CORRECTION, PaperReview.ACCEPTED_WITH_MAJOR_CORRECTION]

    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if (paper.author != request.user) or not paper.is_resubmittable():
            raise PermissionDenied
        paperinitial = model_to_dict(paper, fields=('title', 'abstract', 'category','all_authors'))
        form = [
            PaperResubmissionForm(initial=paperinitial),
            ResubmissionForm()
        ]
        return render(request, "paperauthor/resubmit.html", {"form": form})

    def post(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if (paper.author != request.user) or not paper.is_resubmittable():
            raise PermissionDenied
        paperinitial = model_to_dict(paper, fields=('title', 'abstract', 'category'))
        form = [
            PaperResubmissionForm(request.POST, request.FILES, initial=paperinitial),
            ResubmissionForm(request.POST, request.FILES)
        ]
        if form[0].is_valid() and form[1].is_valid():
            newpaper = form[0].save(commit=False)
            newpaper.reviewer = paper.reviewer
            newpaper.author = paper.author
            newpaper.category = paper.category
            newpaper.save()
            resubmission = form[1].save(commit=False)
            resubmission.paper = newpaper
            resubmission.original_paper = paper
            resubmission.save()
            return redirect('paperauthor:portal')

        return render(request, "paperauthor/resubmit.html", {"form": form})


class ShowPaperView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user:
            raise PermissionDenied
        return render(request, "paperauthor/showpaper.html", {"paper": paper})


class DownloadPaperView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user:
            raise PermissionDenied
        return sendfile(request, paper.upload.path, attachment=True)


class DownloadSuggestedCorrectionsView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user:
            raise PermissionDenied
        return sendfile(request, paper.paperresubmission.suggested_corrections.path, attachment=True)


class DownloadPerformedCorrectionsView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user:
            raise PermissionDenied
        return sendfile(request, paper.paperresubmission.performed_corrections.path, attachment=True)

class PaperFinalSubmissionView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user or not paper.is_finalsubmittable():
            raise PermissionDenied
        form = PaperFinalSubmissionForm()
        return render(request, "paperauthor/finalsubmit.html",{"form":form, "paper":paper})
    
    def post(self, request, paperslug):
        paper = Paper.objects.get(slug=paperslug)
        if paper.author != request.user or not paper.is_finalsubmittable():
            raise PermissionDenied
        form = PaperFinalSubmissionForm(request.POST, request.FILES)
        if form.is_valid:
            finalsubmit = form.save(commit=False)
            finalsubmit.paper = paper
            finalsubmit.save()
            send_final_submission_email(request, finalsubmit)
            return render(request, "paperauthor/finalsubmitsuccess.html",{"paper":paper})
        return render(request, "paperauthor/finalsubmit.html",{"form":form, "paper":paper})
        


class AnnotateView(IsAuthorMixin, LoginRequiredMixin, View):
    def get(self, request):
        uri = request.GET.get('file', '')
        a = resolve(uri)
        paperslug = a.kwargs["paperslug"]
        paper = get_object_or_404(Paper, slug=paperslug)
        return render(request, "annotate/viewerreadonly.html", {"paper": paper})
