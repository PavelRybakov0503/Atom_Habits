from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "time",
        "place",
        "action",
        "pleasant_habit",
        "related_habit",
        "periodicity",
        "reward",
        "time_to_complete",
        "is_published",
    )
