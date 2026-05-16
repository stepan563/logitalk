from customtkinter import *
from PIL import Image
from chat import MainWindow
import os


class AuthWindow(CTk):
    def __init__(self):
        super().__init__()

        self.title("Вхід")
        self.geometry("700x400")
        self.resizable(False, False)

        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side="left", fill="both")

        # Отримуємо шлях до директорії скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(script_dir, "завантаження.png")
        
        ctk_img = CTkImage(Image.open(bg_path), size=(450, 400))
        self.img_label = CTkLabel(
            self.left_frame,
            image=ctk_img,
            text="Salut",
            font=("Helvetica", 60, "bold"),
            text_color="#48ff00"
        )
        self.img_label.pack()

        main_font = ("Helvetica", 20, "bold")
        self.right_frame = CTkFrame(self, fg_color="white")
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side="right", fill="both", expand="True")

        CTkLabel(
            self.right_frame, text="LogiTalk", font=main_font, text_color="#6753cc"
        ).pack(pady=60)

        self.name_entry = CTkEntry(
            self.right_frame,
            placeholder_text="ім'я",
            height=45,
            font=main_font,
            corner_radius=25,
            fg_color="#FF85BB",
            border_color="#021A54",
            text_color="#FFCEE3",
            placeholder_text_color="#F5F5F5",
        )
        self.name_entry.pack(fill="x", padx=10, pady=5)


        self.server_entry = CTkEntry(
            self.right_frame,
            placeholder_text="Сервер",
            placeholder_text_color="#03AED2",
            height=45,
            corner_radius=25,
            fg_color="#F8DE22",
            border_color="#F45B26",
            font=main_font,
            text_color="#D12052"
            )
        self.server_entry.pack(fill="x", padx=10)

        self.port_entry = CTkEntry(
            self.right_frame,
            placeholder_text="Порт",
            placeholder_text_color="#ff00f2",
            height=45,
            corner_radius=25,
            fg_color="#3468ac",
            border_color="#00bef8",
            font=main_font,
            text_color="#ff0ff3"
        )
        self.port_entry.pack(fill="x", padx=10, pady=5)


        self.connect_button = CTkButton(
            self.right_frame,
            text="УВІЙТИ",
            height=45,
            corner_radius=25,
            fg_color="#230f94",
            font=main_font,
            text_color="white",
            command=self.connect
        
        )
        self.connect_button.pack(fill="x", padx=50, pady=10)

    def connect(self):
        username = self.name_entry.get()
        server = self.server_entry.get()
        port = self.port_entry.get()
        if not username or not server or not port:
            CTkLabel(
                self.right_frame,
                text='Всі поля повинні бути заповненні',
                text_color='yellow',
                font=('Helvetica', 12, 'bold')
            ).pack()
            return
        self.destroy()
        window = MainWindow(username, server, port)
        window.mainloop()

window = AuthWindow()
window.mainloop()
