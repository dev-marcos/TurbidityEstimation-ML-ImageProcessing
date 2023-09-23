import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam App")
        
        self.selected_webcam = tk.StringVar()
        self.message = tk.StringVar()
        self.message.set("Aguardando ação...")
        
        self.webcams = self.get_available_webcams()
        self.selected_webcam_capture = None  # Adicione esta linha
        
        self.create_interface()
        
    def get_available_webcams(self):
        webcam_list = []
        for i in range(10):  # Tente verificar até 10 webcams (índices de 0 a 9)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                webcam_list.append("Webcam {}".format(i))
                cap.release()
        return webcam_list
        
    def create_interface(self):
        webcam_label = ttk.Label(self.root, text="Selecionar a webcam disponível:")
        webcam_label.pack(pady=10)
        
        self.webcam_combo = ttk.Combobox(self.root, textvariable=self.selected_webcam, values=self.webcams)
        self.webcam_combo.pack()
        
        start_button = ttk.Button(self.root, text="Iniciar Captura de Vídeo", command=self.start_webcam)
        start_button.pack(pady=10)
        
        save_button = ttk.Button(self.root, text="Salvar Imagem", command=self.save_image)
        save_button.pack(pady=10)
        
        self.message_label = ttk.Label(self.root, textvariable=self.message)
        self.message_label.pack(pady=10)
        
    def start_webcam(self):
        selected_webcam_index = self.webcam_combo.current()
        if selected_webcam_index >= 0:
            self.selected_webcam_capture = cv2.VideoCapture(selected_webcam_index)  # Armazene a captura da webcam selecionada
            self.message.set("Webcam {} iniciada.".format(selected_webcam_index))
            
            while True:
                ret_val, img = self.selected_webcam_capture.read()  # Use a captura da webcam selecionada
                if ret_val:
                    img = cv2.flip(img, 1)
                    imagem_gray = img[:, :, 2]
                    imagem_normalized = imagem_gray / 255.0
                    spectrogram = cv2.applyColorMap((imagem_normalized * 255).astype(np.uint8), cv2.COLORMAP_JET)
                    cv2.imshow('Espectrograma', spectrogram)
                    if cv2.waitKey(1) == 27:
                        break
            self.selected_webcam_capture.release()
            cv2.destroyAllWindows()
            self.message.set("Webcam {} encerrada.".format(selected_webcam_index))
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma webcam antes de iniciar a captura de vídeo.")
            
    def save_image(self):
        if self.selected_webcam_capture:
            ret_val, img = self.selected_webcam_capture.read()  # Captura o frame atual da webcam
            if ret_val:
                save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
                if save_path:
                    cv2.imwrite(save_path, img)
                    self.message.set("Imagem salva em '{}'.".format(save_path))
            else:
                self.message.set("Erro ao salvar a imagem.")
        else:
            messagebox.showerror("Erro", "Por favor, inicie a captura de vídeo antes de salvar a imagem.")

def main():
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
