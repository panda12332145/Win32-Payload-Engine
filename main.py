#!/usr/bin/env python3
"""CLI do Win32 Payload Engine (Windows/GDI)."""
import argparse

from src.engine import run_animation_loop, list_payloads


def main():
    ap = argparse.ArgumentParser(description="Win32 GDI Payload Engine (lab)")
    ap.add_argument("--list", action="store_true", help="lista payloads")
    ap.add_argument("--delay", type=float, default=0.05, help="delay entre payloads (s)")
    ap.add_argument("--once", action="store_true", help="executa uma vez e sai")
    args = ap.parse_args()
    if args.list:
        print("\n".join(list_payloads()))
        return
    run_animation_loop(delay=args.delay, once=args.once)


if __name__ == "__main__":
    main()
