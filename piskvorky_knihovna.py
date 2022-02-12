import PySimpleGUI as sg
from typing import Tuple

sg.theme('Black')

CROSS = 1
CIRCLE = 2
DEFAULT_SIZE = (20, 20)
DEFAULT_CELL_SIZE = 30


class Okno:
    def __init__(self, title: str, size: Tuple[int, int] = DEFAULT_SIZE, cellSizePx: int = DEFAULT_CELL_SIZE):
        """Vytvari okno pro hru

        Args:
            title (str): titulek okna
            size (Tuple[int, int], optional): Velikost hraciho planu (v poctu bunek). Defaults to (20, 20).
            cellSizePx (int, optional): Velikost bunky v px. Defaults to 30.
        """
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
        """Nakresli hraci mrizku v okne, smaze vse dosud pridane.
        """
        self.canvas.TKCanvas.delete("all")  # clear whole canvas

        w = self.size[0] * self.cellSize
        h = self.size[1] * self.cellSize

        for i in range(1, self.size[0]):
            self.canvas.TKCanvas.create_line(
                i*self.cellSize, 0, i*self.cellSize, h, fill="gray")

        for i in range(1, self.size[1]):
            self.canvas.TKCanvas.create_line(
                0, i*self.cellSize, w, i*self.cellSize, fill="gray")

    def zobrazitText(self, text: str):
        """Zobrazi text oznamujici stav hry

        Args:
            text (str): text
        """
        self.textbox.update(text)

    def pockatNaKlik(self) -> Tuple[int, int]:
        """Vycka na kliknuti do hraciho pole

        Returns:
            Tuple[int, int]: souradnice dane bunky
        """
        while self.window.read()[0] != "<Button-1>":
            pass
        x = self.canvas.user_bind_event.x
        y = self.canvas.user_bind_event.y
        return int(x / self.cellSize), int(y / self.cellSize)

    def nakreslitKrizek(self, x: int, y: int):
        """Nakresli krizek do dane bunky v poli

        Args:
            x (int): souradnice x
            y (int): souradnice y
        """
        x *= self.cellSize
        y *= self.cellSize
        sz = self.cellSize-3
        self.canvas.TKCanvas.create_line(
            x+3, y+3, x+sz, y+sz, width=3, fill="orange red")
        self.canvas.TKCanvas.create_line(
            x+3, y+sz, x+sz, y+3, width=3, fill="orange red")

    def nakreslitKolecko(self, x: int, y: int):
        """Nakresli kolecko do dane bunky v poli

        Args:
            x (int): souradnice x
            y (int): souradnice y
        """
        x *= self.cellSize
        y *= self.cellSize
        sz = self.cellSize-3
        self.canvas.TKCanvas.create_oval(
            x+3, y+3, x+sz, y+sz, width=3, outline="SlateBlue2")

    def zobrazitUpozorneni(self, text: str):
        """Zobrazi upozorneni (popup okno)

        Args:
            text (str): text upozorneni
        """
        sg.popup(text)

    def zavrit(self):
        """Zavre okno
        """
        self.window.close()


class HraciPlan:
    def __init__(self, size: Tuple[int, int] = DEFAULT_SIZE):
        """Vytvori herni plan

        Args:
            size (Tuple[int, int], optional): Velikost herniho planu. Defaults to (20, 20).
        """
        self.size = size
        self.plan = [[0 for c in range(size[0])] for r in range(size[1])]
        self.lastMove = None

    def jePoleVolne(self, x: int, y: int) -> bool:
        """Vraci True pokud je pole volne

        Args:
            x (int): souradnice x
            y (int): souradnice y

        Returns:
            bool: True pokud je volne
        """
        return self.plan[y][x] == 0

    def pridatKrizek(self, x: int, y: int):
        """Prida krizek na pozici v hernim planu

        Args:
            x (int): souradnice x
            y (int): souradnice y
        """
        self.lastMove = (x, y)
        self.plan[y][x] = CROSS

    def pridatKolecko(self, x: int, y: int):
        """Prida kolecko na pozici v hernim planu

        Args:
            x (int): souradnice x
            y (int): souradnice y
        """
        self.lastMove = (x, y)
        self.plan[y][x] = CIRCLE

    def countSignsInDirection(self, pos: Tuple[int, int], delta: Tuple[int, int], sign: int, count: int = 0) -> int:
        """Recursively explores the plan in one direction while the cells have the same sign and counts them

        Args:
            pos (Tuple[int, int]): starting position
            delta (Tuple[int, int]): direction of exploration
            sign (int): expected sign
            count (int, optional): count, used for recursion. Defaults to 0.

        Returns:
            int: number of signs in the direction (including `pos`)
        """
        if(pos[0] < 0 or pos[0] >= self.size[0]):  # outside plan
            return count
        if(pos[1] < 0 or pos[1] >= self.size[1]):
            return count
        if(self.plan[pos[1]][pos[0]] != sign):  # different sign
            return count

        newPos = (pos[0] + delta[0], pos[1] + delta[1])
        return self.countSignsInDirection(newPos, delta, sign, count + 1)

    def countSigns(self, pos: Tuple[int, int], delta: Tuple[int, int]) -> int:
        """Counts the number of same signs in a direction from position. Considers both orientations of the direction.

        Args:
            pos (Tuple[int, int]): starting position (specifies the sign to look for)
            delta (Tuple[int, int]): direction, considers (dx, dy) and (-dx, -dy)

        Returns:
            int: count of the same signs
        """
        sign = self.plan[pos[1]][pos[0]]
        countPos = self.countSignsInDirection(
            pos, delta, sign)  # try in both directions
        countNeg = self.countSignsInDirection(
            pos, (-delta[0], -delta[1]), sign)
        return countPos + countNeg - 1  # the start is counted twice

    def vyhralPosledniTah(self, znakuNaVyhru: int = 5) -> bool:
        """Zkontroluje jestli posledni tah byl vyherni

        Args:
            znakuNaVyhru (int, optional): pocet znaku nutnych na vyhru. Defaults to 5.

        Returns:
            bool: True pokud posledni tah vyhral
        """
        if self.lastMove is None:
            print("Volani vyhralPosledniTah() pred jakymkoliv tahem.")
            return False
        sign = self.plan[self.lastMove[1]][self.lastMove[0]]
        for delta in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            znaku = self.countSigns(self.lastMove, delta)
            if znaku >= znakuNaVyhru:
                return True
