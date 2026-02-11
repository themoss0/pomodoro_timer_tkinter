import tkinter as tk
from playsound3 import *

class Timer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        
        self.time_left = 25 * 60
        self.cycle_count = 0
        self.running = False
        self.mode = 'work'

        self._create_ui()
        self._update_timer()

    def _create_ui(self):
        self.timer_label = tk.Label(
            self,
            text='25:00',
            font=('Arial', 48)
        )
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(
            self,
            text='🍅 Помидорка',
            font=('Arial', 14)
        )
        self.status_label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, 
            text='Старт', 
            command=self.start, 
            bg='green', 
            fg='white', 
            width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame, 
            text='Пауза', 
            command=self.pause, 
            bg='orange', 
            fg='white', 
            width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame, 
            text='Ресет', 
            command=self.reset, 
            bg='red', 
            fg='white', 
            width=8).pack(side=tk.LEFT, padx=5)



    def _update_timer(self):
        if (self.running):

            if (self.time_left > 0):

                self.time_left -= 1
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.timer_label.config(text=f'{minutes:02d}:{seconds:02d}')

                if (self.time_left == 9 and self.mode=='idle'):
                    playsound(r'C:\\Users\\Admin\\Documents\\github\\pomodoro_timer_tkinter\\core\\data\\audio\\start_after_rest.mp3', block=False)

            elif (self.time_left == 0):
                print(self.mode)
                if (self.mode == 'work'):
                    self.mode = 'idle'
                    self.cycle_count+=1

                    playsound(r'C:\\Users\\Admin\\Documents\\github\\pomodoro_timer_tkinter\\core\\data\\audio\\interval_audio.mp3', block=False)
                    
                    if (self.cycle_count % 4 == 0 and self.cycle_count > 0):

                        self.time_left = 30 * 60
                        self.status_label.config(text=f"😴 Длительный перерыв! (цикл {self.cycle_count})", fg="purple")
                    else:

                        self.time_left = 5 * 60
                        self.status_label.config(text=f"😴 Отдыхай! (цикл {self.cycle_count})", fg="green")
                
                elif (self.mode == 'idle'):
                    self.mode = 'work'
                    self.time_left = 25 * 60
                    self.status_label.config(text="💪 Работай!", fg="red")
        
        self.after(1000, self._update_timer)


    def start(self):
        self.running = True

    def pause(self):
        self.running = False
        self.mode = 'paused'

    def reset(self):
        self.running = False
        self.time_left = 25 * 60
        self.mode = 'work'
        self.timer_label.config(text=f"{25:02d}:{00:02d}")
        self.cycle_count=0
        self.status_label.config(text="🍅 Помидорка", fg="black")

