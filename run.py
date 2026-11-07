import os
import sys
import customtkinter as ctk

# Автоматически добавляем текущую директорию в пути поиска модулей Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui import QRApp

# Глобальные настройки внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = QRApp()
    app.mainloop()
