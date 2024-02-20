import cv2

from tensorflow.keras.models import load_model

class Carga_Modelos:
    def cargar_modelo_fec(self, direccion_modelo):
        self.modelo_fec = load_model(direccion_modelo)

    def cargar_modelo_cascada(self, direccion_modelo):
        self.modelo_cascada = cv2.CascadeClassifier(direccion_modelo)
