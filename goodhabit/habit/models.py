from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_habits')
    periodicity = models.PositiveIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, blank=True)
    time_to_complete = models.PositiveIntegerField()  # в секундах
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError("Приятные привычки не могут иметь награды или связанные привычки.")
        else:
            if self.reward and self.related_habit:
                raise ValidationError("Привычка не может иметь и награду, и связанную привычку.")
            if not self.reward and not self.related_habit:
                raise ValidationError("Привычка должна иметь либо награду, либо связанную привычку.")
            if self.time_to_complete > 120:
                raise ValidationError("Время на выполнение должно быть 120 секунд или меньше.")
        if self.periodicity < 7:
            raise ValidationError("Привычка должна выполняться как минимум раз в неделю.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.action} at {self.time} in {self.location}'
