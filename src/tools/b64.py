import base64
import tkinter as tk
from tkinter import messagebox, ttk


class Base64GUI:
    """ base64 加解密工具 """
    def __init__(self, master) -> None:
        self.root = tk.Toplevel(master) 

        input_frame = ttk.LabelFrame(self.root, text="Input")
        input_frame.pack(side="left")
        self.input_box = tk.Text(input_frame)
        self.input_box.pack()
        bframe = tk.Frame(self.root)
        bframe.pack(side="left")
        ebtn = ttk.Button(bframe, text="加密", command=self.encrypto)
        ebtn.pack(padx=5, pady=5)
        dbtn = ttk.Button(bframe, text="解密", command=self.decrypto)
        dbtn.pack(padx=5, pady=5)
        output_frame = ttk.LabelFrame(self.root, text="Output")
        output_frame.pack(side="left")
        self.output_box = tk.Text(output_frame)
        self.output_box.pack()

    def encrypto(self):
        input_text = self.input_box.get(1.0, tk.END)
        res = base64.b64encode(input_text.encode("utf-8")).decode("utf-8")
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(1.0, res)

    def decrypto(self):
        try:
            input_text = self.input_box.get(1.0, tk.END)
            res = base64.b64decode(input_text.encode("utf-8")).decode("utf-8")
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(1.0, res)
        except Exception as e:
            messagebox.showerror("错误", e)
