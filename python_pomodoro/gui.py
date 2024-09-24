import time
from enum import Enum
from tkinter import PhotoImage, StringVar, Tk, ttk

from .helpers import get_image_from_resources

"""
Handles all the user interface components like buttons, sliders,
task checklists, and component layouts
"""


class SessionStatus(Enum):
    FOCUS = {
        "title": "Focus",
        "default_time": [25, 00],
        "image": "tomato_red_bg.png",
        "image_paused": "tomato_red_dark_bg.png",
        "foreground": "#ffc9c9",
        "background": "#f55453",
        "foreground_paused": "#ec9291",
        "background_paused": "#d24847",
    }
    SHORT_BREAK = {
        "title": "Short Break",
        "default_time": [5, 0],
        "image": "tomato_yellow_bg.png",
        "image_paused": "tomato_yellow_dark_bg.png",
        "foreground": "#ffecc5",
        "background": "#f5c944",
        "foreground_paused": "#dcbf70",
        "background_paused": "#c5a237",
    }
    LONG_BREAK = {
        "title": "Long Break",
        "default_time": [15, 0],
        "image": "tomato_green_bg.png",
        "image_paused": "tomato_green_dark_bg.png",
        "foreground": "#c2f8c2",
        "background": "#76c776",
        "foreground_paused": "#87c387",
        "background_paused": "#5fa05f",
    }


class TomatoTimer(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk) -> None:
        ttk.Frame.__init__(self, parent)
        self.main_window = main_window

        self.is_paused = False
        self.minutes = StringVar()
        self.seconds = StringVar()

        # DEFAULT STATUS
        self.status = SessionStatus.FOCUS

        # APPEARANCE & STYLES
        self.bg_images = {
            status: PhotoImage(file=get_image_from_resources(str(status.value["image"]))) for status in SessionStatus
        }
        self.bg_images_paused = {
            status: PhotoImage(file=get_image_from_resources(str(status.value["image_paused"])))
            for status in SessionStatus
        }
        self.styles = ttk.Style(self)
        self.styles.configure("TimerImage.TLabel", font=("", 40, "bold"), justify="center")
        self.styles.configure(
            "TimerText.TLabel",
            font=("", 45, "bold"),
            justify="center",
        )
        self.styles.configure("OptionMenu.TMenubutton", width=16)

        # TIMER GUI COMPONENTS
        self.timer_background = ttk.Label(
            # contains background tomato image and colon seperator ie M:S
            self,
            text=":",
            image=self.bg_images[self.status],
            padding=15,
            compound="center",
            style="TimerImage.TLabel",
        )
        self.timer_background.grid(row=0, column=0, columnspan=2)

        timer_minutes = ttk.Label(self, textvariable=self.minutes, style="TimerText.TLabel")
        timer_minutes.grid(row=0, column=0, sticky="e", padx=10)

        timer_seconds = ttk.Label(self, textvariable=self.seconds, style="TimerText.TLabel")
        timer_seconds.grid(row=0, column=1, sticky="w", padx=10)

        self.button_reset = ttk.Button(self, text="Reset", command=self.reset_timer)
        self.button_reset.grid(row=1, column=0, sticky="e", padx=5)

        self.button_pause = ttk.Button(self, text="Pause", command=self.pause_timer)
        self.button_pause.grid(row=1, column=1, sticky="w", padx=5)

        self.button_start = ttk.Button(self, text="Start", command=self.start_timer)
        self.show_start_button()

        session_status_list = [str(status.value["title"]) for status in list(SessionStatus)]
        self.list_selection = StringVar()
        self.list_selection.set(session_status_list[0])
        self.option_menu_session_status = ttk.OptionMenu(
            self,
            self.list_selection,
            str(self.status.value["title"]),
            *session_status_list,
            command=lambda x: self.change_session_status(x),
            style="OptionMenu.TMenubutton",
            direction="above",
        )
        self.option_menu_session_status.grid(row=2, column=0, columnspan=2, pady=10)

        self.set_session_time()
        self.set_styles()

    def set_session_time(self) -> None:
        # set session time and pad with zeros
        mins = int(self.status.value["default_time"][0].__str__())
        secs = int(self.status.value["default_time"][1].__str__())
        self.minutes.set("{0:02}".format(mins))
        self.seconds.set("{0:02}".format(secs))
        self.current_time = int(self.minutes.get()) * 60 + int(self.seconds.get())

    def set_styles(self, reset: bool = False) -> None:
        if self.is_paused and reset is False:
            self.timer_background.configure(image=self.bg_images_paused[self.status])
        else:
            self.timer_background.configure(image=self.bg_images[self.status])

        paused = "_paused" if self.is_paused and reset is False else ""
        self.styles.configure("TimerImage.TLabel", foreground=self.status.value[f"foreground{paused}"])
        self.styles.configure(
            "TimerText.TLabel",
            background=self.status.value[f"background{paused}"],
            foreground=self.status.value[f"foreground{paused}"],
        )

    def show_start_button(self) -> None:
        self.button_start.grid(row=1, column=1, sticky="w", padx=5)

    def start_timer(self) -> None:
        self.is_paused = False  # restart timer
        self.button_start.grid_forget()
        self.set_styles()

        # TODO: change this to use  Tkinter.after() - update() and sleep() cause slight jitter when pressing pause
        # see https://stackoverflow.com/a/74361677
        while self.current_time > -1 and self.is_paused is not True:
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins, secs = divmod(self.current_time, 60)
            # set time and pad with zero
            self.minutes.set("{0:02}".format(mins))
            self.seconds.set("{0:02}".format(secs))
            # updating the GUI window after decrementing the timer 1 second
            self.main_window.title(
                f"Pomodoro - {self.status.value["title"]} - {self.minutes.get()}:{self.seconds.get()}"
            )
            self.main_window.update()
            time.sleep(1)
            self.current_time -= 1

        if self.current_time == -1:
            self.start_next_session()

    def pause_timer(self) -> None:
        self.is_paused = True
        self.main_window.title(f"{self.status.value["title"]} - Paused")
        self.show_start_button()
        self.set_styles()

    def reset_timer(self) -> None:
        self.is_paused = True
        self.show_start_button()
        self.set_session_time()
        self.set_styles(reset=True)
        self.main_window.title(f"Pomodoro - {self.status.value["title"]}")

    def start_next_session(self) -> None:
        self.status = (
            SessionStatus.SHORT_BREAK
        )  # TODO: Temporary status change while developing timer, need to automate this.
        self.main_window.title(f"Pomodoro - Start {self.status.value["title"]}")
        self.show_start_button()
        self.set_session_time()
        self.set_styles(reset=True)

    def change_session_status(self, status_var: StringVar) -> None:
        self.is_paused = True
        for status in list(SessionStatus):
            if status_var == status.value["title"]:
                self.status = status
        self.main_window.title(f"Pomodoro - Start {self.status.value["title"]}")
        self.show_start_button()
        self.set_session_time()
        self.set_styles(reset=True)


class TaskList(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Frame.__init__(self, parent)
        self.configure(border=1, borderwidth=1, relief="sunken", padding=10)

        label1 = ttk.Label(self, text="Tasks")
        label1.pack(side="top")

        self.task_list = ttk.Frame(self, padding=15)
        self.task_list.pack(side="top")

        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()

        button_add_task = ttk.Button(self, text="Add new task")
        button_add_task.pack(side="bottom")


class SettingSlider(ttk.Frame):
    def __init__(self, parent: ttk.Frame, label_text: str, min_value: int, max_value: int) -> None:
        ttk.Frame.__init__(self, parent)

        label1 = ttk.Label(self, text=label_text)
        label1.grid(row=0, column=0)

        slider = ttk.Scale(self, length=150, from_=min_value, to=max_value)
        slider.grid(row=1, column=0)
