from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        extra_kwargs = {
            'action': {'help_text': 'Что нужно сделать'},
            'location': {'help_text': 'Где нужно сделать.'},
            'time': {'help_text': 'Время когда делать'},
        }

    def validate(self, data):
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError("Приятные привычки не могут иметь награды или связанные привычки.")
        else:
            if data.get('reward') and data.get('related_habit'):
                raise serializers.ValidationError("Привычка не может иметь и награду, и связанную привычку.")
            if not data.get('reward') and not data.get('related_habit'):
                raise serializers.ValidationError("Привычка должна иметь либо награду, либо связанную привычку.")
            if data.get('time_to_complete') > 120:
                raise serializers.ValidationError("Время на выполнение должно быть 120 секунд или меньше.")
        if data.get('periodicity') < 7:
            raise serializers.ValidationError("Привычка должна выполняться как минимум раз в неделю.")

        return data
