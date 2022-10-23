from celery import shared_task
import datetime, calendar
from clients.models import Day


class Filler:
    WEEK = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }

    def __init__(self):
        self.month = datetime.datetime.now().date().month
        self.year = datetime.datetime.now().date().year
        self.num_days = calendar.monthrange(self.year, self.month)[1]

    def fill_db(self):
        days = [datetime.date(self.year, self.month, day) for day in range(1, self.num_days + 1)]
        for month_day in days:
            day_instance = Day(
                date=month_day,
                day=self.WEEK[datetime.datetime.weekday(month_day)]
            )
            day_instance.save()


@shared_task
def wrote_to_db():
    filler = Filler()
    filler.fill_db()
