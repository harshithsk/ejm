"""paper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls.conf import path
from baseportal.views import HomePageView, TrackView, AboutUsView, ShowJournalView, SearchJournal, ListVolumeView, \
    ShowVolumeView, RulesAuthorView, RulesReviewerView, EditorialTeamView, VideoView

app_name='baseportal'

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('track', TrackView.as_view(), name="track"),
    path('aboutus/', AboutUsView.as_view(), name="aboutus"),
    path('showjournal/<slug:journalslug>/', ShowJournalView.as_view(), name="showjournal"),
    path('listvolume', ListVolumeView.as_view(), name="listvolume"),
    path('showvolume/<int:volumeid>', ShowVolumeView.as_view(), name="showvolume"),
    path('search', SearchJournal.as_view(), name='search'),
    path('rules/author', RulesAuthorView.as_view(), name='rulesauthor'),
    path('rules/reviewer', RulesReviewerView.as_view(), name='rulesreviewer'),
    path('editorial', EditorialTeamView.as_view(), name='editorialteam'),
    path('video', VideoView.as_view(), name='video'),
]
