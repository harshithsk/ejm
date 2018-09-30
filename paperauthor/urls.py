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
from paperauthor.views import AuthorPortalView, AddPaperView, ShowPaperView, \
    DownloadPaperView, AnnotateView, ResubmitPaperView, DownloadSuggestedCorrectionsView, \
    DownloadPerformedCorrectionsView, PaperFinalSubmissionView

app_name='paperauthor'

urlpatterns = [
    path('portal/', AuthorPortalView.as_view(), name='portal'),
    path('addpaper/', AddPaperView.as_view(), name='addpaper'),
    path('showpaper/<slug:paperslug>/',
        ShowPaperView.as_view(), name='showpaper'),
    path('resubmitpaper/<slug:paperslug>/',
        ResubmitPaperView.as_view(), name='resubmitpaper'),
    path('downloadpaper/<slug:paperslug>.pdf',
        DownloadPaperView.as_view(), name='downloadpaper'),
    path('annotate.html', AnnotateView.as_view(), name='annotate'),
    path('downloadsuggestedcorrections/<slug:paperslug>.pdf',
        DownloadSuggestedCorrectionsView.as_view(), name='downloadsuggestedcorrections'),
    path('downloadperformedcorrections/<slug:paperslug>.pdf',
        DownloadPerformedCorrectionsView.as_view(), name='downloadperformedcorrections'),
    path('finalsubmitpaper/<slug:paperslug>/',
        PaperFinalSubmissionView.as_view(), name='finalsubmitpaper')
]
