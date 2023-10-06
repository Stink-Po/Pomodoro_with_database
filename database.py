from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, MetaData, Boolean, Date
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta
import asyncio

engine = create_engine('sqlite:///pomodoro.db', echo=False)
base = declarative_base()
session = sessionmaker(bind=engine)()
meta = MetaData()


class UsingData(base):
    __tablename__ = 'using_data'
    id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date, unique=True)
    weekday = Column(Integer)
    study_time = Column(Integer, default=0)
    is_study = Column(Boolean, default=False)

    def __init__(self, date_):
        self.date = date_
        self.weekday = date_.weekday()


base.metadata.create_all(engine)


def update_study_time(study_time, current_date):
    record = session.query(UsingData).filter_by(date=current_date).first()
    if record:
        try:
            record.study_time += study_time
            record.is_study = True
            session.commit()
        except SQLAlchemyError as e:
            print(f"error : {e}")
            session.rollback()
        finally:
            session.close()


async def insert_record(session_, today):
    new_record = UsingData(date_=today)
    try:
        session_.add(new_record)
        session_.commit()
    except SQLAlchemyError as e:
        print(f"error: {e}")
        session_.rollback()


async def create_first_records():
    today = date.today()
    if len(session.query(UsingData).all()) == 0:
        tasks = []
        for day in range(365 * 5):
            task = insert_record(session, today)
            tasks.append(task)
            today += timedelta(days=1)
        await asyncio.gather(*tasks)
