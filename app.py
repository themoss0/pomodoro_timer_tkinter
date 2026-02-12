
import tkinter as tk
import os
from os import sys

from model.timer import Timer
from viewmodel.timer_view_model import State, Time, TimerViewModel

class Config:
    WINDOW_SIZE='300x400'
    WINDOW_TITLE='Таймер-помидорка'

class Application:
    def __init__(self):
        self.app=tk.Tk()
        self.app.resizable(False, False)
        self._set_icon()

        self._setup_window()
        self._setup_timer()


    def _resource_path(self, relative_path):
        """Универсальный путь для .py и .exe"""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    
    def _set_icon(self):
        """Ставим иконку (работает и в .py, и в .exe)"""
        try:
            # Конвертируем .ico в .png заранее (один раз)
            # И кладём рядом с main.py
            icon_path = self._resource_path('pomidor.png')
            
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.app.iconphoto(True, icon)
                print(f"✅ Иконка загружена: {icon_path}")
            else:
                print(f"⚠️ Иконка не найдена: {icon_path}")
        except Exception as e:
            print(f"⚠️ Иконка не загружена: {e}")


    def _setup_window(self):
        self.app.title(Config.WINDOW_TITLE)
        self.app.geometry(Config.WINDOW_SIZE)

    def _setup_timer(self):
        self.timer_widget = Timer(parent=self.app, timervm=TimerViewModel(default_state=State.IDLE, time_interval=Time.TIME_25_05_30))
        self.timer_widget.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def run(self):
        self.app.mainloop()