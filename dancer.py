import Tkinter
from Tkinter import Event
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
        """Used by many of the routines."""
        self.ph[N] = ImageTK.PhotoImage(self.mg[N])
        self.lb[N].destroy()
        self.lb[N] = Tkinter.Label(self.tp[N], image=self.ph[N])
        self.lb[N].bind("<Button-3>", self.PointShoot)
        self.lb[N].pack(anchor="nw", side='left')
    
    def Load(self, filename):
        self.mg[N] = Image.open(filename)
        self.Show(N)
    
    def Add(self, filename):
        self.mg.append(Image.open(filename))
        N = len(self.mg) - 1
        self.tp.append(Tkinter.Toplevel(self.rt, visual="best"))
        self.tp[N].title('Image #' + str(N + 1))
        self.ph.append(ImageTk.PhotoImage(self.mg[N]))
        self.lb.append(Tkinter.Label(self.tp[N], image=self.ph[N]))
        self.lb[N].bind("<Button-3>", self.PointShoot)
        self.lb[N].pack(anchor='nw', side='left')

    def Paste(self, mg, N=0):
        self.mg[N] = mg
        self.Show(N)

    def Destroy(self, N1):
        """This wil change the numbers of all the subsequent images"""
        N = N - 1 # coordinates the window title (+1) with the list index
        del self.mg[N]
        del self.ph[N]
        self.lb[N].destroy()
        self.tp[N].destroy()
        del self.lb[N]
        del self.tp[N]
        #rename
        for i in range(0, len(self.mg)):
            self.tp[i].title('Image #' + str(i+1))
    def PointShoot(self, event):
        """Who has focus."""
        # a = self.rt.winfo_children()
        print(event.x, event.y), self.ph[0]._PhotoImage__Photo.get(event.x, event.y)
