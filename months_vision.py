import calendar
from database import UsingData, session
from datetime import date, datetime

class MonthBoard:
    def __init__(self, wanted_date: date):
        self.year = wanted_date.year
        self.month = wanted_date.month
        self.current_month_days = calendar.monthrange(year=self.year, month=self.month)[1]
        self.first_day = None
        self.inserted_days = 0
        self.month_matrix = None
        self.calculate_first_day()

    def calculate_first_day(self):
        self.first_day = calendar.weekday(year=self.year, month=self.month, day=1)
        return self.first_day

    def make_month_matrix(self):
        self.month_matrix = [
            [] for _ in range(6)
        ]
        for index, row in enumerate(self.month_matrix):
            if self.inserted_days <= self.current_month_days:
                for weekday in range(7):
                    if index == 0 and weekday < self.first_day:
                        value = "x"
                    elif self.current_month_days < self.inserted_days + 1:
                        value = "x"
                    else:
                        date_string = f"{self.year}-{self.month}-{self.inserted_days + 1}"
                        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
                        saved_data = session.query(UsingData).filter_by(date=date_object).first()
                        self.inserted_days += 1
                        value = 1 if saved_data and saved_data.is_study else 0

                    row.append((value, self.inserted_days))

        return self.month_matrix
