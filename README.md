# 🍅 Pomidoro Timer

<div align="center">

![Pomidoro Logo](https://github.com/user-attachments/assets/e9d992a2-87d9-4130-bb39-8ae0dd43952d)

**A beautiful and functional Pomodoro timer with themes, multiple languages, and customizable presets.**

[![Release](https://img.shields.io/github/v/release/themoss0/pomidoro_timer_tkinter?color=ff6b8b&label=Download&style=for-the-badge)](https://github.com/themoss0/pomidoro_timer_tkinter/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-ff69b4?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)

</div>

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 🎨 | **3 Beautiful Themes** | Light, Dark, and Rose themes for any mood |
| 🌐 | **Multilingual** | English and Russian interfaces |
| ⏱️ | **Multiple Presets** | 25/5/30, 30/5/30, 60/10/60, 180/30/60 + DEBUG mode |
| 🔊 | **Sound Notifications** | Audio alerts for interval completion and warnings |
| 📊 | **Cycle Counter** | Tracks your progress with 4/4 cycle display |
| 🎯 | **Long Break** | Automatic 30-min long break after 4 cycles |
| ⏸️ | **Pause/Resume** | Full control over your timer |
| 🖼️ | **Custom Icon** | Beautiful tomato icon for the app and executable |

---

## 🖼️ Screenshots

<div align="center">

### Light Theme
<img width="298" alt="Light Theme" src="https://github.com/user-attachments/assets/2e018aab-48f4-4412-808b-3be18890547c" >




### Dark Theme
<img width="298" alt="Dark Theme" src="https://github.com/user-attachments/assets/be308e87-ab15-4e52-a6a4-4cd4c13120cf">




### Rose Theme (💝 Valentine Special)
<img width="298" alt="Rose Theme" src="https://github.com/user-attachments/assets/07ac4f11-878e-4a15-9a7d-fe1dd859b933">

</div>

---

## 📦 Installation

### Option 1: Download Executable (Recommended)

1. Go to **[Releases](https://github.com/themoss0/pomidoro/releases/latest)** page
2. Download `PomidoroTimer_v.1.0.0.exe`
3. Run the file (Windows may show a SmartScreen warning - click "More info" → "Run anyway")

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/themoss0/pomidoro.git
cd pomidoro

# Install dependencies
pip install playsound3

# Run the application
python main.py
```

## 🎮 How to Use

  1. Start - Begin a 25-minute work session

  2. Pause - Temporarily stop the timer

  3. Reset - Reset to initial state

  4. Presets - Choose different time intervals from the menu

  5. Themes - Switch between Light, Dark, and Rose themes

  6. Language - Toggle between English and Russian

## Pomodoro Cycle:

   🔴 Work - 25 minutes (customizable)

   🟢 Short Break - 5 minutes

   🔄 After 4 work sessions → 🟣 Long Break - 30 minutes


## 🛠️ Technical Details

  - Language: Python 3.8+

  - GUI Framework: Tkinter

  - Architecture: MVVM (Model-View-ViewModel)

  - Sound: playsound3 library

  - Build Tool: PyInstaller

## Project Structure
```
pomidoro_timer_tkinter/
├── main.py                 # Entry point
├── app.py                  # Application class
├── model/                  # Business logic
│   ├── timer.py
│   ├── localization.py
│   └── theme_manager.py
├── viewmodel/              # ViewModel layer
│   └── timer_view_model.py
├── widgets/                # UI components
│   └── menu_widget.py
├── sound_manager.py        # Sound handling
├── core/data/audio/        # Sound files
└── pomidor.png/ico         # App icon
```


<div align="center">

**⭐ If you like this project, please star it on GitHub! ⭐**

</div> 
