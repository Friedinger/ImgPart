from PIL import ImageGrab, Image, ImageTk
from io import BytesIO
import win32clipboard
import tkinter as gui

class imgPart:

	def __init__(self):
		self.window = gui.Tk()
		self.window.title("img.part - Load Image")
		self.window.attributes('-topmost',1)
		self.loadImageBtn = gui.Button(self.window, text="Load image from clipboard", command=self.loadImage)
		self.loadImageBtn.pack()
		self.window.mainloop()

	def loadImage(self):
		if hasattr(self, "noImageLabel"): self.noImageLabel.pack_forget()
		self.image = ImageGrab.grabclipboard()
		try:
			self.image.size
		except AttributeError:
			self.noImageLabel = gui.Label(self.window, text="No image in clipboard")
			self.noImageLabel.pack()
			return
		if hasattr(self, "self.canvas"): self.canvas.destroy()
		self.canvas = gui.Canvas(self.window, width=self.image.width, height=self.image.height)
		self.photo = ImageTk.PhotoImage(self.image)
		self.canvas.create_image(0, 0, image=self.photo, anchor=gui.NW)
		self.canvas.bind("<Motion>", self.drawSplitLine)
		self.canvas.bind("<Button-1>", self.splitImage)
		self.canvas.pack()
		self.window.title("img.part - Split Image")
		self.loadImageBtn.pack_forget()

	def drawSplitLine(self, event):
		self.canvas.delete("line")
		self.canvas.create_line(0, event.y, self.image.width, event.y, fill="red", tags="line")

	def splitImage(self, event):
		ySplit = event.y
		width, height = self.image.size
		topImage = self.image.crop((0, 0, width, ySplit))
		bottomImage = self.image.crop((0, ySplit, width, height))
		self.canvas.unbind("<Motion>")
		self.canvas.unbind("<Button-1>")
		saveTopImageBtn = gui.Button(self.window, text="Save top image to clipboard", command=lambda:self.saveImageToClipboard(topImage))
		saveTopImageBtn.pack()
		saveBottomImageBtn = gui.Button(self.window, text="Save bottom image to clipboard", command=lambda:self.saveImageToClipboard(bottomImage))
		saveBottomImageBtn.pack()
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

if __name__ == '__main__':
	imgPart()
