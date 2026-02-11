import tkinter as tk
import os
import sys

from playsound3 import playsound


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Timer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        
        self.time_left = 25 * 60
        self.cycle_count = 0
        self.running = False
        self.mode = 'idle'
        self.mode_before = 'idle'

        self.is_rest = False

        self.is_warning_sound_played = False

        self.audio_interval = resource_path('data/audio/interval_audio.mp3')
        self.audio_warning = resource_path('data/audio/start_after_rest.mp3')

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

            if (self.time_left <= 9 and self.is_warning_sound_played == False and self.mode=='rest'):
                    playsound(r'C:\\Users\\Admin\\Documents\\github\\pomodoro_timer_tkinter\\core\\data\\audio\\start_after_rest.mp3', block=False)
                    self.is_warning_sound_played = True
                    print(f'Песенка отыграла. {self.mode=}')
                    pass
                    
            elif (self.time_left == 0):
                print(f'Время вышло! Состояние: {self.mode}.')
                self.is_warning_sound_played = False
                if (self.mode == 'work'):
                    print(f'Состояние на момент завершения времени: {self.mode}. Ставится rest...')
                    self.mode = 'rest'
                    self.mode_before = self.mode
                    self.is_rest = True
                    print(f'Изменение состояния: {self.mode}.')
                    print('--------------------------------')

                    self.cycle_count+=1
                    try:
                        playsound(r'C:\\Users\\Admin\\Documents\\github\\pomodoro_timer_tkinter\\core\\data\\audio\\interval_audio.mp3', block=False)
                        print('Песня окончания отыграла!')
                    except:
                        print('Ошибка! Не удалось отыграть песню окончания рабочего времени!')
                        pass
                    if (self.cycle_count % 4 == 0 and self.cycle_count > 0):
                        print('Прошла 4 25-ти минутка. Длительный перерыв')
                        print('--------------------------------')

                        self.time_left = 30 * 60
                        self.status_label.config(text=f"😴 Длительный перерыв! (цикл {self.cycle_count})", fg="purple")
                        self.cycle_count = 0
                    else:
                        print('Обычный интервал. Отдых...')
                        print('--------------------------------')
                        self.time_left = 5 * 60
                        self.status_label.config(text=f"😴 Отдыхай! (цикл {self.cycle_count})", fg="green")
                
                elif (self.mode == 'rest'):
                    print(f'Состояние на момент завершения времени: {self.mode}. Ставится work...')
                    self.time_left = 25 * 60
                    self.mode = 'work'
                    self.mode_before = self.mode
                    self.is_rest = False
                    print(f'Изменение состояния: {self.mode}.')
                    print('--------------------------------')
                    self.status_label.config(text="💪 Работай!", fg="red")
        
        self.after(1000, self._update_timer)


    def start(self):
        print('Нажат start:')
        print(f'Состояние до нажатия: {self.mode_before}.')
        self.running = True
        if (self.mode_before == 'idle'):
            self.mode = 'work'
            self.mode_before = self.mode
            self.status_label.config(text="💪 Работай!", fg="red")
        if (self.mode_before == 'paused'):
            if (self.is_rest):
                self.mode = 'rest'
                self.mode_before = self.mode
                self.status_label.config(text=f'😴 Отдыхай! (цикл {self.cycle_count})', fg='green')
            else:
                self.mode = 'work'
                self.mode_before = self.mode
                self.status_label.config(text="💪 Работай!", fg="red")
        print(f'Состояние после нажатия: {self.mode}, {self.is_rest=}.')
        print('--------------------------------')
        

    def pause(self):
        print('Нажат pause:')
        print(f'Состояние до нажатия: {self.mode_before}.')
        self.running = False
        self.mode = 'paused'
        self.mode_before = self.mode
        self.status_label.config(text=f"⏸️ Пауза", fg="black")
        print(f'Состояние после нажатия: {self.mode}, {self.is_rest=}.')
        print('--------------------------------')

    def reset(self):
        print('Нажат reset:')
        print(f'Состояние до нажатия: {self.mode_before}.')
        self.running = False
        self.is_rest = False
        self.time_left = 25 * 60
        self.mode = 'idle'
        self.mode_before = self.mode
        self.timer_label.config(text=f"{25:02d}:{00:02d}")
        self.cycle_count=0
        self.is_warning_sound_played = False
        self.status_label.config(text="🍅 Помидорка", fg="black")
        print(f'Состояние после нажатия: {self.mode}, {self.is_rest=}.')
        print('--------------------------------')

