import numpy as np
import cv2 as cv

from rotation import RotationEffect


class Program():

    ESTADOS = {"rodando":False, "wasd":False, "rapido":1}


    def __init__(self, width, height):
        self.width = width
        self.height = height


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

            # ANGLE MANIPULATION
            if not self.ESTADOS["wasd"]:
                if cv.waitKey(1) == ord('r'):
                    if self.ESTADOS["rodando"]:
                        self.ESTADOS["rodando"] = False
                    else:
                        self.ESTADOS["rodando"] = True
                    print(self.ESTADOS["rodando"])

            if not self.ESTADOS["rodando"]:
                if cv.waitKey(1) == ord('w'):
                    if self.ESTADOS["wasd"]:
                        self.ESTADOS["wasd"] = False
                    else:
                        self.ESTADOS["wasd"] = True
                    print(self.ESTADOS["wasd"])

            if cv.waitKey(1) == ord('f'):
                self.ESTADOS["rapido"] *= 2
            if cv.waitKey(1) == ord('s'):
                self.ESTADOS["rapido"] = 1

            if self.ESTADOS["rodando"]:
                angle += 1 * self.ESTADOS["rapido"]

            if self.ESTADOS["wasd"]:
                if cv.waitKey(1) == ord('d'):
                    angle += 1 * self.ESTADOS["rapido"]
                elif cv.waitKey(1) == ord('a'):
                    angle -= 1 * self.ESTADOS["rapido"]

            print(angle, self.ESTADOS["rapido"])
            ## TRANSFORMATION
            image_ = RotationEffect.rotate(image, angle)


            # Agora, mostrar a imagem na tela!
            cv.imshow('Minha Imagem!', image_)
            
            # Se aperto 'q', encerro o loop
            if cv.waitKey(1) == ord('q'):
                break        

        # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    program = Program(320, 240)
    program.run()