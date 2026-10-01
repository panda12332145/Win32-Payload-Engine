import win32gui
import win32con
import win32api
import time
import random
import math


class Payload:
    """Classe base para todos os payloads de animação."""
    def draw(self, hdc, w, h):
        raise NotImplementedError


class RectanglesPayload(Payload):
    def draw(self, hdc, w, h):
        for _ in range(300):
            rect = (random.randint(0, w-100), random.randint(0, h-100),
                    random.randint(50, 150), random.randint(50, 150))
            brush = win32gui.CreateSolidBrush(win32api.RGB(*[random.randint(0,255) for _ in range(3)]))
            win32gui.FillRect(hdc, rect, brush)


class CirclesPayload(Payload):
    def draw(self, hdc, w, h):
        for _ in range(300):
            x, y = random.randint(0, w-50), random.randint(0, h-50)
            r = random.randint(20, 50)
            win32gui.Ellipse(hdc, x, y, x + 2*r, y + 2*r)


class SpiralPayload(Payload):
    def draw(self, hdc, w, h):
        cx, cy = w // 2, h // 2
        for i in range(300):
            angle = i * (360 / 300)
            ri = i * 5
            x1 = int(cx + ri * math.cos(math.radians(angle)))
            y1 = int(cy + ri * math.sin(math.radians(angle)))
            x2 = int(cx + (i+1) * 5 * math.cos(math.radians(angle)))
            y2 = int(cy + (i+1) * 5 * math.sin(math.radians(angle)))
            color = win32api.RGB(*[random.randint(0, 255) for _ in range(3)])
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, color)
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)


class SunraysPayload(Payload):
    def draw(self, hdc, w, h):
        cx, cy, length = w // 2, h // 2, 100
        for i in range(300):
            angle = i * (360 / 300)
            x1 = int(cx + length * math.cos(math.radians(angle)))
            y1 = int(cy + length * math.sin(math.radians(angle)))
            x2 = int(cx + 2 * length * math.cos(math.radians(angle)))
            y2 = int(cy + 2 * length * math.sin(math.radians(angle)))
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(*[random.randint(0, 255) for _ in range(3)]))
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)


class IconsPayload(Payload):
    """Ícones do sistema sorteados em posições aleatórias (portado de as.py)."""
    name = "ícones_aleatórios"
    _ICONS = ["IDI_APPLICATION", "IDI_ERROR", "IDI_WARNING",
              "IDI_QUESTION", "IDI_INFORMATION", "IDI_HAND"]

    def draw(self, hdc, w, h):
        for _ in range(60):
            x = random.randint(0, max(w - 32, 1))
            y = random.randint(0, max(h - 32, 1))
            icon_id = getattr(win32con, random.choice(self._ICONS))
            hicon = win32gui.LoadIcon(None, icon_id)
            win32gui.DrawIcon(hdc, x, y, hicon)


class IconCubePayload(Payload):
    """Cubo rotativo de ícones 3D (portado de "as - Copia.py").
    Cada chamada a draw() avança um quadro da rotação."""
    name = "cubo_de_ícones"

    _ICONS = ["IDI_APPLICATION", "IDI_ERROR", "IDI_WARNING",
              "IDI_QUESTION", "IDI_INFORMATION", "IDI_HAND"]

    def __init__(self, cube=100, dist=200, focal=200):
        self.cube = cube
        self.dist = dist
        self.focal = focal
        self.A = self.B = self.C = 0.0

    @staticmethod
    def _rot(i, j, k, A, B, C):
        x = (j * math.sin(A) * math.sin(B) * math.cos(C)
             - k * math.cos(A) * math.sin(B) * math.cos(C)
             + j * math.cos(A) * math.sin(C)
             + k * math.sin(A) * math.sin(C)
             + i * math.cos(B) * math.cos(C))
        y = (j * math.cos(A) * math.cos(C)
             + k * math.sin(A) * math.cos(C)
             - j * math.sin(A) * math.sin(B) * math.sin(C)
             + k * math.cos(A) * math.sin(B) * math.sin(C)
             - i * math.cos(B) * math.sin(C))
        z = (k * math.cos(A) * math.cos(B)
             - j * math.sin(A) * math.cos(B)
             + i * math.sin(B))
        return x, y, z

    def draw(self, hdc, w, h):
        win32gui.PatBlt(hdc, 0, 0, w, h, win32con.BLACKNESS)
        icons = [win32gui.LoadIcon(None, getattr(win32con, n))
                 for n in self._ICONS]
        c = self.cube
        step = 20
        faces = [
            (-c, range(-c, c + step, step), icons[0]),   # X-
            (c, range(-c, c + step, step), icons[1]),    # X+
            (-c, range(-c, c + step, step), icons[2]),   # Y-
            (c, range(-c, c + step, step), icons[3]),    # Y+
            (-c, range(-c, c + step, step), icons[4]),   # Z-
            (c, range(-c, c + step, step), icons[5]),    # Z+
        ]
        for idx, (fixed, rng, icon) in enumerate(faces):
            for r1 in rng:
                for r2 in rng:
                    if idx < 2:
                        i, j, k = fixed, r1, r2
                    elif idx < 4:
                        i, j, k = r1, fixed, r2
                    else:
                        i, j, k = r1, r2, fixed
                    x, y, z = self._rot(i, j, k, self.A, self.B, self.C)
                    z += self.dist
                    if z > 0:
                        ooz = 1 / z
                        xp = int(w / 2 + self.focal * ooz * x)
                        yp = int(h / 2 - self.focal * ooz * y)
                        win32gui.DrawIcon(hdc, xp, yp, icon)
        self.A += 0.03
        self.B += 0.02
        self.C += 0.01


# Registro de todos os payloads disponíveis
ALL_PAYLOADS = [
    RectanglesPayload, CirclesPayload, SpiralPayload, SunraysPayload,
    IconsPayload, IconCubePayload,
]
