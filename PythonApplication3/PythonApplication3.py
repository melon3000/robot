import os
import customtkinter as ctk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk

PART_FOLDERS = {
    "Näo kuju": "fotorobot/naovorm",
    "Silmad": "fotorobot/silmad",
    "Nina": "fotorobot/ninad",
    "Suu": "fotorobot/suud",
}

IMAGE_SIZE = (400, 400)
CANVAS_SIZE = (600, 600)

pildid = {}
current_indices = {}
objektid = {}
controls = {}

LAYER_ORDER = ["Näo kuju", "Nina", "Silmad", "Suu"]

def load_images():
    for osa, folder in PART_FOLDERS.items():
        pildid[osa] = []
        if not os.path.exists(folder):
            os.makedirs(folder)
        files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".png")])
        for f in files:
            try:
                img = Image.open(os.path.join(folder, f)).convert("RGBA").resize(IMAGE_SIZE, Image.NEAREST)
                tk_img = ImageTk.PhotoImage(img)
                pildid[osa].append((f, tk_img))
            except Exception as e:
                print(f"Ошибка загрузки {f}: {e}")

def update_all_images():
    canvas.delete("all")
    objektid.clear()

    for osa in LAYER_ORDER:
        if osa not in current_indices or not pildid[osa]:
            continue
        idx = current_indices[osa]
        fname, tk_img = pildid[osa][idx]
        controls[osa].configure(text=fname)
        objektid[osa] = canvas.create_image(300, 300, image=tk_img)

def prev_image(osa):
    if not pildid[osa]:
        return
    current_indices[osa] = (current_indices[osa] - 1) % len(pildid[osa])
    update_all_images()

def next_image(osa):
    if not pildid[osa]:
        return
    current_indices[osa] = (current_indices[osa] + 1) % len(pildid[osa])
    update_all_images()

def save_robot():
    try:
        # Loome uue tühja pildi läbipaistva taustaga
        lõpptulemus = Image.new("RGBA", IMAGE_SIZE, (255, 255, 255, 0))

        for osa in LAYER_ORDER:
            if osa not in current_indices or not pildid[osa]:
                continue

            idx = current_indices[osa]
            failinimi, _ = pildid[osa][idx]
            pildi_tee = os.path.join(PART_FOLDERS[osa], failinimi)

            # Laeme pildi uuesti ja kombineerime
            kiht = Image.open(pildi_tee).convert("RGBA").resize(IMAGE_SIZE, Image.NEAREST)
            lõpptulemus = Image.alpha_composite(lõpptulemus, kiht)

        # Salvesta lõpptulemus PNG-failina
        lõpptulemus.save("fotorobot.png")
        messagebox.showinfo("Edukalt salvestatud", "Fotorobot on salvestatud kui 'fotorobot.png'!")

    except Exception as e:
        messagebox.showerror("Viga", f"Fotoroboti salvestamine ebaõnnestus: {e}")


ctk.set_appearance_mode("dark")  # или "light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fotorobot - Листай части лица стрелочками")
app.geometry("1200x700")

load_images()

control_frame = ctk.CTkScrollableFrame(app, width=550, height=650)
control_frame.pack(side="left", padx=10, pady=10, fill="y")

canvas = Canvas(app, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1], bg="white")
canvas.pack(side="right", padx=20, pady=20)

for osa in pildid:
    frame = ctk.CTkFrame(control_frame, fg_color="#2b2b2b", corner_radius=8)
    frame.pack(fill="x", pady=10)

    label = ctk.CTkLabel(frame, text=osa, font=("Segoe UI", 22, "bold"))
    label.pack(padx=10, pady=5)

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack()

    btn_prev = ctk.CTkButton(btn_frame, text="<", width=40,
                             command=lambda o=osa: prev_image(o))
    btn_prev.pack(side="left", padx=10, pady=5)

    controls[osa] = ctk.CTkLabel(btn_frame, text="", font=("Segoe UI", 16))
    controls[osa].pack(side="left", padx=10)

    btn_next = ctk.CTkButton(btn_frame, text=">", width=40,
                             command=lambda o=osa: next_image(o))
    btn_next.pack(side="left", padx=10, pady=5)

    current_indices[osa] = 0  # инициализация индекса для каждой части

update_all_images()  # один раз отрисовать все части после инициализации

btn_salvesta = ctk.CTkButton(control_frame, text="Сохранить фоторобота", command=save_robot)
btn_salvesta.pack(pady=10)
    

app.mainloop()
