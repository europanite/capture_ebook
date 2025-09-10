# [Capture ebook](https://github.com/europanite/capture_ebook "Capture ebook")

This script captures sequential screenshots of an online ebook page viewer.  
It automatically saves each page as an image file and simulates pressing a key to advance pages.

---

## ⚠️ Disclaimer
- **Use this script ONLY for lawful and personal purposes.**  
- Respect the Terms of Service (ToS) of the website or ebook service you use.  
- **Do NOT share, redistribute, or publish the captured images without permission.**  
- You are fully responsible for ensuring compliance with copyright laws.

---


## Usage

Run the script with default settings:
```bash
python capture_ebook.py
```

Example with custom arguments:
```bash
python capture_ebook.py   --outdir screenshots   --count 100   --left 500 --top 100 --width 800 --height 900   --next-key right   --per-page-wait 2.5
```

---

## Arguments

| Option              | Description                                   |
|---------------------|-----------------------------------------------|
| `--outdir`          | Output directory                              |
| `--count`           | Number of pages to capture                    |
| `--start-index`     | Starting filename index                       |
| `--left`            | Left pixel of capture region                  |
| `--top`             | Top pixel of capture region                   |
| `--width`           | Width of capture region                       |
| `--height`          | Height of capture region                      |
| `--next-key`        | Key used to move to next page                 |
| `--pre-wait`        | Seconds to wait before starting               |
| `--per-page-wait`   | Seconds to wait before each screenshot        |
| `--filename-digits` | Number of digits in zero-padded filenames     |
| `--no-fail-safe`    | Disable PyAutoGUI failsafe (Esc = abort)      |

---

## Notes
- Place your browser window so the ebook page fully fits within the capture region.  
- Ensure each page is fully loaded before the script captures it.  
- You can abort safely by moving your mouse to the **top-left corner** (unless `--no-fail-safe` is used).  
