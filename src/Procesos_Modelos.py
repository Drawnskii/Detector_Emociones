import cv2
import numpy as np

from PIL import Image, ImageTk
from tkinter import Label  # Importa el Label desde tkinter
from tensorflow.keras.preprocessing.image import img_to_array

from src.Modelos import Carga_Modelos # Se importa la clase "Carga_Modelos" del archivo Modelos.py

class Procesa_Modelos:
    # Constructor
    def __init__(self):  # Pasar referencia al botón 1 al constructor
        self.md = Carga_Modelos()
        self.md.cargar_modelo_fec('modelos/modelFEC.h5')
        self.md.cargar_modelo_cascada('modelos/haarcascade_frontalface.xml')
        self.camara_encendida = False
        self.cap = None
        self.frame = None
        self.contador_rostros = 0
        self.cuadro_video = None
        self.boton_1 = None  # Asignar el botón pasado como argumento al atributo de la clase
        self.lbl_emocion = None

    # Métodos
    def capturar_emocion(self):
        cara_recortada = self.capturar_cara()
        img = cv2.cvtColor(cara_recortada, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (48, 48))
        cara = img_to_array(img)
        cara = np.expand_dims(cara, axis=0)
        emociones = self.md.modelo_fec.predict(cara)
        emocion_predicha = np.argmax(emociones)
        emociones_lista = ["Enojo", "Disgusto", "Miedo", "Felicidad", "Neutral", "Tristeza", "Sorpresa"]
        emocion_detectada = emociones_lista[emocion_predicha]
        self.lbl_emocion.config(text=emocion_detectada)
        return emocion_detectada


    def capturar_cara(self):
        if self.frame is not None:
            face_cascade = self.md.modelo_cascada
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cara_recortada = self.frame[y:y+h, x:x+w]
                return cara_recortada
    
    def mostrar_video(self):
        if self.camara_encendida:
            _, self.frame = self.cap.read()
            if _:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # Detección de rostros
                face_cascade = self.md.modelo_cascada
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Convertir el frame a formato compatible con Tkinter
                img = Image.fromarray(self.frame)
                img = ImageTk.PhotoImage(image=img)

                # Mostrar el frame en el cuadro de video (asumiendo que cuadro_video es un Label de Tkinter)
                self.cuadro_video.img = img
                self.cuadro_video.config(image=img)
                self.cuadro_video.after(10, self.mostrar_video)  # Llama recursivamente a mostrar_video
        else:
            # Si la cámara está apagada, detener la recursión
            pass

    def control_captura(self):
        if self.camara_encendida and self.cap is not None:
            self.cap.release()
            self.boton_1.config(text="Inicializar Cámara")
            self.camara_encendida = False
        else:
            self.cap = cv2.VideoCapture(0)
            self.boton_1.config(text="Apagar Cámara")
            self.camara_encendida = True
            self.mostrar_video()  # Iniciar la visualización del video si la cámara está encendida
