import tkinter as tk
from tkinter import ttk

from gui import SettingSlider, TaskList, TomatoTimer

"""
Main entry point application.
It will initialize the Tkinter window, setup the app layout, and call the
necessary modules (e.g., GUI, timer, tasks)
"""


class Pomodoro:
    def __init__(self, main_window) -> None:
        main_window.title("Pomodoro")

        # Content frame
        container = ttk.Frame(main_window, padding=5, style="Container.TFrame")
        container.pack(side="top", fill="y", expand=True)

        timer = TomatoTimer(container)
        timer.grid(row=0, column=0)

        tasks = TaskList(container)
        tasks.grid(row=0, column=1)

        # Settings frame
        settings = ttk.Frame(main_window, padding=5, style="Settings.TFrame")
        settings.pack(side="top", fill="y", expand=False)

        setting_focus = SettingSlider(settings, "Focus time", 5, 25)
        setting_focus.grid(row=0, column=0)

        setting_cycles = SettingSlider(settings, "Cycles", 1, 10)
        setting_cycles.grid(row=0, column=1)

        setting_short_break = SettingSlider(settings, "Short Break", 1, 10)
        setting_short_break.grid(row=1, column=0)

        setting_long_break = SettingSlider(settings, "Long Break", 5, 45)
        setting_long_break.grid(row=1, column=1)

        settings_button = ttk.Button(settings, text="Settings")
        settings_button.grid(row=2, column=0, columnspan=2)


def main():
    root = tk.Tk()
    _ = Pomodoro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
