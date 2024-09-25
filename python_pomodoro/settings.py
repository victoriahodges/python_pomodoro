from tkinter import IntVar, Scale, Tk, ttk

from .tomato_timer import DEFAULT_CYCLES, SessionStatus, TomatoTimer

"""
Handles all the settings components like control sliders,
for sessions and cycles.
"""


class Settings(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk, timer: TomatoTimer, controller: ttk.Button) -> None:
        ttk.Frame.__init__(self, parent)
        self.main_window = main_window
        self.timer = timer
        self.button = controller

        self.setting_focus = SettingSlider(self, "Focus time", 5, 60, SessionStatus.FOCUS.value.default_time.minutes)
        self.setting_focus.grid(row=0, column=0, padx=15)

        self.setting_cycles = SettingSlider(self, "Cycles", 1, 10, DEFAULT_CYCLES)
        self.setting_cycles.grid(row=0, column=1, padx=15)

        self.setting_short_break = SettingSlider(
            self, "Short Break", 1, 10, SessionStatus.SHORT_BREAK.value.default_time.minutes
        )
        self.setting_short_break.grid(row=1, column=0, padx=15, pady=10)

        self.setting_long_break = SettingSlider(
            self, "Long Break", 5, 45, SessionStatus.LONG_BREAK.value.default_time.minutes
        )
        self.setting_long_break.grid(row=1, column=1, padx=15, pady=10)

        self.button_reset = ttk.Button(self, text="Reset", command=self.reset_defaults)
        self.button_reset.grid(row=2, column=0, sticky="e", padx=5)
        self.button_save = ttk.Button(self, text="Save", command=self.update_settings)
        self.button_save.grid(row=2, column=1, sticky="w", padx=5)

    def reset_defaults(self) -> None:
        self.setting_focus.set_slider_value(SessionStatus.FOCUS.value.default_time.minutes)
        self.setting_short_break.set_slider_value(SessionStatus.SHORT_BREAK.value.default_time.minutes)
        self.setting_long_break.set_slider_value(SessionStatus.LONG_BREAK.value.default_time.minutes)
        for s in list(SessionStatus):
            s.value.set_time_to_default()
        self.setting_cycles.set_slider_value(DEFAULT_CYCLES)

    def update_settings(self) -> None:
        focus_minutes = self.setting_focus.get_slider_value()
        SessionStatus.FOCUS.value.set_time(focus_minutes)

        short_break_minutes = self.setting_short_break.get_slider_value()
        SessionStatus.SHORT_BREAK.value.set_time(short_break_minutes)

        long_break_minutes = self.setting_long_break.get_slider_value()
        SessionStatus.LONG_BREAK.value.set_time(long_break_minutes)

        cycles = self.setting_cycles.get_slider_value()
        self.timer.set_cycles(cycles)

        self.timer.set_status(SessionStatus.FOCUS)
        self.timer.reset_timer()

        # hide settings after saving
        self.pack_forget()
        self.button.pack(side="bottom", fill="x")
        self.resize_window()

    def resize_window(self) -> None:
        self.main_window.minsize(600, 538)
        self.main_window.maxsize(600, 538)


class SettingSlider(ttk.Frame):
    def __init__(self, parent: ttk.Frame, label_text: str, min_value: int, max_value: int, default_value: int) -> None:
        ttk.Frame.__init__(self, parent)
        self.value = IntVar()

        self.value.set(default_value)

        self.slider_name_label = ttk.Label(self, text=label_text)
        self.slider_name_label.grid(row=1, column=0, pady=3)

        self.slider = Scale(
            self,
            variable=self.value,
            length=200,
            from_=min_value,
            to=max_value,
            orient="horizontal",
        )
        self.slider.grid(row=0, column=0)

    def set_slider_value(self, value: int) -> None:
        self.value.set(value)

    def get_slider_value(self) -> int:
        return self.value.get()
