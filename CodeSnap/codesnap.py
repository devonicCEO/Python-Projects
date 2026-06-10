import datetime
import os
import sys
import time
from pathlib import Path
import tkinter as tk

try:
    import pyperclip
except Exception:
    pyperclip = None
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pygments import lex
from pygments.lexers import guess_lexer
from pygments.lexers.special import TextLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Token
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


APP = "CodeSnap"
AUTHOR = "devonicCEO"
GITHUB = "github.com/devonicCEO"
VERSION = "1.0"

bg = "#1e1f29"
fg = "#d4d4d4"
pad = 30
font_size = 20
line_numbers = True  
console = Console()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def grad_header(text: str) -> Text:
    colors = ["#00e5ff", "#9d4edd", "#ff5faf"]  
    out = Text()
    if not text:
        return out
    n = len(text)
    for i, ch in enumerate(text):
        t = i / max(1, n - 1)
        if t < 0.5:
            c1, c2 = colors[0], colors[1]
            k = t * 2
        else:
            c1, c2 = colors[1], colors[2]
            k = (t - 0.5) * 2
        rgb1 = tuple(int(c1[j : j + 2], 16) for j in (1, 3, 5))
        rgb2 = tuple(int(c2[j : j + 2], 16) for j in (1, 3, 5))
        r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * k)
        g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * k)
        b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * k)
        out.append(ch, style=f"bold rgb({r},{g},{b})")
    return out


def center_line(text: str, width: int = 69) -> str:
    clean = text
    if len(clean) > width:
        clean = clean[:width]
    left = (width - len(clean)) // 2
    right = width - len(clean) - left
    return " " * left + clean + " " * right


def box_row(text: str = "", width: int = 71, style: str = "white"):
    row = Text()
    row.append("║", style="bold #00e5ff")
    row.append(text[:width].ljust(width), style=style)
    row.append("║", style="bold #00e5ff")
    console.print(row)



def print_main_banner():
    w = 81
    console.print("[bold #00e5ff]╔" + "═" * w + "╗[/]")
    box_row("", width=w)
    box_row("     ██████╗  ██████╗ ██████╗ ███████╗███████╗███╗   ██╗ █████╗ ██████╗", width=w, style="#8be9fd")
    box_row("    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝██╔════╝████╗  ██║██╔══██╗██╔══██╗", width=w, style="#8be9fd")
    box_row("    ██║      ██║   ██║██║  ██║█████╗  ███████╗██╔██╗ ██║███████║██████╔╝", width=w, style="#8be9fd")
    box_row("    ██║      ██║   ██║██║  ██║██╔══╝  ╚════██║██║╚██╗██║██╔══██║██╔═══╝ ", width=w, style="#8be9fd")
    box_row("    ╚██████╗ ╚██████╔╝██████╔╝███████╗███████║██║ ╚████║██║  ██║██║     ", width=w, style="#8be9fd")
    box_row("     ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ", width=w, style="#8be9fd")
    box_row("", width=w)

    sub = f" {APP} -Clipboard to Beautiful Code Image"
    box_row(center_line(sub, w), width=w, style="bold #ffd166")
    box_row(center_line(f"by {AUTHOR}   •   v{VERSION}", w), width=w, style="#cdd6f4")
    box_row("", width=w)

    console.print("[bold #00e5ff]╠" + "═" * w + "╣[/]")
    box_row(center_line("[1] Görsel Oluştur", w), width=w, style="bold #7ee787")
    box_row("", width=w)
    box_row(center_line("[2] Bilgi", w), width=w, style="bold #82aaff")
    box_row("", width=w)
    box_row(center_line("[0] Çıkış", w), width=w, style="bold #ff7b72")
    console.print("[bold #00e5ff]╚" + "═" * w + "╝[/]")
             


def show_menu():
    clear_screen()
    console.print("\n")
    print_main_banner()
    console.print("[dim]İpucu: Kodu kopyala → 1'e bas → PNG oluşsun ✨[/]\n")


def show_info():
    print_main_banner()
    console.print("[bold #4ec9b0]╔" + "═" * 71 + "╗[/]")
    box_row("Uygulama   : CodeSnap", width=71, style="#cdd6f4")
    box_row("Sürüm      : 1.0", width=71, style="#cdd6f4")
    box_row("Geliştirici: devonicCEO", width=71, style="#cdd6f4")
    box_row("GitHub     : github.com/devonicCEO", width=71, style="#89dceb")
    box_row("Built with ☕ and Python", width=71, style="#cdd6f4")
    box_row("İpucu: Kodu kopyala, 1'e bas, estetik görsel al", width=71, style="#f9e2af")
    console.print("[bold #4ec9b0]╚" + "═" * 71 + "╝[/]")


def get_clipboard_code() -> str:
    if pyperclip is not None:
        try:
            txt = pyperclip.paste()
            return txt if isinstance(txt, str) else ""
        except Exception:
            pass

    try:

        root = tk.Tk()
        root.withdraw()
        txt = root.clipboard_get()
        root.destroy()
        return txt if isinstance(txt, str) else ""
    except Exception:
        return ""


def get_font(size: int):
    picks = [
        "CascadiaMono.ttf",
        "JetBrainsMono-Regular.ttf",
        "Consola.ttf",
        "DejaVuSansMono.ttf",
    ]
    for p in picks:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def token_color(tok) -> str:
    if tok in Name.Function or tok in Name.Decorator:
        return "#dcdcaa"
    if tok in Name.Class:
        return "#4ec9b0"
    if tok in Keyword:
        return "#c586c0"
    if tok in String:
        return "#ce9178"
    if tok in Comment:
        return "#6a9955"
    if tok in Number:
        return "#b5cea8"
    if tok in Operator or tok in Punctuation:
        return "#d4d4d4"
    if tok in Name:
        return "#9cdcfe"
    return "#d4d4d4"


def guess_lang_and_name(code: str):
    try:
        lx = guess_lexer(code)
    except Exception:
        return TextLexer(), "snippet.txt", "Text"

    nm = (lx.name or "Text").lower()
    if "python" in nm:
        return lx, "main.py", "Python"
    if "javascript" in nm:
        return lx, "app.js", "JavaScript"
    if "typescript" in nm:
        return lx, "app.ts", "TypeScript"
    if "java" in nm:
        return lx, "Main.java", "Java"
    if "html" in nm:
        return lx, "index.html", "HTML"
    if "css" in nm:
        return lx, "styles.css", "CSS"
    if "json" in nm:
        return lx, "data.json", "JSON"
    return lx, "snippet", lx.name or "Text"


def lex_into_lines(code: str, lexer):
    rows = [[]]
    for tok, val in lex(code.replace("\t", "    "), lexer):
        bits = val.split("\n")
        col = token_color(tok)
        for i, bit in enumerate(bits):
            if bit:
                rows[-1].append((bit, col, tok))
            if i < len(bits) - 1:
                rows.append([])
    if not rows:
        rows = [[("", "#d4d4d4", Token.Text)]]
    return rows


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def draw_bg_gradient(draw, w, h):
    top = (28, 30, 44)
    bot = (20, 22, 33)
    for y in range(h):
        k = y / max(1, h - 1)
        r = int(top[0] + (bot[0] - top[0]) * k)
        g = int(top[1] + (bot[1] - top[1]) * k)
        b = int(top[2] + (bot[2] - top[2]) * k)
        draw.line((0, y, w, y), fill=(r, g, b, 255))


def render_image(code: str):
    lexer, win_title, lang = guess_lang_and_name(code)
    rows = lex_into_lines(code, lexer)
    font = get_font(font_size)
    ln_font = get_font(max(14, font_size - 3))

    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    lh = int(font_size * 1.55)
    
    left_gutter = 0
    if line_numbers:
        digits = len(str(max(1, len(rows))))
        left_gutter = int(td.textlength(" " + "9" * digits + " ", font=ln_font)) + 12

    max_w = 0
    for row in rows:
        width = 0
        for text, _, _ in row:
            width += int(td.textlength(text, font=font))
        max_w = max(max_w, width)

    top_bar = 46
    code_w = left_gutter + max_w + (pad * 2)
    code_h = len(rows) * lh + (pad * 2)
    ww = max(540, code_w)
    wh = top_bar + code_h

    rad = 18
    shadow_off = 16
    shadow_layer = Image.new("RGBA", (ww + shadow_off * 2, wh + shadow_off * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.rounded_rectangle([shadow_off, shadow_off, shadow_off + ww, shadow_off + wh], radius=rad, fill=(0, 0, 0, 160))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12))

    win = Image.new("RGBA", (ww, wh), (0, 0, 0, 0))
    wd = ImageDraw.Draw(win)
    draw_bg_gradient(wd, ww, wh)

    wd.rectangle([0, 0, ww, top_bar], fill=(36, 38, 52, 255))
    wd.line([0, top_bar, ww, top_bar], fill=(65, 70, 90, 255), width=1)

    circles = [(22, "#ff5f56"), (46, "#ffbd2e"), (70, "#27c93f")]
    for cx, col in circles:
        wd.ellipse([cx - 7, 16 - 7, cx + 7, 16 + 7], fill=col)

    title_font = get_font(15)
    title = f"{win_title}  •  {lang}"
    tw = int(wd.textlength(title, font=title_font))
    wd.text(((ww - tw) // 2, 10), title, font=title_font, fill="#b8c0d9")

    y = top_bar + pad
    for i, row in enumerate(rows, start=1):
        x = pad + left_gutter
        if line_numbers:
            ln = str(i).rjust(len(str(len(rows))))
            ln_w = int(wd.textlength(ln, font=ln_font))
            ln_x = pad + left_gutter - ln_w - 10
            wd.text((ln_x, y + 2), ln, font=ln_font, fill="#5f6378")
        if not row:
            y += lh
            continue
        for piece, col, _ in row:
            wd.text((x, y), piece, font=font, fill=col)
            x += int(wd.textlength(piece, font=font))
        y += lh

    
    glow = Image.new("RGBA", (ww, wh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle([0, 0, ww, top_bar + 20], fill=(120, 80, 220, 22))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    win.alpha_composite(glow)

    mask = rounded_mask((ww, wh), rad)
    clipped = Image.new("RGBA", (ww, wh), (0, 0, 0, 0))
    clipped.paste(win, (0, 0), mask=mask)

    final = Image.new("RGBA", shadow_layer.size, (0, 0, 0, 0))
    final.alpha_composite(shadow_layer, (0, 0))
    final.alpha_composite(clipped, (shadow_off, shadow_off))
    return final


def save_img(img):
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(f"codesnap_{stamp}.png")
    img.save(out, "PNG")
    return out.resolve()


def error_box(msg: str):
    console.print(Panel(msg, title="✖ Hata", border_style="red", padding=(0, 2)))


def success_box(path: Path):
    msg = Text("✓ Dosya başarıyla kaydedildi\n", style="bold #7ee787")
    msg.append(str(path), style="bold cyan")
    console.print(Panel(msg, title="Tamam", border_style="#3fb950", padding=(0, 2)))
    console.print("[dim]Preview:[/] ┌───────────┐")
    console.print("[dim]         [/]|  code snap |")
    console.print("[dim]         [/]|   image ✓  |")
    console.print("[dim]         [/]|___________|")


def generate_flow():
    code = get_clipboard_code()
    if not code.strip():
        error_box("Clipboard boş ya da okunamadı. Önce kod kopyala.")
        return

    with console.status("[bold #82aaff]Sanat eseriniz oluşturuluyor...[/]", spinner="aesthetic"):
        time.sleep(0.25)  
        img = render_image(code)
        path = save_img(img)
        time.sleep(0.15)
    success_box(path)


def main():
    while True:
        show_menu()
        choice = console.input("[bold #9cdcfe]Seçimin[/] [#6c7a99](1/2/0)[/]: ").strip()
        clear_screen()
        if choice == "1":
            generate_flow()
        elif choice == "2":
            show_info()
        elif choice in {"0", "q", "Q", "exit"}:
            console.print("\n[bold #a8b3cf]CodeSnap kapanıyor, iyi kodlamalar ✨[/]")
            break
        else:
            error_box("Geçersiz seçim! 1, 2 veya 0 kullan.")
        console.input("\n[dim]Devam etmek için Enter...[/]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)