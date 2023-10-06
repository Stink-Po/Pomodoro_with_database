from ui_app import MainApp
from database import create_first_records
import asyncio


def start_pomodoro():
    asyncio.run(create_first_records())
    MainApp()


if __name__ == "__main__":
    start_pomodoro()
