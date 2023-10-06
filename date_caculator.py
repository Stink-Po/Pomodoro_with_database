from datetime import date, time, timedelta, datetime
from database import update_study_time
import time


# Return True if given year is leap otherwise False
def is_leap_year(year: int):
    if (year % 400 == 0) and (year % 100 == 0):
        return True

    elif (year % 4 == 0) and (year % 100 != 0):
        return True

    else:
        return False


leap_months = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

normal_months = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


class StudyTimer:

    def __init__(self):
        self.year = None
        self.month = None
        self.today = date.today()
        self.start_time = None
        self.end_time = None
        self.duration = 0
        self.current_month = None
        self.next_month = None
        self.previous_month = None
        self.get_current_next_and_previous_month(self.today)

    def write_data(self):
        update_study_time(current_date=self.today, study_time=self.duration)

    def timer_start(self):
        self.start_time = time.time()
        return self.start_time

    def timer_stop(self):
        self.end_time = time.time()
        final_duration = (self.end_time - self.start_time) // 60
        self.duration += final_duration
        return self.duration

    def get_current_date(self):
        self.year = date.today().year
        self.month = date.today().month

    def get_current_next_and_previous_month(self, date_object: date):
        self.current_month = date_object
        month = date_object.month
        if is_leap_year(date_object.year):
            current_month_long = leap_months[month]
        else:
            current_month_long = normal_months[month]

        self.previous_month = date_object - timedelta(days=current_month_long)
        self.next_month = date_object + timedelta(days=current_month_long)
        return self.previous_month, self.next_month, self.current_month

    def go_next_month(self):
        self.current_month, self.previous_month = self.next_month, self.current_month
        month_long = self.get_current_month_long(date_=self.current_month)
        self.next_month = self.current_month + timedelta(days=month_long)
        return self.previous_month, self.next_month, self.current_month

    def go_previous_month(self):
        self.current_month, self.next_month = self.previous_month, self.current_month
        month_long = self.get_current_month_long(date_=self.current_month)
        self.previous_month = self.current_month - timedelta(days=month_long)
        return self.previous_month, self.next_month, self.current_month

    @staticmethod
    def get_current_month_long(date_: date):
        month = date_.month
        if is_leap_year(date_.year):
            return leap_months[month]
        else:
            return normal_months[month]

    @staticmethod
    def date_object_from_string(date_string: str):
        return datetime.strptime(date_string, "%Y-%m-%d").date()

    @staticmethod
    def get_weekday_name(weekday: int):
        try:
            weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return weekday_names[weekday]
        except TypeError:
            pass

    def call_current_time_again(self):
        self.get_current_next_and_previous_month(self.today)
