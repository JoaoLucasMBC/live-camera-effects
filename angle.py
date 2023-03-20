class Angle:

    ESTADOS = {"rotate":False, "reverse":False,"wasd":False, "incremento": 1}

    @classmethod
    def main(cls, function, angle):
        if function == ord('r'):
            return cls.rotate(angle)
        elif function == ord('t'):
            return cls.reverse_rotate(angle)
        elif function == ord('w') or function == ord("d") or function == ord("a"):
            return cls.wasd(angle, function)
        elif function == ord('f'):
            cls.faster()
        elif function == ord("x"):
            return cls.restart()
        return angle

    @classmethod
    def rotate(cls, angle):
        if not cls.ESTADOS["wasd"]:
            cls.ESTADOS["rotate"] = True
            cls.ESTADOS["reverse"] = False
            angle += cls.ESTADOS["incremento"]
        return angle
    
    @classmethod
    def reverse_rotate(cls, angle):
        if not cls.ESTADOS["wasd"]:
            cls.ESTADOS["reverse"] = True
            cls.ESTADOS["rotate"] = False
            angle -= cls.ESTADOS["incremento"]
        return angle
    
    @classmethod
    def wasd(cls, angle, function):
        if not cls.ESTADOS["rotate"] and not cls.ESTADOS["reverse"]:
            if function == ord("w"):
                cls.ESTADOS["wasd"] = True
            if cls.ESTADOS["wasd"]:
                if function == ord("d"):
                    angle += 5
                elif function == ord("a"):
                    angle -= 5
        return angle
    
    @classmethod
    def faster(cls):
        cls.ESTADOS["incremento"] *= 2

    @classmethod 
    def restart(cls):
        cls.ESTADOS = {"rotate":False, "reverse":False,"wasd":False, "incremento":1}
        return 1