from customtkinter import *
from PIL import Image
import threading, socket, base64, io
from tkinter import filedialog


class MainWindow(CTk):
    def __init__(self, username, server, port):
        super().__init__()
        self.geometry("600x500")
        self.title(f"Чат - {username}")

        self.username = username
        self.raw = None
        self.file_name = None

        # --- поле для чату ---
        self.chat_field = CTkScrollableFrame(self, width=580, height=400)
        self.chat_field.pack(padx=10, pady=10, fill="both", expand=True)

        # --- нижня панель ---
        bottom_frame = CTkFrame(self)
        bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)

        self.mesasge_entry = CTkEntry(bottom_frame, 
            placeholder_text="Введіть ваше повідомлення", height=40
        )
        self.mesasge_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.send_image = CTkButton(
            bottom_frame, text="📁", width=50, height=40, command=self.open_img
        )
        self.send_image.pack(side="left", padx=5)

        self.send_message = CTkButton(
            bottom_frame, text=">", width=50, height=40, command=self.send_msg
        )
        self.send_message.pack(side="left", padx=5)

        # превʼю картинки (якщо вибрана)
        self.image_to_send = CTkLabel(self, text="")
        self.image_to_send.bind("<Button-1>", self.remove_image)

        # --- підключення до сервера ---
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((str(server), int(port)))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} підключився до чату!\n"
            self.socket.sendall(hello.encode("utf-8"))
            threading.Thread(target=self.recieve_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалось підключитися до сервера: {e}")

    # ------------------- UI -------------------
    def remove_image(self, e=None):
        self.image_to_send.pack_forget()
        self.raw = None
        self.file_name = None

    def add_message(self, message, img=None):
        message_frame = CTkFrame(self.chat_field, fg_color="#636363")
        message_frame.pack(pady=5, anchor="w", fill="x")

        if not img:
            CTkLabel(
                message_frame,
                text=message,
                wraplength=500,
                justify="left",
                text_color="white",
            ).pack(padx=10, pady=5, anchor="w")
        else:
            CTkLabel(
                message_frame,
                text=message,
                wraplength=500,
                justify="left",
                image=img,
                compound="top",
                text_color="white",
            ).pack(padx=10, pady=5, anchor="w")

    # ------------------- Логіка -------------------
    def send_msg(self):
        message = self.mesasge_entry.get()
        if message and not self.raw:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.socket.sendall(data.encode())
            except:
                pass
        elif self.raw:
            b64_data = base64.b64encode(self.raw).decode()
            data = f"IMAGE@{self.username}@{message}@{b64_data}\n"
            try:
                self.socket.sendall(data.encode())
            except:
                pass
            self.add_message(
                f"{self.username}: {message}",
                img=self.resize_img(Image.open(self.file_name)),
            )
            self.remove_image()
        self.mesasge_entry.delete(0, "end")

    def resize_img(self, image):
        width, height = image.size
        max_width, max_height = 300, 300
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            width, height = int(width * ratio), int(height * ratio)
        resized_img = image.resize((width, height), Image.Resampling.LANCZOS)
        return CTkImage(resized_img, size=(width, height))

    def open_img(self):
        self.file_name = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if not self.file_name:
            return
        try:
            with open(self.file_name, "rb") as f:
                self.raw = f.read()
            # показати превʼю
            self.image_to_send.configure(
                image=CTkImage(Image.open(self.file_name), size=(100, 100))
            )
            self.image_to_send.pack(pady=5)
        except Exception as e:
            self.add_message(f"Помилка: {e}")

    def recieve_message(self):
        buffer = ""
        while True:
            try:
                message = self.socket.recv(16384)
                if not message:
                    break
                buffer += message.decode("utf-8", errors="ignore")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.socket.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            self.add_message(f"{parts[1]}: {parts[2]}")
        elif msg_type == "IMAGE":
            try:
                image_data = base64.b64decode(parts[3])
                img = Image.open(io.BytesIO(image_data))
                img = self.resize_img(img)
                self.add_message(f"{parts[1]}: {parts[2]}", img=img)
            except Exception as e:
                self.add_message(f"Помилка: {e}")
