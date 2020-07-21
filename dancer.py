import Tkinter
from PIL import Image, ImageTk, ImageEnhance

class Dancer:
    """Dancer Class
    A Module extracted from the book called Python for Bioinformatics by Jason Kinser.
    ----------------------------------------------------------------------------------
    """
    def __init__(self, JPY):
        self.rt = Tkinter.Tk()
        self.rt.withdraw()
        self.tp = [ Tkinter.Toplevel(self.rt, visual="best")]
        self.tp[0].title('Image #1')
        self.mg = [Image.open(JPY + '/startup.jpg')]
        self.ph = [ImageTk.PhotoImage(self.mg)]
        self.lb = [Tkinter.Label(self.tp[0], image = self.ph[0])]
        #Use Button-2 for point and shoot
        self.lb[0].bind("<Button-3>", self.PointShoot)
        self.lb[0].pack(anchor='nw', side='left')
    
    def Show(self, N=0):
        pass
