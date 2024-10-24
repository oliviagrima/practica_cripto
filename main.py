from app import Aplication

class Main:
    
    def __init__(self):
        self.app = Aplication()

    def run(self):
        self.app.inicio()
    
if __name__ == "__main__":
    main = Main()
    main.run()