from django.db import models
from location_field.models.plain import PlainLocationField
from recurrence.fields import RecurrenceField

class TimeConstraints(models.Model):
  end_date    = models.DateField()
  start_date  = models.DateField()
  dt = models.DateTimeField()
  recurrence = RecurrenceField()
  
class LocationConstraints(models.Model):
  title = models.TextField(max_length=80)
  descr = models.TextField(max_length=255)
  location = PlainLocationField()

class MatterConstraints(models.Model):
  name  = models.TextField(max_length=80)
  descr = models.TextField(max_length=255)

class SkillConstraints(models.Model):
  title = models.TextField(max_length=80)
  descr = models.TextField(max_length=255)

class Interaction(models.Model):
  title = models.TextField(max_length=80)
  descr = models.TextField(max_length=255)
  time_cs = models.ForeignKey(TimeConstraints,
    on_delete = models.CASCADE,
    blank = True,
  )
  loc_cs  = models.ForeignKey(LocationConstraints,
    on_delete = models.CASCADE,
    blank = True,
    null = True,
  )
  matt_cs = models.ForeignKey(MatterConstraints,
    on_delete = models.CASCADE,
    blank = True,
    null = True,
  )
  skill_cs= models.ForeignKey(SkillConstraints,
    on_delete = models.CASCADE,
    blank = True,
    null = True,
  )
