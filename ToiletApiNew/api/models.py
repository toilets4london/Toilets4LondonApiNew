from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Toilet(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=300, blank=True, default="")
    access_notes = models.CharField(max_length=300, blank=True, default="")
    is_free = models.BooleanField(default=True)
    charge = models.CharField(max_length=100, blank=True, default="")
    opening_hours = models.CharField(max_length=300, blank=True, default="")
    is_open = models.BooleanField(default=True)
    male_only = models.BooleanField(default=False)
    female_only = models.BooleanField(default=False)
    unisex = models.BooleanField(default=False)
    baby_change = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    radar_only = models.BooleanField(default=False)
    radar_available = models.BooleanField(default=False)
    changing_place = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    data_source = models.CharField(max_length=200, blank=True, default="")
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    num_ratings = models.IntegerField(blank=True, default=0)
    rating = models.FloatField(blank=True, null=True)

    @property
    def lat_lng(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def __str__(self):
        if len(self.name) > 0:
            return self.name + " " + str(self.pk)
        else:
            return str(self.pk)

    class Meta:
        ordering = ['-date_modified']


class SuggestedToilet(models.Model):
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    details = models.CharField(blank=True, max_length=1000, default='')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Rating(models.Model):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))

    toilet = models.ForeignKey(Toilet, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Toilet %s rated %s" % (self.toilet.__str__(), self.date.strftime("%m/%d/%Y, %H:%M:%S"))

    class Meta:
        ordering = ['-date']


class Report(models.Model):
    REASON_CHOICES = [
        ('DNE', 'This toilet does not exist'),
        ('O', 'Other')
    ]

    reason = models.CharField(
        max_length=3,
        choices=REASON_CHOICES,
        blank=False
    )

    other_description = models.TextField(blank=True, default="", max_length=500)
    toilet = models.ForeignKey(Toilet, on_delete=models.CASCADE, related_name='reports')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Toilet %s reported %s" % (self.toilet.__str__(), self.date.strftime("%m/%d/%Y, %H:%M:%S"))

    class Meta:
        ordering = ['-date']