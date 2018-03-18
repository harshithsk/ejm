from django.forms.models import ModelForm
from paperauthor.models import Paper, PaperResubmission


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ('title', 'abstract', 'category', 'upload', 'keywords')

class PaperResubmissionForm(ModelForm):
    class Meta:
        model = Paper
        fields = ('title', 'abstract', 'upload')
    def __init__(self, *args, **kwargs):
        super(PaperResubmissionForm, self).__init__(*args,**kwargs)
        self.fields["title"].disabled=True
        #self.fields["category"].disabled=True

class ResubmissionForm(ModelForm):
    class Meta:
        model = PaperResubmission
        fields = ('suggested_corrections','performed_corrections')
