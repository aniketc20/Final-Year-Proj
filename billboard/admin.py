from django.contrib import admin
from .models import Slot, SlotTimings, Billboard

# Register your models here.
admin.site.register(Slot)
admin.site.register(SlotTimings)
admin.site.register(Billboard)
