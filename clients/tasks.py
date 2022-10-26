from celery import shared_task
import datetime, calendar
from clients.models import Day


class Filler:
    WEEK = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    WEEKEND = ("Воскресенье", "Понедельник")

    def __init__(self):
        self.month = datetime.datetime.now().date().month
        self.year = datetime.datetime.now().date().year
        self.num_days = calendar.monthrange(self.year, self.month)[1]

    def fill_db(self):
        days = [datetime.date(self.year, self.month, day) for day in range(1, self.num_days + 1)]
        for month_day in days:
            week_day = self.WEEK[datetime.datetime.weekday(month_day)]
            day_instance = Day(
                date=month_day,
                week_day=week_day,
                is_available=True if week_day not in self.WEEKEND else False
            )
            day_instance.save()


@shared_task
def wrote_to_db():
    filler = Filler()
    filler.fill_db()
