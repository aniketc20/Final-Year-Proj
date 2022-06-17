from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SlotTimings(models.Model):
    slot_timing_id = models.AutoField(primary_key=True)
    slot_from_time = models.TimeField()
    slot_to_time = models.TimeField()
    
    def __str__(self) -> str:
        return str(self.slot_from_time) + " to " + str(self.slot_to_time)

class Billboard(models.Model):
    billboard_id = models.AutoField(primary_key=True)
    billboard_name = models.CharField(max_length=250, blank=False)
    billboard_location = models.CharField(max_length=250, blank=False)
    def __str__(self) -> str:
        return self.billboard_name + ":" + self.billboard_location
    
    class Meta:
        db_table = "billboard"


class Slot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    slot_date = models.DateField()
    slot_timing = models.ForeignKey(SlotTimings, on_delete = models.PROTECT)
    company = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, default=None, null=True)
    billboard = models.ForeignKey(Billboard, on_delete=models.PROTECT, blank=True, default=None)
    video_url = models.URLField(max_length=200, default=None)
    def __str__(self) -> str:
        return str(self.slot_date) + " Timings:" + str(self.slot_timing.slot_from_time)\
         + " Location-" + self.billboard.billboard_name + "-" + self.billboard.billboard_location
    
    class Meta:
        db_table = "slot"
