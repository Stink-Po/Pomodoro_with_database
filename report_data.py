from database import UsingData, session
from sqlalchemy import func


class ReportData:
    def __init__(self):
        self.data = session.query(UsingData).all()
        self.total_usage = 0
        self.daily_best = 0
        self.best_month = None
        self.best_day_in_week = None

    def sum_usage(self):
        self.total_usage = (
                session.query(func.sum(UsingData.study_time)).scalar() or 0
        )
        return self.total_usage

    def get_daily_best(self):
        self.daily_best = (
                session.query(func.max(UsingData.study_time)).scalar() or 0
        )
        return self.daily_best

    def get_best_day_in_week(self):
        result = (
            session
            .query(UsingData.weekday, func.sum(UsingData.study_time))
            .group_by(UsingData.weekday)
            .order_by(func.sum(UsingData.study_time).desc())
            .first()
        )
        self.best_day_in_week = result or (0, 0)
        return self.best_day_in_week

    @staticmethod
    def get_month_records(start_date, end_date):
        print(start_date, end_date)
        try:
            total_study_time = session.query(func.sum(
                UsingData.study_time
            )).filter(UsingData.date >= start_date,
                      UsingData.date <= end_date).scalar()

            most_study_weekday = session.query(UsingData.weekday, func.sum(UsingData.study_time)).filter(
                UsingData.date >= start_date,
                UsingData.date <= end_date,
                UsingData.is_study.is_(True)
            ).group_by(UsingData.weekday).order_by(func.sum(UsingData.study_time).desc()).first()

            most_study_day = session.query(UsingData.date, func.sum(UsingData.study_time)).filter(
                UsingData.date >= start_date,
                UsingData.date <= end_date,
                UsingData.is_study.is_(True)
            ).group_by(UsingData.date).order_by(func.sum(UsingData.study_time).desc()).first()

            return total_study_time, most_study_day, most_study_weekday
        except AttributeError or TypeError:
            return 0, 0, (0, 0)
