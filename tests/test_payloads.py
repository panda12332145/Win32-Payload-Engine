"""Testes do Win32-Payload-Engine (GDI mockado — roda em qualquer SO)."""
import os
import sys
import types
from unittest.mock import MagicMock

# Faz mock dos módulos pywin32 ANTES de importar o engine
for name in ("win32gui", "win32con", "win32api"):
    mod = types.ModuleType(name)
    mod.__dict__.update({
        "GetDC": MagicMock(return_value=1),
        "ReleaseDC": MagicMock(),
        "GetDesktopWindow": MagicMock(return_value=1),
        "PatBlt": MagicMock(),
        "DrawIcon": MagicMock(),
        "DrawIconEx": MagicMock(),
        "Ellipse": MagicMock(),
        "Rectangle": MagicMock(),
        "CreatePen": MagicMock(return_value=1),
        "SelectObject": MagicMock(),
        "MoveToEx": MagicMock(),
        "LineTo": MagicMock(),
        "LoadIcon": MagicMock(return_value=1),
        "GetStockObject": MagicMock(return_value=1),
        "FillRect": MagicMock(),
        "DeleteObject": MagicMock(),
        "CreateSolidBrush": MagicMock(return_value=1),
        "CreateRectRgn": MagicMock(return_value=1),
        "CombineRgn": MagicMock(),
        "SelectClipRgn": MagicMock(),
        "SM_CXSCREEN": 0,
        "SM_CYSCREEN": 1,
        "BLACKNESS": 0x00000042,
        "IDI_APPLICATION": 32512,
        "IDI_ERROR": 32513,
        "IDI_WARNING": 32514,
        "IDI_QUESTION": 32515,
        "IDI_INFORMATION": 32516,
        "IDI_HAND": 32513,
        "PS_SOLID": 0,
        "WHITENESS": 0x00FF0062,
        "SRCCOPY": 0x00CC0020,
        "RGB": lambda r, g, b: r | (g << 8) | (b << 16),
        "GetSystemMetrics": MagicMock(side_effect=lambda i: 800 if i == 0 else 600),
    })
    sys.modules[name] = mod

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.payloads import ALL_PAYLOADS, IconCubePayload, IconsPayload
from src.engine import list_payloads, run_animation_loop


def test_all_payloads_complete():
    names = list_payloads()
    assert len(names) >= 6
    for legacy in ("RectanglesPayload", "CirclesPayload", "SpiralPayload",
                   "SunraysPayload", "IconsPayload", "IconCubePayload"):
        assert legacy in names, f"faltando {legacy}"


def test_every_payload_draws_with_mock_hdc():
    for P in ALL_PAYLOADS:
        p = P()
        p.draw(1, 800, 600)   # não deve levantar exceção com mocks


def test_icon_cube_advances_frames():
    p = IconCubePayload()
    p.draw(1, 800, 600)
    assert (p.A, p.B, p.C) != (0.0, 0.0, 0.0)


def test_engine_once_run():
    run_animation_loop(delay=0.0, once=True)   # não deve travar


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")
