import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Variables globales
img = None
img_pixelada = None
tk_img = None
zoom = 1
pixel_size = 10

# Funciones
def abrir_imagen():
    global img, img_pixelada, tk_img, zoom, pixel_size
    path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg;*.bmp")])
    if path:
        img = Image.open(path)
        img_pixelada = None
        zoom = 1
        pixel_size = 10
        mostrar_imagen(img)
        # Deshabilitar controles de píxel hasta que se pulse "Pixelar Imagen"
        btn_pixel_mas.config(state=tk.DISABLED)
        btn_pixel_menos.config(state=tk.DISABLED)

def pixelar_imagen():
    global img, img_pixelada, tk_img, pixel_size
    if img is None:
        messagebox.showwarning("Aviso", "Primero abre una imagen")
        return
    ancho, alto = img.size
    img_small = img.resize((max(1, ancho//pixel_size), max(1, alto//pixel_size)), Image.BILINEAR)
    img_pixelada = img_small.resize(img.size, Image.NEAREST)
    mostrar_imagen(img_pixelada)

    # Habilitar controles de píxeles
    btn_pixel_mas.config(state=tk.NORMAL)
    btn_pixel_menos.config(state=tk.NORMAL)

def mostrar_imagen(imagen):
    global tk_img, zoom
    ancho, alto = imagen.size
    ancho_zoom = int(ancho * zoom)
    alto_zoom = int(alto * zoom)
    img_mostrable = imagen.resize((ancho_zoom, alto_zoom), Image.NEAREST)
    tk_img = ImageTk.PhotoImage(img_mostrable)
    lbl_imagen.config(image=tk_img)

def aumentar_zoom():
    global zoom
    zoom += 0.1
    if img_pixelada:
        mostrar_imagen(img_pixelada)
    elif img:
        mostrar_imagen(img)

def disminuir_zoom():
    global zoom
    zoom = max(0.1, zoom - 0.1)
    if img_pixelada:
        mostrar_imagen(img_pixelada)
    elif img:
        mostrar_imagen(img)

def aumentar_pixel():
    global pixel_size
    pixel_size += 1
    pixelar_imagen()

def disminuir_pixel():
    global pixel_size
    pixel_size = max(1, pixel_size - 1)
    pixelar_imagen()

def guardar_imagen():
    global img_pixelada
    if img_pixelada is None:
        messagebox.showwarning("Aviso", "No hay imagen pixelada para guardar")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("JPG","*.jpg")])
    if path:
        img_pixelada.save(path)
        messagebox.showinfo("Guardado", f"Imagen pixelada guardada en:\n{path}")

def mostrar_info():
    messagebox.showinfo("Información",
        """*** IMAGE TO PIXELS ***

Autor: sebastianllg
WhatsApp: +593 984548191
Email: sebastianllg@gmail.com
Paypal Donations: @sebastianllerena1
"""
    )

def salir():
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Pixelador de Imágenes")
ventana.geometry("1000x700")

# Frame botones a la izquierda
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Botón abrir imagen
tk.Button(frame_botones, text="Abrir Imagen", width=20, command=abrir_imagen).pack(pady=5)

# Sección Zoom
lbl_zoom = tk.Label(frame_botones, text="Zoom")
lbl_zoom.pack(pady=2)
tk.Button(frame_botones, text="+", width=8, command=aumentar_zoom).pack(pady=2)
tk.Button(frame_botones, text="-", width=8, command=disminuir_zoom).pack(pady=2)

# Sección Tamaño de píxeles
lbl_pixel = tk.Label(frame_botones, text="Tamaño de Pixel")
lbl_pixel.pack(pady=5)
btn_pixel_mas = tk.Button(frame_botones, text="+", width=8, command=aumentar_pixel, state=tk.DISABLED)
btn_pixel_mas.pack(pady=2)
btn_pixel_menos = tk.Button(frame_botones, text="-", width=8, command=disminuir_pixel, state=tk.DISABLED)
btn_pixel_menos.pack(pady=2)

# Pixelar imagen
tk.Button(frame_botones, text="Pixelar Imagen", width=20, command=pixelar_imagen).pack(pady=10)

# Guardar imagen
tk.Button(frame_botones, text="Guardar Imagen Pixelada", width=20, command=guardar_imagen).pack(pady=5)

# Información y Salir
tk.Button(frame_botones, text="Información", width=20, command=mostrar_info).pack(pady=5)
tk.Button(frame_botones, text="Salir", width=20, command=salir).pack(pady=5)

# Label para imagen a la derecha
lbl_imagen = tk.Label(ventana)
lbl_imagen.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)

ventana.mainloop()
