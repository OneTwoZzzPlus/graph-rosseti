import tkinter as tk
from tkinter import filedialog


class Point:
    def __init__(self, x, y, number):
        m, dx, dy, self.mx, self.my = 50, 30, 30, 560, 460
        self.number = number
        self.x = int(x * m) + dx
        self.y = self.my - (int(y * m) + dy)


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.square_start = None
        self.square_end = None


def save_file():
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        return filename
    except _ as e:
        return ''


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Рисовалка графов (РОССЕТИ) С OneTwoZzz[Plus]')
        self.button_save = tk.Button(root, text="Save", command=self.save_file)
        self.button_save.pack()
        self.button_update = tk.Button(root, text="Update", command=self.update)
        self.button_update.pack()
        self.text = tk.Label(root, text="nothing", font=("Arial", 16))
        self.text.pack()
        self.canvas = tk.Canvas(root, width=Point(0, 0, 0).mx, height=Point(0, 0, 0).my)
        self.canvas.pack()
        self.points = [
            Point(0, 0, 1), Point(0, 8, 2), Point(2, 1.5, 3), Point(0, 3.5, 4), Point(1.5, 6, 5),
            Point(4.5, 4, 6), Point(5.5, 1, 7), Point(4.5, 6.5, 8), Point(7, 5, 9), Point(7, 2, 10),
            Point(8, 0, 11), Point(7, 8, 12), Point(10, 6, 13), Point(10, 3, 14), Point(10, 0, 15)]
        self.draw_points()
        self.lines = []
        self.selected_line = None
        self.start_point = None
        self.end_point = None
        self.koef_square = 5
        self.size_square = 10
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.root.mainloop()

    def update(self):
        pass



    def save_file(self):
        filename = save_file()
        if filename:
            with open(filename, 'w') as file:
                k, s = 1, []
                for line in self.lines:
                    rk_start = int(line.square_start is not None)
                    rk_end = int(line.square_end is not None)
                    s.append(f'{k}\t{line.start.number}\t{line.end.number}\t{rk_start}\t{rk_end}\n')
                    k += 1
                file.writelines(s)
            self.text.config(text="Saved!")

    def draw_points(self):
        for point in self.points:
            self.canvas.create_oval(point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill="blue")

    def on_click(self, event):
        for point in self.points:
            if abs(event.x - point.x) < 5 and abs(event.y - point.y) < 5:
                if self.start_point is None:
                    self.start_point = point
                    self.text.config(text='start point change')
                elif self.start_point != point:
                    self.end_point = point
                    self.text.config(text='end point change')
                    self.lines.append(Line(self.start_point, self.end_point))
                    self.canvas.create_line(self.start_point.x, self.start_point.y,
                                            self.end_point.x, self.end_point.y)
                    with open("lines.txt", "a") as file:
                        file.write(f"({self.start_point.x}, {self.start_point.y}) -> "
                                   f"({self.end_point.x}, {self.end_point.y})\n")
                    self.text.config(text='line draw')
                    self.start_point = None
                    self.end_point = None
                break
        else:
            self.text.config(text='nothing')
            self.start_point = None
            self.end_point = None

    def on_right_click(self, event):
        self.start_point = None
        self.end_point = None
        self.text.config(text='Change line')
        for line in self.lines:
            if line.start.x == line.end.x:
                f = (line.start.x - 5 < event.x < line.start.x + 5 and
                     min(line.start.y, line.end.y) < event.y < max(line.start.y, line.end.y))
            elif line.start.y == line.end.y:
                f = (min(line.start.x, line.end.x) < event.x < max(line.start.x, line.end.x)
                     and (line.start.y - 5 < event.y < line.start.y + 5))
            else:
                f = (min(line.start.x, line.end.x) < event.x < max(line.start.x, line.end.x)
                     and min(line.start.y, line.end.y) < event.y < max(line.start.y, line.end.y))
            if f:
                self.selected_line = line
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Delete Line", command=self.delete_line)
                menu.add_command(label="Draw / Erase 1", command=self.draw_square1)
                menu.add_command(label="Draw / Erase 2", command=self.draw_square2)
                menu.post(event.x_root, event.y_root)
                break

    def delete_line(self):
        self.lines.remove(self.selected_line)
        self.canvas.delete(self.selected_line.square_start)
        self.selected_line.square_start = None
        self.canvas.delete(self.selected_line.square_end)
        self.selected_line.square_end = None
        self.canvas.delete("all")
        self.draw_points()
        for i in range(len(self.lines)):
            size = self.size_square
            self.canvas.create_line(self.lines[i].start.x, self.lines[i].start.y,
                                                    self.lines[i].end.x, self.lines[i].end.y)
            self.selected_line = self.lines[i]
            self.redraw_square()
        self.selected_line = None

        with open("lines.txt", "w") as file:
            for line in self.lines:
                file.write(f"({line.start.x}, {line.start.y}) -> "
                           f"({line.end.x}, {line.end.y})\n")

    def redraw_square(self):
        if self.selected_line.square_start is not None:
            sx, sy = self.selected_line.start.x, self.selected_line.start.y
            ex, ey = self.selected_line.end.x, self.selected_line.end.y
            mid_x = sx + ((ex - sx) // self.koef_square)
            mid_y = sy + ((ey - sy) // self.koef_square)
            size = self.size_square
            self.canvas.create_rectangle(mid_x - size // 2, mid_y - size // 2,
                                         mid_x + size // 2, mid_y + size // 2,
                                         fill="red", tag="square")
        if self.selected_line.square_end is not None:
            sx, sy = self.selected_line.start.x, self.selected_line.start.y
            ex, ey = self.selected_line.end.x, self.selected_line.end.y
            mid_x = ex + ((sx - ex) // self.koef_square)
            mid_y = ey + ((sy - ey) // self.koef_square)
            size = self.size_square
            self.canvas.create_rectangle(mid_x - size // 2, mid_y - size // 2,
                                         mid_x + size // 2, mid_y + size // 2,
                                         fill="red", tag="square")

    def draw_square1(self):
        sx, sy = self.selected_line.start.x, self.selected_line.start.y
        ex, ey = self.selected_line.end.x, self.selected_line.end.y
        mid_x = sx + ((ex-sx) // self.koef_square)
        mid_y = sy + ((ey-sy) // self.koef_square)

        if self.selected_line.square_start is None:
            size = self.size_square
            self.selected_line.square_start = self.canvas.create_rectangle(mid_x - size // 2, mid_y - size // 2,
                                                                           mid_x + size // 2, mid_y + size // 2,
                                                                           fill="red", tag="square")
        else:
            self.canvas.delete(self.selected_line.square_start)
            self.selected_line.square_start = None

    def draw_square2(self):
        sx, sy = self.selected_line.start.x, self.selected_line.start.y
        ex, ey = self.selected_line.end.x, self.selected_line.end.y
        mid_x = ex + ((sx - ex) // self.koef_square)
        mid_y = ey + ((sy - ey) // self.koef_square)

        if self.selected_line.square_end is None:
            size = self.size_square
            self.selected_line.square_end = self.canvas.create_rectangle(mid_x - size // 2, mid_y - size // 2,
                                                                         mid_x + size // 2, mid_y + size // 2,
                                                                         fill="red", tag="square")
        else:
            self.canvas.delete(self.selected_line.square_end)
            self.selected_line.square_end = None


root = tk.Tk()
app = App(root)
