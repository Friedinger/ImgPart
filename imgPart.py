from PIL import ImageGrab, Image, ImageTk
from io import BytesIO
import win32clipboard
from tkinter import *
from tkinter.ttk import *
import customtkinter as gui

class ImgPart:

	def __init__(self):
		self.start()

	def start(self):
		gui.set_appearance_mode("System")
		gui.set_default_color_theme("blue")
		self.window = gui.CTk()
		self.window.after(0, lambda: self.window.wm_state("zoomed"))
		style = Style()
		style.configure("TFrame", background="gray14")
		self.prepareGui()
		self.window.mainloop()

	def prepareGui(self):
		self.window.title("img.part - Load Image")
		self.buttonFrame = Frame(self.window)
		self.buttonFrame.pack(side=BOTTOM, pady=10)
		self.loadImageBtn = gui.CTkButton(self.buttonFrame, text="Load image from clipboard", command=self.loadImage)
		self.loadImageBtn.pack(side=LEFT, padx=10)

	def loadImage(self):
		if hasattr(self, "noImageLabel"): self.noImageLabel.destroy()
		self.image = ImageGrab.grabclipboard()
		try:
			self.image.size
		except AttributeError:
			self.noImageLabel = gui.CTkLabel(self.buttonFrame, text="No image in clipboard")
			self.noImageLabel.pack(side=RIGHT, padx=10)
			return
		if hasattr(self, "self.canvas"): self.canvas.destroy()
		aspectRatio = self.image.width / self.image.height
		width, height = self.window.winfo_width(), self.window.winfo_height()-50
		screenAspectRatio = width / height
		if aspectRatio > screenAspectRatio:
			print (1)
			image = self.image.resize((width, int(width / aspectRatio)))
		else:
			print (2)
			image = self.image.resize((int(height * aspectRatio), height))
		self.canvas = gui.CTkCanvas(self.window, width=image.width, height=image.height, relief="flat", highlightthickness=0)
		self.photo = ImageTk.PhotoImage(image)
		self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
		self.canvas.bind("<Motion>", self.drawSplitLine)
		self.canvas.bind("<Button-1>", self.splitImage)
		self.canvas.pack()
		self.splitImageLabel = gui.CTkLabel(self.buttonFrame, text="Select where to split the image")
		self.splitImageLabel.pack(side=LEFT, padx=10)
		self.window.title("img.part - Split Image")
		self.loadImageBtn.destroy()

	def drawSplitLine(self, event):
		self.canvas.delete("line")
		self.canvas.create_line(0, event.y, self.canvas.winfo_width(), event.y, fill="red", tags="line")

	def splitImage(self, event):
		width, height = self.image.size
		ySplit = height * (event.y / self.canvas.winfo_height())
		topImage = self.image.crop((0, 0, width, ySplit))
		bottomImage = self.image.crop((0, ySplit, width, height))
		self.canvas.unbind("<Motion>")
		self.canvas.unbind("<Button-1>")
		self.splitImageLabel.destroy()
		saveTopImageBtn = gui.CTkButton(self.buttonFrame, text="Save top image to clipboard", command=lambda:self.saveImageToClipboard(topImage))
		saveTopImageBtn.pack(side=LEFT, padx=10)
		saveBottomImageBtn = gui.CTkButton(self.buttonFrame, text="Save bottom image to clipboard", command=lambda:self.saveImageToClipboard(bottomImage))
		saveBottomImageBtn.pack(side=LEFT, padx=10)
		resetImageBtn = gui.CTkButton(self.buttonFrame, text="Reset image", command=lambda:self.resetImage())
		resetImageBtn.pack(side=RIGHT, padx=10)
		self.window.title("img.part - Save Image")

	def saveImageToClipboard(self, image):
		output = BytesIO()
		image.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
		win32clipboard.CloseClipboard()
	
	def resetImage(self):
		for widget in self.window.winfo_children():
			widget.destroy()
		self.prepareGui()

if __name__ == "__main__":
	ImgPart()
