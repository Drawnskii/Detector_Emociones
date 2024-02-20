import cv2
import tkinter as tk
import numpy as np

import requests
import webview

from PIL import Image, ImageTk 
from io import BytesIO  # Importar BytesIO desde el módulo io

from src.Procesos_Modelos import Procesa_Modelos # Se importan todas las clases del archivo Procesos_Modelos.py
from Superbase import SuperbaseClient # Se importa el módulo de conexión con superbase

def crea_interfaz():
        # Se carga el cuadro de las imágenes como globar
        global frame_imagenes

        procesos_md = Procesa_Modelos() # Se crea un objeto del tipo "Procesa_Modelos"

        # Crear la ventana principal
        ventana = tk.Tk()
        ventana.title("Detección de Emociones")
        ventana.geometry("1920x1080")
        ventana.configure(bg="#0a111c")

        # Crea el frame encabezado
        encabezado = tk.Frame(ventana, bg="#0a111c", bd=5)
        encabezado.place(relx=0.5, rely=0.09, relwidth=0.9, relheight=0.20, anchor="center")

        # Agrega un título
        titulo_label = tk.Label(encabezado, text="'Sistema de Detección de Emociones' y recomendación de\nmúsica o películas",
                                        font=("Share Tech Mono", 25, "bold"), bg="#0a111c", fg="white")
        titulo_label.pack()
        titulo_label.place(relx=0.5, rely=0.6, anchor="center")

        # Dividir la ventana en dos secciones: izquierda y derecha
        frame_izquierda = tk.Frame(ventana, bg="#0a111c", bd=5)
        frame_izquierda.place(relx=0.05, rely=0.16, relwidth=0.5, relheight=0.8)

        frame_derecha = tk.Frame(ventana, bg="#0a111c", bd=5)
        frame_derecha.place(relx=0.500, rely=0.16, relwidth=0.47, relheight=0.8)

        # Crear un cuadro para el video en la sección izquierda
        cuadro_video_frame = tk.Frame(frame_izquierda, bg="#202a3d", bd=5)
        cuadro_video_frame.place(relx=0.45, rely=0.45, relwidth=0.9, relheight=0.8, anchor="center")

        # Crear el cuadro para mostrar el video en el Frame
        cuadro_video = tk.Label(cuadro_video_frame, bg="#202a3d", bd=0)
        cuadro_video.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        procesos_md.cuadro_video = cuadro_video # Se asigna la etiqueta a "Cuadro_Video" al objeto "Procesos

        # Etiqueta y cuadro de texto en la sección derecha
        etiqueta = tk.Label(frame_derecha, text="Emoción Detectada:", font=("Roboto", 14, "bold"), bg="#0a111c", fg="#bcbdc0")
        etiqueta.place(relx=0.02, rely=0.06)

        cuadro_texto = tk.Label(frame_derecha, font=("Roboto", 14, "bold"), bg="#202a3d", fg="#bcbdc0")
        cuadro_texto.place(relx=0.45, rely=0.06, relwidth=0.52)

        # Frame para imágenes en la sección derecha
        frame_imagenes = tk.Frame(frame_derecha, bg="#202a3d", bd=5)
        frame_imagenes.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.7, anchor="center")

        # Frame para los botones en la parte inferior
        frame_botones = tk.Frame(ventana, bg="#0a111c", bd=5)
        frame_botones.place(relx=0.5, rely=0.91, relwidth=0.9, relheight=0.12, anchor="center")

        # Crear los botones dentro del frame_botones
        boton_1 = tk.Button(frame_botones, text="Inicializar Cámara", bg="#0096ff", fg="white", relief="flat", command=procesos_md.control_captura)
        boton_1.grid(row=0, column=0, padx=10, pady=25, ipadx=20, ipady=10)
        procesos_md.boton_1 = boton_1 # Se asigna la etiqueta a "Cuadro_Video" al objeto "Procesos

        boton_2 = tk.Button(frame_botones, text="Recomendar Canción", bg="#0096ff", fg="white", relief="flat", command=lambda: recomendar_multimedia("canciones", procesos_md.capturar_emocion()))
        boton_2.grid(row=0, column=1, padx=10, pady=25, ipadx=20, ipady=10)

        boton_3 = tk.Button(frame_botones, text="Recomendar Película", bg="#0096ff", fg="white", relief="flat", command=lambda: recomendar_multimedia("peliculas", procesos_md.capturar_emocion()))
        boton_3.grid(row=0, column=2, padx=10, pady=25, ipadx=20, ipady=10)

        procesos_md.lbl_emocion = cuadro_texto # Se actualiza la etiqueta "cuadro_texto" con emoción detectada tras cada recomendación

        # Centrar los botones horizontalmente
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        frame_botones.grid_columnconfigure(2, weight=1)

        # Aplicar una fuente específica
        fuente_personalizada = ("Roboto", 12)
        boton_1.config(font=fuente_personalizada)
        boton_2.config(font=fuente_personalizada)
        boton_3.config(font=fuente_personalizada)

        # Inicializar la captura de video desde la cámara
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Ancho del frame
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Alto del framee

        # Mostrar la ventana
        ventana.mainloop()

        cap.release() # Libera la captura de video

def recomendar_multimedia(tabla, emocion):
        # Intenta obtener la recomendación de multimedia desde Superbase
        try:
                # Crea una instancia de SuperbaseClient
                superbase_client = SuperbaseClient()
                # Obtiene la recomendación de multimedia
                recomendacion = superbase_client.obtener_multimedia(tabla, emocion)

                # Verifica si la recomendación existe
                if recomendacion:
                # Muestra la imagen y asocia el enlace
                        imagen = recomendacion.data[0]["imagen"]
                        enlace = recomendacion.data[0]["enlace"]
                        mostrar_imagen_recomendacion(imagen, enlace)
                else:
                        print("No se encontró ninguna recomendación para la emoción", emocion)
        except Exception as e:
                # Maneja cualquier error que ocurra durante el proceso de recomendación
                print("Error al recomendar multimedia:", str(e))


def mostrar_imagen_recomendacion(imagen_url, enlace_recomendacion):
        # Descargar la imagen desde la URL
        response = requests.get(imagen_url)
        imagen_data = response.content

        # Convertir la imagen descargada a un objeto Image
        imagen_recomendacion = Image.open(BytesIO(imagen_data))

        # Convertir la imagen a un formato que Tkinter pueda manejar
        imagen_tk = ImageTk.PhotoImage(imagen_recomendacion)

        # Limpiar el frame de imágenes antes de mostrar la nueva imagen
        for widget in frame_imagenes.winfo_children():
                widget.destroy()

        # Crear etiqueta para mostrar la nueva imagen en el frame
        cuadro_imagen_recomendacion = tk.Label(frame_imagenes, image=imagen_tk, bd=0)
        cuadro_imagen_recomendacion.image = imagen_tk
        cuadro_imagen_recomendacion.pack(expand=True)

        # Asociar el enlace al clic en la imagen
        cuadro_imagen_recomendacion.bind("<Button-1>", lambda event: crear_ventana("Recomendación", enlace_recomendacion))

def crear_ventana(titulo, enlace):
        # Se crea la ventana de visualización
        webview.create_window(titulo, enlace)

        # Se muestra la ventana en pantalla
        webview.start()