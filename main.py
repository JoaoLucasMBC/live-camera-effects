import numpy as np
import cv2 as cv

from rotation import RotationEffect
from angle import Angle


class Program():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.commands = [ord("r"),ord("t"),ord("w"), ord("x")]
        self.aux_commands = [ord("d"), ord("a"), ord("f")]
        self.command = ""
        self.aux_command = ""


    def run(self):
        # Essa função abre a câmera. Depois desta linha, a luz de câmera (se seu computador tiver) deve ligar.
        cap = cv.VideoCapture(0)

        # Talvez o programa não consiga abrir a câmera. Verifique se há outros dispositivos acessando sua câmera!
        if not cap.isOpened():
            print("Não consegui abrir a câmera!")
            exit()

        # Esse loop é igual a um loop de jogo: ele encerra quando apertamos 'q' no teclado.
        angle = 0
        while True:
            # Captura um frame da câmera
            ret, frame = cap.read()

            # A variável `ret` indica se conseguimos capturar um frame
            if not ret:
                print("Não consegui capturar frame!")
                break

            # Mudo o tamanho do meu frame para reduzir o processamento necessário
            # nas próximas etapas
            frame = cv.resize(frame, (self.width, self.height), interpolation =cv.INTER_AREA)

            # A variável image é um np.array com shape=(width, height, colors)
            image = np.array(frame).astype(float)/255

            key = cv.waitKey(1)

            # ANGLE MANIPULATION
            if key in self.commands:
                self.command = key

            if key in self.aux_commands:
                self.aux_command = key
                angle = Angle.main(self.aux_command, angle)
                self.aux_command = ""

            angle = Angle.main(self.command, angle)

            ## TRANSFORMATION
            image_ = RotationEffect.rotate(image, angle)


            # Agora, mostrar a imagem na tela!
            cv.imshow('Minha Imagem!', image_)
            
            # Se aperto 'q', encerro o loop
            if key == ord('q'):
                break        

        # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    program = Program(320, 240)
    program.run()