import tkinter as tk
import os
import sys

from playsound3 import playsound

from sound_manager import get_sound_manager
from viewmodel.timer_view_model import State

class Timer(tk.Frame):
    def __init__(self, parent, timervm):
        super().__init__(parent)

        self.parent = parent
        self.timervm = timervm
        self.time = timervm.get_seconds_of_time()
        self.time_work_seconds = self.time[0]
        self.time_rest_seconds = self.time[1]
        self.time_long_rest_seconds = self.time[2]

        self.is_sound_played = False
        self.sound = get_sound_manager()

        self._create_ui()
        self._update_timer()

    def _create_ui(self):
        self.timer_label = tk.Label(
            self,
            text=f'{self.time[0]//60:02d}:{self.time[0]%60:02d}',
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

        is_running: bool = self.timervm.get_running_mode()

        if (is_running):
            #======== WORK ========
            if (self.timervm.state == State.WORK):
                self.status_label.config(text=f"💪 Работай! {self.timervm.cycle_count+1}/4", fg="red")
                if (self.time_work_seconds > 0):
                    self.time_work_seconds -= 1
                    minutes = self.time_work_seconds // 60
                    seconds = self.time_work_seconds % 60
                    self.timer_label.config(text=f'{minutes:02d}:{seconds:02d}')

                    if (self.time_work_seconds == 0):
                        self.timervm.cycle_count += 1
                        self.sound.play_async('interval')
                        self.is_sound_played = False

                        if (self.timervm.cycle_count % 4 == 0 and self.timervm.cycle_count > 0):
                            self.reset_timer_for_state(State.LONG_REST)
                            self.timervm.set_long_rest_configuration()
                        else:
                            self.reset_timer_for_state(State.REST)
                            self.timervm.set_rest_configuration()
            #======== REST ========
            elif (self.timervm.state == State.REST):
                self.status_label.config(text=f"😴 Отдыхай! {self.timervm.cycle_count}/4", fg="green")
                #print('===REST===')
                if (self.time_rest_seconds > 0):
                    self.time_rest_seconds -= 1
                    minutes = self.time_rest_seconds // 60
                    seconds = self.time_rest_seconds % 60
                    self.timer_label.config(text=f'{minutes:02d}:{seconds:02d}')

                    if (self.time_rest_seconds <= 9 and self.time_rest_seconds > 0):
                        if not(self.is_sound_played):
                            self.sound.play_async('warning')
                            self.is_sound_played = True
                    else:
                        self.is_sound_played = False

                    if (self.time_rest_seconds == 0):
                        self.is_sound_played = False
                        self.reset_timer_for_state(State.WORK)
                        self.timervm.set_work_configuration()
            #======== LONG_REST ========
            elif (self.timervm.state == State.LONG_REST):
                self.status_label.config(text=f"🎉 Длинный перерыв! 4/4 ✅", fg="purple")
                if (self.time_long_rest_seconds > 0):
                    self.time_long_rest_seconds -=1
                    minutes = self.time_long_rest_seconds // 60
                    seconds = self.time_long_rest_seconds % 60
                    self.timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
                    if (self.time_long_rest_seconds <= 9 and self.time_long_rest_seconds > 0):
                        if not(self.is_sound_played):
                            self.sound.play_async('warning')
                            self.is_sound_played = True
                    else:
                        self.is_sound_played = False
                    if (self.time_long_rest_seconds == 0):
                        self.is_sound_played = False
                        self.reset_timer_for_state(State.WORK)
                        self.timervm.set_work_configuration()

        else:
            if (self.timervm.state == State.PAUSED):
                self.status_label.config(text=f"⏸️ Пауза", fg="black")
            #print('ТАЙМЕР НЕ РАБОТАЕТ!')

        self.after(1000, self._update_timer)


    def reset_timer_for_state(self, state: State) -> None:
        current_times = self.timervm.get_seconds_of_time()
    
        if (state == State.WORK):
            self.time_work_seconds = current_times[0]
        elif (state == State.REST):
            self.time_rest_seconds = current_times[1]
        elif (state == State.LONG_REST):
            self.time_long_rest_seconds = current_times[2]


        
    def check_state(self):
        state = self.timervm.state
        current_time = self.timervm.get_seconds_of_time()
        if state == State.IDLE:
            self.timervm.set_state(State.WORK)
            self.timervm.set_is_rest_mode(False) 
        elif state == State.PAUSED:
            if (self.timervm.is_rest):
                self.timervm.set_state(State.REST)
                self.timervm.set_is_rest_mode(True)
            else:
                self.timervm.set_state(State.WORK)
                self.timervm.set_is_rest_mode(False)


    def _reset_time_values(self) -> None:
        """Полный сброс всех временных значений"""
        self.time = self.timervm.get_seconds_of_time()
        self.time_work_seconds = self.time[0]
        self.time_rest_seconds = self.time[1]
        self.time_long_rest_seconds = self.time[2]
        self.timer_label.config(text=f'{self.time[0]//60:02d}:{self.time[0]%60:02d}') 
        self.status_label.config(text="🍅 Помидорка", fg="black")       


    def start(self) -> None:
        #print('===START===')
        self.timervm.set_running_mode(mode=True)
        self.check_state()

        

    def pause(self) -> None:
        if (self.timervm.state == State.WORK or self.timervm.state == State.REST or self.timervm.state == State.LONG_REST):
            self.timervm.set_paused_configuration()
            self.is_sound_played = False

    def reset(self) -> None:
        self.timervm.set_reset_configuration()
        self._reset_time_values()
        self.is_sound_played = False
        

