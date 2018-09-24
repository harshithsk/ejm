from django.db import models
from paperauthor.models import Paper
from django.contrib.auth.models import User


# Create your models here.
class PaperReviewRequest(models.Model):
    ACCEPTED = "ACC"
    REJECTED = "REJ"
    REVIEW_REQUEST_STATUS_CHOICES = (
        (ACCEPTED, "Accept"),
        (REJECTED, "Reject"),
    )
    status = models.CharField(
        max_length=3,
        choices=REVIEW_REQUEST_STATUS_CHOICES,
        blank=True,
        null=True,
        default=None,
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "reviewer"})
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, limit_choices_to={'reviewer': None})
    def __str__(self):
        return self.paper.title


class PaperReview(models.Model):
    ACCEPTED = "ACC"
    ACCEPTED_WITH_MINOR_CORRECTION = "AMI"
    ACCEPTED_WITH_MAJOR_CORRECTION = "AMA"
    REJECTED = "REJ"
    REVIEW_STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (ACCEPTED_WITH_MINOR_CORRECTION, "Accepted with minor correction"),
        (ACCEPTED_WITH_MAJOR_CORRECTION, "Accepted with major correction"),
        (REJECTED, "Rejected"),
    )
    paper = models.OneToOneField(Paper, on_delete=models.CASCADE)
    review_status = models.CharField(
        max_length=3,
        choices=REVIEW_STATUS_CHOICES,
        null=True,
        default=None,
    )
    comments_to_author = models.TextField(blank=True, null=True, default=None)
    comments_to_editor = models.TextField(blank=True, null=True, default=None)
    final_comments_to_author = models.TextField(blank=True, null=True, default=None)

    def review_complete(self):
        return self.paper.review_complete

    review_complete.boolean = True

    def __str__(self):
        return self.paper.title
