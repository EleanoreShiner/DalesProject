import tkinter as tk
from tkinter import ttk


class TempConvertor:
    def __init__(self, kelvin):
        self._kelvin = kelvin

    @property
    def kelvin(self):
        return self._kelvin

    @kelvin.setter
    def kelvin(self, k):
        self._kelvin = k

    @property
    def celsius(self):
        return self._kelvin - 273.15

    @celsius.setter
    def celsius(self, c):
        self._kelvin = c + 273.15

    @property
    def farenheit(self):
        return (self.celsius) * 9 / 5 + 32

    @farenheit.setter
    def farenheit(self, f):
        self._kelvin = (f - 32) * (5 / 9) + 273.15


class GUI(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.config(bg="white")

        self.edt = tk.Entry(self,
                            bg="white",
                            fg="black")
        self.edt2 = tk.Entry(self,
                            bg="white",
                            fg="black")
        Temps = "Celsius", "Fahrenheit", "Kelvin"
        self.temp1 = ttk.Combobox(self, state="readonly", values = Temps)
        self.temp2 = ttk.Combobox(self, state="readonly", values = Temps)

        self.temp1.set("Choose First Temp Scale")
        self.temp2.set("Choose Second Temp Scale")


        self.place_widgets()

    def place_widgets(self):

        placement_settings = {'padx': 25, 'pady': 25, 'sticky': 'news'}

        self.temp1.grid(row=0, column=0, **placement_settings)
        self.temp2.grid(row=0, column=1, **placement_settings)
        self.edt.grid(row=1, column=0, **placement_settings)
        self.edt2.grid(row=1, column=1, **placement_settings)


    def convert(self):

        if self.edt.get():
            value = float(self.edt.get())
        elif self.edt2.get():
            value = float(self.edt2.get())

        first = self.temp1.get()
        second = self.temp2.get()

        converter = TempConvertor(0)

        if first == "Celsius":
            converter.celsius = value
        elif first == "Fahrenheit":
            converter.farenheit = value
        elif first == "Kelvin":
            converter.kelvin = value

        if second == "Celsius":
            result = converter.celsius
        elif second == "Fahrenheit":
            result = converter.farenheit
        elif second == "Kelvin":
            result = converter.kelvin

        if self.edt.get():
            self.edt2.delete(0, tk.END)
            self.edt2.insert(f"{result:.2f}")
        if self.edt2.get():
            self.edt.delete(0, tk.END)
            self.edt.insert(f"{result:.2f}")




if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('550x200+100+100')
    root.title('Tkinter Class Example')
    main_frame = GUI(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()