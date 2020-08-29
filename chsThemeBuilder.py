import tkinter as tk


class RGB(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")

        # WIDGETS
        self.r = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, length=300)
        self.g = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, length=300)
        self.b = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, length=300)
        self.preview = tk.Frame(self, bg="white", width=150, height=150)

        XOFF = 20
        self.REFRESH = 50

        self.r.grid(row=0, column=0, padx=XOFF, pady=30)
        self.g.grid(row=1, column=0, padx=XOFF, pady=15)
        self.b.grid(row=2, column=0, padx=XOFF, pady=30)

        self.preview.grid(row=0, column=1, rowspan=3)
        self.updateFrame()

    def updateFrame(self):
        strHex = self.toHex((self.r.get(), self.g.get(), self.b.get()))
        self.preview.config(bg=strHex)
        self.preview.after(self.REFRESH, self.updateFrame)

    @staticmethod
    def toHex(colors: tuple):
        string = ["#"]
        for value in colors:
            string.append(format(value, "02x"))

        return "".join(string)


RGB().mainloop()

