from app import Aplicacion

class Main:
    
    def __init__(self):
        self.app = Aplicacion()

    def run(self):
        self.app.inicio()
    
if __name__ == "__main__":
    main = Main()
    main.run()