from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from paperauthor.models import Paper
from baseportal.models import PublishedJournal, Volume


# Create your views here.

class HomePageView(View):
    def get(self, request):
        journals = PublishedJournal.objects.all()
        authors = User.objects.filter(groups__name='author')
        return render(request, "baseportal/homepage.html", {"journals": journals, "authors": authors})


class ListVolumeView(View):
    def get(self, request):
        volumes = Volume.objects.all()
        return render(request, "baseportal/listvolumes.html", {"volumes": volumes})


class ShowVolumeView(View):
    def get(self, request, volumeid):
        volume = Volume.objects.get(id=volumeid)
        return render(request, "baseportal/showvolume.html", {"volume": volume})


class SearchJournal(View):
    def get(self, request):
        keyword = request.GET.get("q", '')
        results = PublishedJournal.objects.filter(name__icontains=keyword)
        return render(request, "baseportal/search.html", {"results": results, "keyword": keyword})


class ShowJournalView(View):
    def get(self, request, journalslug):
        journal = get_object_or_404(PublishedJournal, slug=journalslug)
        return render(request, "baseportal/showjournal.html", {"journal": journal})


class AboutUsView(View):
    def get(self, request):
        return render(request, "baseportal/aboutus.html")


class TrackView(View):
    def get(self, request):
        track_id = request.GET.get('id', '')
        context = {"track_id": track_id}
        if track_id == '':
            context["showtrack"] = False
        else:
            try:
                paper = Paper.objects.get(track_id=track_id)

            except (ValidationError, ObjectDoesNotExist) as e:
                context["showerror"] = True
                paper = None

            if paper is not None:
                context["showtrack"] = True
                context["paper"] = paper
                if paper.reviewer is None:
                    context["trackstatus"] = 0
                elif paper.is_reviewed() is False:
                    context["trackstatus"] = 1
                else:
                    context["trackstatus"] = 2
        return render(request, "baseportal/track.html", context)


class RulesAuthorView(View):
    def get(self, request):
        return render(request, "baseportal/rules_author.html")


class RulesReviewerView(View):
    def get(self, request):
        return render(request, "baseportal/rules_reviewer.html")

class EditorialTeamView(View):
    def get(self, request):
        return render(request, "baseportal/editorialteam.html")
