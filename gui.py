import customtkinter as ctk
from PIL import ImageTk, Image
from app.generator import create_designer_qr

class QRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройки окна премиального уровня
        self.title("QR Builder Automation PRO")
        self.geometry("500x740")
        self.resizable(False, False)
        
        # Палитра для QR-кода со значками
        self.qr_colors_dict = {
            "🟣 Фиолетовый неон": (138, 43, 226),
            "🌸 Розовая сакура": (255, 20, 147),
            "🟢 Кислотный зеленый": (50, 205, 50),
            "🔥 Огненный оранжевый": (255, 69, 0),
            "🔵 Глубокий синий": (0, 191, 255),
            "⚫️ Угольный черный": (20, 20, 20)
        }
        
        self.setup_ui()

    def setup_ui(self):
        # --- ВЕРХНЯЯ ДИЗАЙНЕРСКАЯ ПАНЕЛЬ ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#0F0F12", height=90, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.label_title = ctk.CTkLabel(
            self.header_frame, 
            text="✨ QR AUTOMATION STUDIO", 
            font=("Segoe UI", 22, "bold"),
            text_color="#00BFFF"
        )
        self.label_title.pack(pady=(22, 2))
        
        self.label_subtitle = ctk.CTkLabel(
            self.header_frame, 
            text="PRO EDITION // CORE v2.6", 
            font=("Consolas", 10),
            text_color="#44444C"
        )
        self.label_subtitle.pack()

        # --- ГЛАВНЫЙ КОНТЕНТ-ФРЕЙМ ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(pady=20, padx=30, fill="both", expand=True)

        # Поле ввода URL
        self.label_input = ctk.CTkLabel(
            self.main_content, 
            text="ЦЕЛЕВАЯ ССЫЛКА (URL-АДРЕС)", 
            font=("Segoe UI", 11, "bold"),
            text_color="#888899"
        )
        self.label_input.pack(anchor="w", padx=5, pady=(5, 5))
        
        self.input_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.input_container.pack(fill="x", pady=0)
        
        self.entry_text = ctk.CTkEntry(
            self.input_container, 
            width=380, 
            height=42,
            placeholder_text="https://ya.ru",
            font=("Segoe UI", 14),
            border_color="#27272A",
            fg_color="#18181B",
            text_color="#FFFFFF"
        )
        self.entry_text.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_text.bind("<KeyRelease>", self.live_validator)
        
        # Живая кнопка очистки текста с анимацией нажатия
        self.btn_clear = ctk.CTkButton(
            self.input_container, 
            text="✕", 
            width=42, 
            height=42, 
            fg_color="#18181B", 
            hover_color="#EF4444",
            border_color="#27272A",
            border_width=1,
            font=("Segoe UI", 14, "bold"),
            command=self.clear_input
        )
        self.btn_clear.pack(side="right")
        
        # Индикатор валидации ссылки (Неоновый прогресс-бар)
        self.val_bar = ctk.CTkProgressBar(
            self.main_content, 
            width=440, 
            height=4, 
            fg_color="#18181B", 
            progress_color="#3B82F6"
        )
        self.val_bar.set(0)
        self.val_bar.pack(pady=(8, 2))
        
        # Информационная строка под полем ввода
        self.char_counter = ctk.CTkLabel(
            self.main_content, 
            text="Ожидание ввода корректного URL-адреса...", 
            font=("Segoe UI", 11), 
            text_color="#71717A"
        )
        self.char_counter.pack(anchor="w", padx=5, pady=(0, 15))
        
        # Блок настроек цвета
        self.settings_frame = ctk.CTkFrame(self.main_content, fg_color="#18181B", border_color="#27272A", border_width=1, corner_radius=12, height=65)
        self.settings_frame.pack_propagate(False)
        self.settings_frame.pack(fill="x", pady=10)
        
        self.lbl_qr_col = ctk.CTkLabel(self.settings_frame, text="СТИЛЬ И КВАНТОВЫЙ ЦВЕТ КOДА:", font=("Segoe UI", 11, "bold"), text_color="#A1A1AA")
        self.lbl_qr_col.place(x=15, y=24)
        
        self.qr_color_picker = ctk.CTkOptionMenu(
            self.settings_frame, 
            values=list(self.qr_colors_dict.keys()),
            width=190,
            height=35,
            fg_color="#09090B",
            button_color="#27272A",
            button_hover_color="#3F3F46",
            dropdown_fg_color="#09090B",
            dropdown_hover_color="#18181B",
            font=("Segoe UI", 12)
        )
        self.qr_color_picker.place(x=230, y=15)
        
        # --- ВЫДЕЛЯЮЩАЯСЯ ОБЪЕМНАЯ КНОПКА ГЕНЕРАЦИИ С ТАКТИЛЬНЫМ ОТКЛИКОМ ---
        self.btn_generate = ctk.CTkButton(
            self.main_content, 
            text="⚡  СФОРМИРОВАТЬ ДИЗАЙНЕРСКИЙ QR-КОД  ⚡", 
            font=("Segoe UI", 13, "bold"),
            height=54,
            fg_color="#00BFFF",
            hover_color="#009ACD",
            text_color="#000000",
            corner_radius=10,
            border_width=2,
            border_color="#BFEFFF",
            command=self.generate_qr
        )
        self.btn_generate.pack(fill="x", pady=20)
        
        # Секция интерактивного предпросмотра (УБРАНА ЧЕРНАЯ СИСТЕМНАЯ РАМКА)
        self.qr_preview_container = ctk.CTkFrame(
            self.main_content, 
            width=230, 
            height=230, 
            fg_color="transparent",  # Прозрачный фон скрывает любые жесткие границы
            corner_radius=16
        )
        self.qr_preview_container.pack_propagate(False)
        self.qr_preview_container.pack(pady=5)
        
        self.preview_placeholder = ctk.CTkLabel(
            self.qr_preview_container, 
            text="СИСТЕМА ГОТОВА\nК КВАНТОВОЙ СБОРКЕ", 
            font=("Consolas", 12, "bold"),
            text_color="#27272A"
        )
        self.preview_placeholder.pack(expand=True)
        
        # --- НИЖНИЙ СТАТУС-БАР ---
        self.status_frame = ctk.CTkFrame(self, fg_color="#0F0F12", height=45, corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="🟢 Модули инициализированы. Ошибок нет.", 
            font=("Segoe UI", 11, "bold"), 
            text_color="#52525B"
        )
        self.status_label.pack(pady=12, fill="x")

    # ЖИВАЯ ФУНКЦИЯ: Интеллектуальный анализатор ссылки
    def live_validator(self, event):
        text = self.entry_text.get().strip()
        length = len(text)
        
        if length == 0:
            self.char_counter.configure(text="Ожидание ввода корректного URL-адреса...", text_color="#71717A")
            self.val_bar.set(0)
            self.val_bar.configure(progress_color="#3B82F6")
            self.entry_text.configure(border_color="#27272A")
        elif text.startswith("http://") or text.startswith("https://"):
            self.char_counter.configure(text=f"Ссылка полностью валидна ({length} симв.). Матрица стабильна. 🟢", text_color="#10B981")
            self.val_bar.set(1.0)
            self.val_bar.configure(progress_color="#10B981")
            self.entry_text.configure(border_color="#10B981")
        else:
            self.char_counter.configure(text=f"Внимание: Неверный сетевой протокол ({length} симв.) 🔴", text_color="#EF4444")
            self.val_bar.set(0.35)
            self.val_bar.configure(progress_color="#EF4444")
            self.entry_text.configure(border_color="#EF4444")

    # ЖИВАЯ ФУНКЦИЯ: Сброс полей
    def clear_input(self):
        self.entry_text.delete(0, 'end')
        self.char_counter.configure(text="Ожидание ввода корректного URL-адреса...", text_color="#71717A")
        self.val_bar.set(0)
        self.val_bar.configure(progress_color="#3B82F6")
        self.entry_text.configure(border_color="#27272A")
        self.status_label.configure(text="🟢 Поле ввода успешно очищено", text_color="#52525B")

    def generate_qr(self):
        text_data = self.entry_text.get().strip()
        selected_qr_color = self.qr_color_picker.get()
        rgb_color = self.qr_colors_dict[selected_qr_color]
        
        if not text_data:
            self.status_label.configure(text="❌ КРИТИЧЕСКАЯ ОШИБКА: Поле ввода пустое!", text_color="#EF4444")
            return
            
        if not (text_data.startswith("http://") or text_data.startswith("https://")):
            self.status_label.configure(text="❌ КРИТИЧЕСКАЯ ОШИБКА: Задайте верный сетевой формат!", text_color="#EF4444")
            return
        
        self.status_label.configure(text="🛸 Запуск квантового рендеринга матрицы кода...", text_color="#00BFFF")
        self.update() # Обновляем окно, чтобы текст успел показаться
        
        try:
            img, safe_name = create_designer_qr(text_data, rgb_color)
            
            preview_img = img.resize((210, 210))
            ctk_image = ImageTk.PhotoImage(preview_img)
            
            for child in self.qr_preview_container.winfo_children():
                child.destroy()
                
            img_label = ctk.CTkLabel(self.qr_preview_container, image=ctk_image, text="")
            img_label.image = ctk_image
            img_label.pack(expand=True)
            
            self.status_label.configure(
                text=f"✅ УСПЕХ: {safe_name}.png экспортирован в QR_Outputs!", 
                text_color="#10B981"
            )
        except Exception as e:
            self.status_label.configure(text=f"💥 СБОЙ ЯДРА: {str(e)}", text_color="#EF4444")
