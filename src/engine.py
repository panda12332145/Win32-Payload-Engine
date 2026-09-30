import win32gui
import win32con
import win32api
import time
from .payloads import ALL_PAYLOADS


def list_payloads():
    """Lista os nomes dos payloads registrados."""
    return [p.__name__ for p in ALL_PAYLOADS]


def run_animation_loop(delay: float = 0.05, once: bool = False):
    """Percorre todos os payloads de animação sequencialmente.
    Com once=False repete indefinidamente (Ctrl+C encerra)."""
    screen_w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    hwnd = win32gui.GetDesktopWindow()
    try:
        while True:
            for PayloadClass in ALL_PAYLOADS:
                payload = PayloadClass()
                hdc = win32gui.GetDC(hwnd)
                try:
                    payload.draw(hdc, screen_w, screen_h)
                finally:
                    win32gui.ReleaseDC(hwnd, hdc)
                time.sleep(delay)
            if once:
                break
    except KeyboardInterrupt:
        print("\n[INFO] Encerrado pelo usuário.")
    finally:
        print("[INFO] Engine finalizado.")


if __name__ == "__main__":
    run_animation_loop()
