# Add this import at the top
from django.db import models

# This is your new Jail model
class Jail(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Update the Prisoner model
class Prisoner(models.Model):
    # Add this ForeignKey field
    jail = models.ForeignKey(Jail, on_delete=models.CASCADE, related_name="prisoners")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    prisoner_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='prisoner_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.prisoner_id})"