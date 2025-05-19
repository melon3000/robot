import customtkinter as ctk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
import os

# Словари для хранения изображений, объектов и состояния
pildid = {}
objektid = {}
olemas = {}

# Путь к папке с изображениями
IMAGE_FOLDER = "fotorobot"

# Функция для отображения части лица
def toggle_osa(nimi, fail, x, y):
    if nimi in objektid:
        canvas.delete(objektid[nimi])  # Удаляем изображение с canvas
        objektid.pop(nimi)  # Удаляем объект из словаря
        olemas[nimi] = False  # Обновляем состояние
    else:
        # Проверка наличия файла перед загрузкой
        if not os.path.exists(f"{IMAGE_FOLDER}/{fail}"):
            messagebox.showerror("Ошибка", f"Файл {fail} не найден!")
            return

        try:
            pilt_img = Image.open(f"{IMAGE_FOLDER}/{fail}").convert("RGBA").resize((200, 200))  # Загружаем и изменяем размер
            tk_img = ImageTk.PhotoImage(pilt_img)

            pildid[nimi] = tk_img  # Сохраняем изображение
            objektid[nimi] = canvas.create_image(x, y, image=tk_img)  # Создаем изображение на canvas
            olemas[nimi] = True  # Обновляем состояние
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

# Функция для сохранения выбранных частей лица в файл
def salvesta_robot():
    valikud = [nimi for nimi, olek in olemas.items() if olek]
    try:
        with open("fotorobotid.txt", "w") as file:
            file.write(",".join(valikud))
        messagebox.showinfo("Успех", "Фоторобот сохранён!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить фоторобот: {e}")

# Функция для загрузки последнего фоторобота
def lae_viimane_robot():
    # Удаляем все текущие изображения с canvas
    canvas.delete("all")
    objektid.clear()  # Очистка словаря объектов
    olemas.clear()    # Очистка словаря состояний

    try:
        with open("fotorobotid.txt", "r") as file:
            valikud = file.read().split(",")
        for nimi in valikud:
            if nimi in pildid:
                toggle_osa(nimi, f"{nimi}.png", 200, 200)
        messagebox.showinfo("Успех", "Последний фоторобот загружен!")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл с фотороботами не найден!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить фоторобот: {e}")

# Основное окно приложения
app = ctk.CTk()

# Canvas для отображения фоторобота
canvas = Canvas(app, width=400, height=400, bg="white")
canvas.pack(side="right", padx=10, pady=10)

# Frame для кнопок с Checkbutton
frame_mus = ctk.CTkFrame(app)
frame_mus.pack(side="left", padx=10, pady=10)

# Кнопки для выбора частей лица
btn_nao_ovaal = ctk.CTkCheckBox(frame_mus, text="Näo ovaal", command=lambda: toggle_osa("näo_ovaal", "naovorm1.png", 200, 150))
btn_nao_ovaal.pack()

btn_silmad = ctk.CTkCheckBox(frame_mus, text="Silmad", command=lambda: toggle_osa("silmad", "silmad1.png", 200, 150))
btn_silmad.pack()

btn_anteen = ctk.CTkCheckBox(frame_mus, text="Anteen", command=lambda: toggle_osa("anteen", "anteen1.png", 200, 150))
btn_anteen.pack()

btn_suu = ctk.CTkCheckBox(frame_mus, text="Suu", command=lambda: toggle_osa("suu", "suu1.png", 200, 150))
btn_suu.pack()


# Кнопки для сохранения и загрузки фоторобота
btn_salvesta = ctk.CTkButton(frame_mus, text="Salvesta fotorobot", command=salvesta_robot)
btn_salvesta.pack(pady=10)

btn_vaata_viimane = ctk.CTkButton(frame_mus, text="Vaata viimast robotit", command=lae_viimane_robot)
btn_vaata_viimane.pack(pady=10)

# Инициализируем состояние для части лица
olemas["näo_ovaal"] = False
toggle_osa("näo_ovaal", "naovorm1.png", 200, 100)

app.mainloop()
