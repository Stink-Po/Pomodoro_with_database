import math
from tkinter import *
from sound_player import Sounds
from constence import *
from months_vision import MonthBoard
from date_caculator import StudyTimer
from report_data import ReportData


class MainApp:
    def __init__(self):
        self.timer_calculator = StudyTimer()
        self.sound_player = Sounds()
        self.repeats = 0
        self.window = Tk()
        self.canvas = Canvas(width=300, height=300, bg=YELLOW, highlightthickness=0)
        self.label = Label(text="Timer", font=("Ink Free", 30, "bold"), bg=YELLOW, fg=GREEN)
        self.tomato_image = PhotoImage(file="images/tomato.png")
        self.timer_text = None
        self.timer = None
        self.button = Button(text="Start", bg=YELLOW, highlightthickness=0, command=self.start_timer, )
        self.report_button = Button(text="Report", bg=YELLOW, highlightthickness=0, command=self.show_records)
        self.stop_button = Button(text="Stop", bg=YELLOW, highlightthickness=0, command=self.reset)
        self.next_month_btn = Button(text="Next", bg=YELLOW, highlightthickness=0, command=self.next_record)
        self.previous_month_btn = Button(text="Previous", bg=YELLOW, highlightthickness=0, command=self.previous_record)
        self.date_label = Label(text="", bg=YELLOW, fg=GREEN)
        self.back_btn = Button(text="Back", bg=YELLOW, highlightthickness=0, command=self.back_btn_press)
        self.report_label = Label(text="",bg=YELLOW, fg=GREEN)
        self.config()
        self.grid_start()
        self.window.mainloop()

    # config set window size and title
    def config(self):
        self.canvas.delete("all")
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=100, bg=YELLOW)
        self.window.minsize(width=600, height=600)
        self.window.maxsize(width=600, height=600)
        self.canvas.create_image(150, 150, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(150, 150, text="00:00", font=("Ink Free", 25, "bold"), fill="white")
        return self.timer_text

    def grid_start(self):
        self.label.grid(column=0, row=0, columnspan=3)
        self.canvas.grid(column=1, row=1)
        self.button.grid(column=0, row=2, columnspan=3)
        self.report_button.grid(column=0, row=3, columnspan=3)

    # after pressing start button this function will remove the start button and report button and replace with stop btn
    def grid_start_press(self):
        self.timer_calculator.timer_start()
        self.button.grid_forget()
        self.report_button.grid_forget()
        self.stop_button.grid(column=0, row=4)

    # when we are in report page after press this button every thing will take us to main page delete old items and
    # replace new ones
    def back_btn_press(self):
        self.report_label.grid_forget()
        self.timer_calculator.call_current_time_again()
        self.date_label.grid_forget()
        self.back_btn.grid_forget()
        self.next_month_btn.grid_forget()
        self.previous_month_btn.grid_forget()
        self.config()
        self.grid_start()

    # Counting down and simulate clock in tkinter canvas
    def count_down(self, count):
        count_minute = math.floor(count / 60)
        count_second = count % 60
        if count_second == 0:
            count_second = "00"
        elif count_second < 10:
            count_second = f"0{count_second}"
        if count_minute < 10:
            count_minute = f"0{count_minute}"
        self.canvas.itemconfig(self.timer_text, text=f"{count_minute}:{count_second}")
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()

    # Start the pomodoro app and change canvas and labels to break or study ...
    def start_timer(self):
        self.config()
        self.grid_start()
        self.grid_start_press()
        self.repeats += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60
        if self.repeats % 8 == 0:
            self.sound_player.long_break()
            self.count_down(long_break_sec)
            self.label.config(text="Long Break", fg="#81CACF")

        elif self.repeats % 2 == 0:
            self.sound_player.short_break()
            self.count_down(short_break_sec)
            self.label.config(text="Short Break", fg="#5A8F7B")

        else:
            self.sound_player.study()
            self.count_down(work_sec)
            self.label.config(text="Study", fg="#355764")

        return self.repeats

    # Reset the Buttons canvas label
    def reset(self):
        self.timer_calculator.timer_stop()
        self.timer_calculator.write_data()
        self.stop_button.grid_forget()
        self.grid_start()
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.label.config(text="Timer", fg=GREEN)
        self.repeats = 0
        return self.repeats

    def show_records(self):
        self.report_button.grid_forget()
        self.button.grid_forget()
        self.date_label.grid(row=2, column=0, columnspan=3)
        self.back_btn.grid(row=4, column=0, columnspan=3)
        self.date_label.config(
            text=f"{self.timer_calculator.current_month.year} : {self.timer_calculator.current_month.month}"
        )
        self.next_month_btn.grid(row=1, column=2)
        self.previous_month_btn.grid(row=1, column=0)
        self.canvas.delete("all")
        self.label.config(text="Records", fg="#355764")
        x_position = 20
        y_position = 20
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # we add name of weekdays to tkinter canvas
        for i in range(7):
            self.create_circle(x=x_position, y=y_position, radius=20, text=week_days[i], color="#B2533E")
            x_position += 40
        y_position = 60
        board = MonthBoard(wanted_date=self.timer_calculator.current_month)
        board.make_month_matrix()
        record = ReportData()
        # we make a string for start day of this month from values
        start_date_string = (
            f"{self.timer_calculator.current_month.year}"
            f"-{self.timer_calculator.current_month.month}-01"
        )
        # we also make a string for end of this month
        end_date_string = (
            f"{self.timer_calculator.current_month.year}"
            f"-{self.timer_calculator.current_month.month}"
            f"-{board.current_month_days}"
        )
        this_month_records = record.get_month_records(
            start_date=self.timer_calculator.date_object_from_string(start_date_string),
            end_date=self.timer_calculator.date_object_from_string(end_date_string),
        )
        try:
            total_study_time_in_month = this_month_records[0]
            most_study_day = this_month_records[1].date.strftime("%Y %B %d")
            try:
                highest_study_weekday = self.timer_calculator.get_weekday_name(weekday=int(this_month_records[2][0]))
            except TypeError:
                highest_study_weekday = None
            report = (f"total focused minutes in month : {total_study_time_in_month}\n"
                      f"day with highest focus in month is : {most_study_day}\n"
                      f"You mostly focused weekday is : { highest_study_weekday}")
        except (AttributeError, TypeError):
            report = ("total focused minutes in month : 0\n"
                      "day with highest focus in month is : None\n"
                      "You mostly focused weekday is : None")

        self.report_label.config(text=report)
        self.report_label.grid(row=3, column=0, columnspan=3
                               )
        # this matrix is made with current month days
        matrix = board.month_matrix
        for row in matrix:
            x_position = 20
            for col in row:
                if col[0] == "x":
                    month_day = ""
                    color = YELLOW
                else:
                    month_day = col[1]
                    if col[0] == 1:
                        color = GREEN
                    else:
                        color = RED

                self.create_circle(x=x_position, y=y_position, radius=20, text=month_day, color=color)
                x_position += 40
            y_position += 40

    # Drawing Circle for each column in month matrix also write number of current month on it
    def create_circle(self, x, y, radius, text, color):
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

        self.canvas.create_text(x, y, text=text, fill="black")

    def next_record(self):
        self.timer_calculator.go_next_month()
        self.show_records()

    def previous_record(self):
        self.timer_calculator.go_previous_month()
        self.show_records()
