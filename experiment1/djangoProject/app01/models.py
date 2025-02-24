from django.db import models

# Create your models here.
from django.db import models
from decimal import Decimal

class AccuracySubmission(models.Model):
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    submission_time = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_accuracy(self):
        """Returns the accuracy as a string with a percent sign."""
        return f"{self.accuracy}%"

    def __str__(self):
        return f"Accuracy: {self.formatted_accuracy} | Submission Time: {self.submission_time}"
