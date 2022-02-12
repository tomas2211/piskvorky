from turtle import back
import PySimpleGUI as sg

sg.theme('Black')


class Okno:
    def __init__(self, title, size=(20, 20), cellSizePx=30):
        self.size = size
        self.cellSize = cellSizePx

        self.textbox = sg.Text("")
        self.canvas = sg.Canvas(
            size=(size[0] * cellSizePx, size[1] * cellSizePx), background_color="white")
        layout = [
            [self.textbox],
            [self.canvas],
        ]
        self.window = sg.Window(title, layout)
        self.window.read(10)  # let the window show up
        self.canvas.bind("<Button-1>", None)

    def nakreslitMrizku(self):
        self.canvas.TKCanvas.delete("all")  # clear whole canvas

        w = self.size[0] * self.cellSize
        h = self.size[1] * self.cellSize

        for i in range(1, self.size[0]):
            self.canvas.TKCanvas.create_line(
                i*self.cellSize, 0, i*self.cellSize, h, fill="gray")

        for i in range(1, self.size[1]):
            self.canvas.TKCanvas.create_line(
                0, i*self.cellSize, w, i*self.cellSize, fill="gray")

    def zobrazitText(self, txt):
        self.textbox.update(txt)

    def pockatNaKlik(self):
        event, values = self.window.read()
        if(event != "<Button-1>"):
            return
        x = self.canvas.user_bind_event.x
        y = self.canvas.user_bind_event.y
        return int(x / self.cellSize), int(y / self.cellSize)

    def nakreslitKrizek(self, pos):
        x, y = pos
        x *= self.cellSize
        y *= self.cellSize
        sz = self.cellSize-3
        self.canvas.TKCanvas.create_line(
            x+3, y+3, x+sz, y+sz, width=3, fill="orange red")
        self.canvas.TKCanvas.create_line(
            x+3, y+sz, x+sz, y+3, width=3, fill="orange red")

    def nakreslitKolecko(self, pos):
        x, y = pos
        x *= self.cellSize
        y *= self.cellSize
        sz = self.cellSize-3
        self.canvas.TKCanvas.create_oval(
            x+3, y+3, x+sz, y+sz, width=3, outline="SlateBlue2")

    def zobrazitUpozorneni(self, text):
        sg.popup(text)

    def zavrit(self):
        self.window.close()


CROSS = 1
CIRCLE = 2


class HraciPlan:
    def __init__(self, size=(20, 20)):
        self.size = size
        self.plan = [[0 for c in range(size[0])] for r in range(size[1])]
        self.lastMove = None

    def jePoleVolne(self, pos):
        return self.plan[pos[1]][pos[0]] == 0

    def pridatKrizek(self, pos):
        self.lastMove = pos
        self.plan[pos[1]][pos[0]] = CROSS

    def pridatKolecko(self, pos):
        self.lastMove = pos
        self.plan[pos[1]][pos[0]] = CIRCLE

    def countSignsInDirection(self, pos, delta, sign, count=0):
        if(pos[0] < 0 or pos[0] >= self.size[0]):  # outside plan
            return count
        if(pos[1] < 0 or pos[1] >= self.size[1]):
            return count
        if(self.plan[pos[1]][pos[0]] != sign):  # different sign
            return count

        newPos = (pos[0] + delta[0], pos[1] + delta[1])
        return self.countSignsInDirection(newPos, delta, sign, count + 1)

    def countSigns(self, pos, delta):
        sign = self.plan[pos[1]][pos[0]]
        countPos = self.countSignsInDirection(
            pos, delta, sign)  # try in both directions
        countNeg = self.countSignsInDirection(
            pos, (-delta[0], -delta[1]), sign)
        return countPos + countNeg - 1  # the start is counted twice

    def vyhralPosledniTah(self, znakuNaVyhru=5):
        if self.lastMove is None:
            print("Volani vyhralPosledniTah() pred jakymkoliv tahem.")
            return False
        sign = self.plan[self.lastMove[1]][self.lastMove[0]]
        for delta in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            znaku = self.countSigns(self.lastMove, delta)
            if znaku >= znakuNaVyhru:
                return True


