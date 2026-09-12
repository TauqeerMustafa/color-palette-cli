#!/usr/bin/env python3
"""
color-palette-cli: Color palette generator & WCAG contrast checker.
"""
import argparse, math, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

__version__ = "1.0.0"

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b):
    a = [v / 255.0 for v in [r, g, b]]
    a = [((v + 0.055) / 1.055) ** 2.4 if v > 0.03928 else v / 12.92 for v in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def contrast_ratio(hex1, hex2):
    lum1 = luminance(*hex_to_rgb(hex1))
    lum2 = luminance(*hex_to_rgb(hex2))
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return round((brightest + 0.05) / (darkest + 0.05), 2)

def main():
    parser = argparse.ArgumentParser(description="🎨 color-palette-cli: Palette generator & contrast checker")
    parser.add_argument("hex", nargs="?", default="#3B82F6", help="Base HEX color (default: #3B82F6)")
    args = parser.parse_args()
    
    c_white = contrast_ratio(args.hex, "#FFFFFF")
    c_black = contrast_ratio(args.hex, "#000000")
    
    print("=" * 60)
    print(f"🎨 COLOR PALETTE & WCAG REPORT FOR {args.hex.upper()}")
    print("=" * 60)
    print(f"HEX Code         : {args.hex.upper()}")
    print(f"RGB Values       : {hex_to_rgb(args.hex)}")
    print("-" * 60)
    print(f"Contrast on White (#FFF) : {c_white}:1 ➔ {'✅ PASS (WCAG AA)' if c_white >= 4.5 else '❌ FAIL'}")
    print(f"Contrast on Black (#000) : {c_black}:1 ➔ {'✅ PASS (WCAG AA)' if c_black >= 4.5 else '❌ FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
