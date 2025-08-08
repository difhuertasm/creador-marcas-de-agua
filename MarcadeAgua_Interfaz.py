from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk

ruta_archivo = "" 

def buscar_archivo():
    #Abre un diálogo para seleccionar una imagen y almacena la ruta en la variable global.
    global ruta_archivo
    ruta_archivo = fd.askopenfilename(title="Seleccionar archivo",
                                      filetypes=[("Imágenes", "*.png;*.jpg")])
    if ruta_archivo:
        etiqueta1.config(text="Archivo seleccionado.")

def MarcadeAgua():
    #Aplica una marca de agua a la imagen seleccionada y devuelve la imagen modificada.
    global ruta_archivo
    if not ruta_archivo:
        messagebox.showerror("Error", "Primero debes seleccionar un archivo.")
        return None

    tamano_fuente = 100 #Tamaño de fuente predeterminada
    imagen = Image.open(ruta_archivo).convert("RGBA")

    # Elección carga de fuente
    archivo_fuente = "ARIAL.TTF" if lista2.get() == "Arial" else "ARIAL-BLACK.TTF"
    
    # Carga de fuente
    fuente = ImageFont.truetype(archivo_fuente, tamano_fuente)

    # Obtiene el texto para la marca de agua
    texto_marca_agua = entrada_texto.get()

    # Define tamaño de la imagen de marca de agua
    ancho, alto = 4300, 3300
    imagen_marca_agua = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    dibujo_marca = ImageDraw.Draw(imagen_marca_agua)

    # Calcula el tamaño del texto
    limite_texto = dibujo_marca.textbbox((0, 0), texto_marca_agua, font=fuente)
    ancho_texto = limite_texto[2] - limite_texto[0]
    alto_texto = limite_texto[3] - limite_texto[1]

    # Elección del color de la marca de agua
    color_marca = (255, 0, 0, 200) if lista1.get() == "Rojo semitransparente" else (0, 0, 0, 200)

    # Posiciona el texto en el centro de la imagen de marca de agua
    x = (ancho - ancho_texto) // 2
    y = (alto - alto_texto) // 2
    dibujo_marca.text((x, y), texto_marca_agua, font=fuente, fill=color_marca)

    # Elección del ángulo de rotación
    rotacion = int(lista3.get())

    # Rota la imagen de la marca de agua
    marca_rotada = imagen_marca_agua.rotate(rotacion, expand=True)

    # Calcula posición centrada en la imagen original
    x_centrado = (imagen.width - marca_rotada.width) // 2
    y_centrado = (imagen.height - marca_rotada.height) // 2

    # Fusiona la marca de agua con la imagen original
    imagen.paste(marca_rotada, (x_centrado, y_centrado), marca_rotada)

    return imagen

def GuardarArchivo():
    #Guarda la imagen con la marca de agua aplicada.
    imagen_modificada = MarcadeAgua()
    if imagen_modificada:
        imagen_modificada.save("resultado2.png", format="PNG")
        messagebox.showinfo("Éxito", "Imagen guardada como 'resultado2.png'.")
        Label(ventana, text="Imagen guardada exitosamente.", bg= "#BEF1CC", fg='#022212', font = ("Arial", 15)).place(x=250, y=190)

'''______________________INTERFAZ GRÁFICA Y COMPONENTES___________'''

ventana = Tk()
ventana.title("Watermarks Maker WM")
ventana.minsize(width=640, height=300)
ventana.config(padx=35, pady=35, bg='#BEF1CC')

Label(ventana, text="1. Seleccione el documento", bg='#BEF1CC', fg="#3A3A3A").place(x=0, y=0)
boton_buscar = tk.Button(ventana, text="Buscar Archivo", bg='#022212', fg="#BEF1CC", command=buscar_archivo)
boton_buscar.place(x=0, y=30)
etiqueta1 = Label(ventana, text="No se ha seleccionado ningún archivo", bg='#BEF1CC', fg="#022212")
etiqueta1.place(x=0, y=70)

Label(ventana, text='2. Ingrese el texto para incluir en la marca de agua', bg='#BEF1CC', fg="#022212").place(x=250, y=0)
entrada_texto = Entry(ventana, bg='#F2FCF5')
entrada_texto.place(relwidth=0.5, relheight=0.1, x=250, y=30)

Label(ventana, text="3. Color", bg='#BEF1CC', fg="#3A3A3A").place(x=0, y=110)
lista1 = ttk.Combobox(ventana, values=["Rojo semitransparente", "Negro semitransparente"])
lista1.place(x=0, y=140)

Label(ventana, text="4. Fuente", bg='#BEF1CC', fg="#3A3A3A").place(x=200, y=110)
lista2 = ttk.Combobox(ventana, values=["Arial", "Arial Black"])
lista2.place(x=200, y=140)

Label(ventana, text="5. Ángulo de rotación", bg='#BEF1CC', fg="#3A3A3A").place(x=400, y=110)
lista3 = ttk.Combobox(ventana, values=["0", "45", "65"]) 
lista3.place(x=400, y=140)

boton_generar = tk.Button(ventana, text="Generar Archivo con marca", bg='#022212',fg="#BEF1CC", command=GuardarArchivo)
boton_generar.place(x=0, y=190)

ventana.mainloop()
