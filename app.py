
import tkinter as tk
import os

from model.timer import Timer

class Config:
    WINDOW_SIZE='300x400'
    WINDOW_TITLE='Таймер-помидорка'

class Application:
    def __init__(self):
        self.app=tk.Tk()
        
        self.icon_path = os.path.join(os.path.dirname(__file__), 'pomidor.ico')
        self.app.iconbitmap(self.icon_path)

        self._setup_window()
        self._setup_timer()

    def _setup_window(self):
        self.app.title(Config.WINDOW_TITLE)
        self.app.geometry(Config.WINDOW_SIZE)

    def _setup_timer(self):
        self.timer_widget = Timer(parent=self.app)
        self.timer_widget.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def run(self):
        self.app.mainloop()