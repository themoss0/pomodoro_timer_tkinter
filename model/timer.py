import tkinter as tk
import os
import sys
from tkinter import messagebox

from playsound3 import playsound

from model.localization import Localization
from model.theme_manager import ThemeManager
from sound_manager import get_sound_manager
from viewmodel.timer_view_model import State, Time, TimerViewModel

class Timer(tk.Frame):
    def __init__(self, parent, timervm, theme_manager, localization):
        super().__init__(parent)

        self.parent = parent
        self.timervm: TimerViewModel = timervm
        self.theme_manager: ThemeManager = theme_manager
        self.localization: Localization = localization

        self.time = timervm.get_seconds_of_time()
        self.time_work_seconds = self.time[0]
        self.time_rest_seconds = self.time[1]
        self.time_long_rest_seconds = self.time[2]

        self.is_sound_played = False
        self.sound = get_sound_manager()

        self._create_ui()
        
        self.master.update_idletasks()
        self.master.update()
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
            text=self.localization.get('pomidoro'),
            font=('Arial', 14)
        )
        self.status_label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_button: tk.Button = tk.Button(
            btn_frame, 
            text=self.localization.get('start_btn'), 
            command=self.start, 
            bg=self.theme_manager.get('start_bg'), 
            fg=self.theme_manager.get('start_fg'), 
            width=8)
        self.pause_button: tk.Button = tk.Button(
            btn_frame, 
            text=self.localization.get('pause_btn'), 
            command=self.pause, 
            bg=self.theme_manager.get('pause_bg'), 
            fg=self.theme_manager.get('pause_fg'), 
            width=8)
        self.reset_button: tk.Button = tk.Button(
            btn_frame, 
            text=self.localization.get('reset_btn'), 
            command=self.reset, 
            bg=self.theme_manager.get('reset_bg'), 
            fg=self.theme_manager.get('reset_fg'), 
            width=8)
        
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)



    def _update_timer(self):

        is_running: bool = self.timervm.get_running_mode()

        if (is_running):
            #======== WORK ========
            if (self.timervm.state == State.WORK):
                self.status_label.config(text=f"{self.localization.get('work')} {self.timervm.cycle_count+1}/4", fg=self._get_status_color())
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
                self.status_label.config(text=f"{self.localization.get('rest')} {self.timervm.cycle_count+1}/4", fg=self._get_status_color())
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
                self.status_label.config(text=f"{self.localization.get('long_rest')} 4/4", fg=self._get_status_color())
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
                self.status_label.config(text=f"{self.localization.get('paused')}", fg=self._get_status_color())
            #print('ТАЙМЕР НЕ РАБОТАЕТ!')

        self.after(1000, self._update_timer)

    def _apply_preset(self):
        self.time = self.timervm.get_seconds_of_time()

        if (self.timervm.state in (State.IDLE, State.PAUSED)):
            self._reset_time_values()
            self.timervm.state = State.IDLE
        else:
            pass

    def change_preset(self, preset: Time):
        """Смена пресета времени"""
        if (self.timervm.state not in (State.IDLE, State.PAUSED)):
           self._show_warning("Смена пресета доступна только на паузе или в режиме ожидания")
           return
            
        self.timervm.set_time_preset(preset)
        self._apply_preset()

        self._show_info(f"Пресет изменён на {preset.name}")

    def change_theme(self, theme_name: str):
        if (self.theme_manager):
            print(f"\n🎨 Смена темы на {theme_name}")
            self.theme_manager.apply_theme(widget=self.master, theme_name=theme_name, source='change_theme')
            self.master.update()

            self.start_button.config(bg=self.theme_manager.get('start_bg'), fg=self.theme_manager.get('start_fg'))
            self.pause_button.config(bg=self.theme_manager.get('pause_bg'), fg=self.theme_manager.get('pause_fg'))
            self.reset_button.config(bg=self.theme_manager.get('reset_bg'), fg=self.theme_manager.get('reset_fg'))

            status_color = self._get_status_color()
            print(f"🎨 Статус цвет: {status_color}")
            self.status_label.config(fg=status_color)

            self.master.update_idletasks()  # Обновить макет
            self.master.update() 

            print(f"✅ Тема {theme_name} применена\n")

    def change_language(self, lang_code: str):
        if (self.localization):
            self.localization.set_language(lang_code)
            self._update_language()

            if hasattr(self.master, 'menu'):
                self.master.menu.update_language()

    def _get_status_color(self):
        """Получение цвета для текущего состояния из темы"""
        #print(f'текущая тема: {self.theme_manager.current_theme}')
        if (not self.theme_manager):
            colors_default = {
                State.WORK: 'red',
                State.REST: 'green',
                State.LONG_REST: 'purple',
                State.PAUSED: 'black',
                State.IDLE: 'black'
            }
            return colors_default.get(self.timervm.state, 'black')
        
        theme = self.theme_manager.THEMES[self.theme_manager.current_theme]

        color_map = {
            State.WORK: 'status_work',
            State.REST: 'status_rest',
            State.LONG_REST: 'status_long_rest',
            State.PAUSED: 'status_paused',
            State.IDLE: 'status_idle', 
        }

        color_key = color_map.get(self.timervm.state, 'fg')
        return theme.get(color_key, theme['fg'])


    def set_theme_manager(self, theme_manager: ThemeManager):
        """Отвечает за установку менеджера тем"""
        self.theme_manager = theme_manager
        

    def set_localization(self, localization: Localization):
        """Отвечает за установку локализации"""
        self.localization = localization

    def _update_language(self):
        """Обновление текстов при смене языка"""
        if not self.localization:
            return
        
        self.start_button.config(text=self.localization.get('start_btn'))
        self.pause_button.config(text=self.localization.get('pause_btn'))
        self.reset_button.config(text=self.localization.get('reset_btn'))

        self.status_label.config(text=self._get_status_text())

        self.master.title(self.localization.get('app_title'))

    def _show_warning(self, message: str):
        messagebox.showwarning(title="Внимание", message=message)    

    def _show_info(self, message: str):
        messagebox.showinfo(title="Внимание", message=message)  

    def reset_timer_for_state(self, state: State) -> None:
        current_times = self.timervm.get_seconds_of_time()
    
        if (state == State.WORK):
            self.time_work_seconds = current_times[0]
        elif (state == State.REST):
            self.time_rest_seconds = current_times[1]
        elif (state == State.LONG_REST):
            self.time_long_rest_seconds = current_times[2]

    def _get_status_text(self) -> str:
        if not self.localization:
            return 
        state = self.timervm.state
        if (state == State.WORK):
            return self.localization.get('work') + f"{self.timervm.cycle_count+1}/4"
        elif (state == State.REST):
            return self.localization.get('rest')+ f"{self.timervm.cycle_count}/4"
        elif (state == State.LONG_REST):
            return self.localization.get('long_rest')+ " 4/4 ✅"
        elif (state == State.PAUSED):
            return self.localization.get('paused')
        elif (state == State.IDLE):
            return self.localization.get('pomidoro')

        
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
        print(f'ВРЕМЯ: {self.time}')
        self.status_label.config(text=self.localization.get('pomidoro'), fg=self._get_status_color())       


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
        

