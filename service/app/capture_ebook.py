#!/usr/bin/env python3
"""
Capture page-by-page screenshots from an online book viewer.

⚠️ IMPORTANT
- Use this script ONLY for lawful, personal use. Check the website's ToS and applicable copyright laws.
- Do NOT share or redistribute captured images without permission.

Requires:
    Python 3.x
    pyautogui
    pynput
"""

import argparse
import os
import time

import pyautogui
from pynput import mouse


def wait_start_via_click():
    """Wait for a single left-click anywhere, then return."""
    print("[Wait] Click on the target window once to start...")

    def on_click(x, y, button, pressed):
        from pynput.mouse import Button
        if pressed and button == Button.left:
            return False  # stop after first left click

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    print("[OK] Click detected. Starting in 1.0s...")
    time.sleep(1.0)


def main():
    parser = argparse.ArgumentParser(
        description="Take sequential screenshots of a viewport region and press a key to advance pages."
    )
    parser.add_argument("--outdir", default="data", help="Output directory (default: data)")
    parser.add_argument("--count", type=int, default=50, help="Number of pages to capture")
    parser.add_argument("--start-index", type=int, default=0, help="Start index for filenames (default: 0)")
    parser.add_argument("--left", type=int, default=300, help="Capture region left (pixels)")
    parser.add_argument("--top", type=int, default=300, help="Capture region top (pixels)")
    parser.add_argument("--width", type=int, default=800, help="Capture region width (pixels)")
    parser.add_argument("--height", type=int, default=600, help="Capture region height (pixels)")
    parser.add_argument("--next-key", default="right", help="Key to go to next page (default: right)")
    parser.add_argument("--per-page-wait", type=float, default=2.0, help="Seconds to wait before each capture (default: 2.0)")
    parser.add_argument("--filename-digits", type=int, default=4, help="Zero-padding digits in filenames (default: 4)")
    parser.add_argument("--no-fail-safe", action="store_true", help="Disable pyautogui.FAILSAFE")
    args = parser.parse_args()

    # Configure PyAutoGUI
    pyautogui.FAILSAFE = not args.no_fail_safe
    pyautogui.PAUSE = 0.1

    # Sanity checks
    if args.count <= 0:
        print("Nothing to capture: --count must be >= 1")
        return
    if args.width <= 0 or args.height <= 0:
        print("Invalid region: --width and --height must be positive.")
        return

    dir_path = os.path.join("/data",args.outdir)
    os.makedirs(dir_path, exist_ok=True)

    region = (args.left, args.top, args.width, args.height)
    print("=== Capture Settings ===")
    print(f"Output dir       : {os.path.abspath(dir_path)}")
    print(f"Pages (count)    : {args.count}")
    print(f"Start index      : {args.start_index}")
    print(f"Region (L,T,W,H) : {region}")
    print(f"Next-page key    : {args.next_key}")
    print(f"Per-page wait    : {args.per_page_wait}s")   # ← 修正済み
    print(f"Filename digits  : {args.filename_digits}")
    print(f"FAILSAFE         : {pyautogui.FAILSAFE}")
    print("========================")

    # Always wait for click before starting
    wait_start_via_click()

    print("[Info] Ensure the target viewer window is focused.")

    idx = args.start_index
    try:
        for _ in range(args.count):
            time.sleep(args.per_page_wait)

            img = pyautogui.screenshot(region=region)
            filename = os.path.join(dir_path, str(idx).zfill(args.filename_digits) + ".png")
            img.save(filename)
            print("Created", filename, flush=True)

            pyautogui.press(args.next_key)
            idx += 1

        print("Done.")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully.")


if __name__ == "__main__":
    main()
