#!/usr/bin/env python3
"""
256 色字符图生成器 — GUI 版
将图片转换为彩色字符画，支持自定义字符、背景色、导出图片/HTML/TXT。
"""

import sys
import os
import math
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont

# ── 1. 字符密度序列 ──────────────────────────────────────────────
ASCII_RAMP = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

MIXED_RAMP = list("繁龍龜鼎鬱麤鱗龘驫鑫犇灥猋麐𪚥䲜䨻㵘𡔽𠀾𠁅𠂉𠃊𠄌𠆢𠇍𠈌𠉭𠊎𠋑𠌫𠍱𠎝𠏉𠐟𠑥𠒣𠓙𠔦𠕄𠖀𠗃𠘚𠙹𠚤𠛬𠜎𠝍𠞰𠟅𠠄𠡳𠢯𠣴𠤎𠥆𠦒𠧧𠨩𠩺𠪊𠫓𠬝𠭥𠮟𠯋𠰀𠱁𠲵𠳿𠴱𠵅𠶜𠷡𠸉𠹌𠺘𠻗𠼝𠽤𠾭𠿪𡀔𡁏𡂝𡃁𡄯𡅅𡆇𡇙𡈑𡉚𡊄𡋗𡌛𡍣𡎺𡏄𡐓𡑞𡒗𡓟𡔚𡕛𡖖𡗗𡘙𡙛𡚜𡛝𡜞𡝟𡞠𡟡𡠢𡡣𡢤𡣥𡤦𡥧𡦨𡧩𡨪𡩫𡪬𡫭𡬮𡭯𡮰𡯱𡰲𡱳𡲴𡳵𡴶𡵷𡶸𡷹𡸺𡹻𡺼𡻽𡼾𡽿𡾀𡿁𢀂𢁃𢂄𢃅𢄆𢅇𢆈𢇉𢈊𢉋𢊌𢋍𢌎𢍏𢎐𢏑𢐒𢑓𢒔𢓕𢔖𢕗𢖘𢗙𢘚𢙛𢚜𢛝𢜞𢝟𢞠𢟡𢠢𢡣𢢤𢣥𢤦𢥧𢦨𢧩𢨪𢩫𢪬𢫭𢬮𢭯𢮰𢯱𢰲𢱳𢲴𢳵𢴶𢵷𢶸𢷹𢸺𢹻𢺼𢻽𢼾𢽿𢾀𢿁𣀂𣁃𣂄𣃅𣄆𣅇𣆈𣇉𣈊𣉋𣊌𣋍𣌎𣍏𣎐𣏑𣐒𣑓𣒔𣓕𣔖𣕗𣖘𣗙𣘚𣙛𣚜𣛝𣜞𣝟𣞠𣟡𣠢𣡣𣢤𣣥𣤦𣥧𣦨𣧩𣨪𣩫𣪬𣫭𣬮𣭯𣮰𣯱𣰲𣱳𣲴𣳵𣴶𣵷𣶸𣷹𣸺𣹻𣺼𣻽𣼾𣽿𣾀𣿁𤀂𤁃𤂄𤃅𤄆𤅇𤆈𤇉𤈊𤉋𤊌𤋍𤌎𤍏𤎐𤏑𤐒𤑓𤒔𤓕𤔖𤕗𤖘𤗙𤘚𤙛𤚜𤛝𤜞𤝟𤞠𤟡𤠢𤡣𤢤𤣥𤤦𤥧𤦨𤧩𤨪𤩫𤪬𤫭𤬮𤭯𤮰𤯱𤰲𤱳𤲴𤳵𤴶𤵷𤶸𤷹𤸺𤹻𤺼𤻽𤼾𤽿𤾀𤿁𥀂𥁃𥂄𥃅𥄆𥅇𥆈𥇉𥈊𥉋𥊌𥋍𥌎𥍏𥎐𥏑𥐒𥑓𥒔𥓕𥔖𥕗𥖘𥗙𥘚𥙛𥚜𥛝𥜞𥝟𥞠𥟡𥠢𥡣𥢤𥣥𥤦𥥧𥦨𥧩𥨪𥩫𥪬𥫭𥬮𥭯𥮰𥯱𥰲𥱳𥲴𥳵𥴶𥵷𥶸𥷹𥸺𥹻𥺼𥻽𥼾𥽿𥾀𥿁𦀂𦁃𦂄𦃅𦄆𦅇𦆈𦇉𦈊𦉋𦊌𦋍𦌎𦍏𦎐𦏑𦐒𦑓𦒔𦓕𦔖𦕗𦖘𦗙𦘚𦙛𦚜𦛝𦜞𦝟𦞠𦟡𦠢𦡣𦢤𦣥𦤦𦥧𦦨𦧩𦨪𦩫𦪬𦫭𦬮𦭯𦮰𦯱𦰲𦱳𦲴𦳵𦴶𦵷𦶸𦷹𦸺𦹻𦺼𦻽𦼾𦽿𦾀𦿁𧀂𧁃𧂄𧃅𧄆𧅇𧆈𧇉𧈊𧉋𧊌𧋍𧌎𧍏𧎐𧏑𧐒𧑓𧒔𧓕𧔖𧕗𧖘𧗙𧘚𧙛𧚜𧛝𧜞𧝟𧞠𧟡𧠢𧡣𧢤𧣥𧤦𧥧𧦨𧧩𧨪𧩫𧪬𧫭𧬮𧭯𧮰𧯱𧰲𧱳𧲴𧳵𧴶𧵷𧶸𧷹𧸺𧹻𧺼𧻽𧼾𧽿𧾀𧿁𨀂𨁃𨂄𨃅𨄆𨅇𨆈𨇉𨈊𨉋𨊌𨋍𨌎𨍏𨎐𨏑𨐒𨑓𨒔𨓕𨔖𨕗𨖘𨗙𨘚𨙛𨚜𨛝𨜞𨝟𨞠𨟡𨠢𨡣𨢤𨣥𨤦𨥧𨦨𨧩𨨪𨩫𨪬𨫭𨬮𨭯𨮰𨯱𨰲𨱳𨲴𨳵𨴶𨵷𨶸𨷹𨸺𨹻𨺼𨻽𨼾𨽿𨾀𨿁𩀂𩁃𩂄𩃅𩄆𩅇𩆈𩇉𩈊𩉋𩊌𩋍𩌎𩍏𩎐𩏑𩐒𩑓𩒔𩓕𩔖𩕗𩖘𩗙𩘚𩙛𩚜𩛝𩜞𩝟𩞠𩟡𩠢𩡣𩢤𩣥𩤦𩥧𩦨𩧩𩨪𩩫𩪬𩫭𩬮𩭯𩮰𩯱𩰲𩱳𩲴𩳵𩴶𩵷𩶸𩷹𩸺𩹻𩺼𩻽𩼾𩽿𩾀𩿁𪀂𪁃𪂄𪃅𪄆𪅇𪆈𪇉𪈊𪉋𪊌𪋍𪌎𪍏𪎐𪏑𪐒𪑓𪒔𪓕𪔖𪕗𪖘𪗙𪘚𪙛𪚜𪛝𪜞𪝟𪞠𪟡𪠢𪡣𪢤𪣥𪤦𪥧𪦨𪧩𪨪𪩫𪪬𪫭𪬮𪭯𪮰𪯱𪰲𪱳𪲴𪳵𪴶𪵷𪶸𪷹𪸺𪹻𪺼𪻽𪼾𪽿𪾀𪿁𫀂𫁃𫂄𫃅𫄆𫅇𫆈𫇉𫈊𫉋𫊌𫋍𫌎𫍏𫎐𫏑𫐒𫑓𫒔𫓕𫔖𫕗𫖘𫗙𫘚𫙛𫚜𫛝𫜞𫝟𫞠𫟡𫠢𫡣𫢤𫣥𫤦𫥧𫦨𫧩𫨪𫩫𫪬𫫭𫬮𫭯𫮰𫯱𫰲𫱳𫲴𫳵𫴶𫵷𫶸𫷹𫸺𫹻𫺼𫻽𫼾𫽿𫾀𫿁𬀂𬁃𬂄𬃅𬄆𬅇𬆈𬇉𬈊𬉋𬊌𬋍𬌎𬍏𬎐𬏑𬐒𬑓𬒔𬓕𬔖𬕗𬖘𬗙𬘚𬙛𬚜𬛝𬜞𬝟𬞠𬟡𬠢𬡣𬢤𬣥𬤦𬥧𬦨𬧩𬨪𬩫𬪬𬫭𬬮𬭯𬮰𬯱𬰲𬱳𬲴𬳵𬴶𬵷𬶸𬷹𬸺𬹻𬺼𬻽𬼾𬽿𬾀𬿁𭀂𭁃𭂄𭃅𭄆𭅇𭆈𭇉𭈊𭉋𭊌𭋍𭌎𭍏𭎐𭏑𭐒𭑓𭒔𭓕𭔖𭕗𭖘𭗙𭘚𭙛𭚜𭛝𭜞𭝟𭞠𭟡𭠢𭡣𭢤𭣥𭤦𭥧𭦨𭧩𭨪𭩫𭪬𭫭𭬮𭭯𭮰𭯱𭰲𭱳𭲴𭳵𭴶𭵷𭶸𭷹𭸺𭹻𭺼𭻽𭼾𭽿𭾀𭿁𮀂𮁃𮂄𮃅𮄆𮅇𮆈𮇉𮈊𮉋𮊌𮋍𮌎𮍏𮎐𮏑𮐒𮑓𮒔𮓕𮔖𮕗𮖘𮗙𮘚𮙛𮚜𮛝𮜞𮝟𮞠𮟡𮠢𮡣𮢤𮣥𮤦𮥧𮦨𮧩𮨪𮩫𮪬𮫭𮬮𮭯𮮰𮯱")

def get_ramp(use_chinese: bool, custom_chars: str | None = None):
    """Return a character list sorted by visual density (dark to light)."""
    if custom_chars:
        return list(custom_chars)
    if use_chinese:
        return MIXED_RAMP
    return ASCII_RAMP


# ── 2. xterm 256色映射 ──────────────────────────────────────────
def rgb_to_ansi256(r: int, g: int, b: int) -> int:
    """Map RGB (0-255 each) to the closest xterm 256-color index."""
    grey_val = (r * 30 + g * 59 + b * 11) // 100
    if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15:
        grey_idx = min(23, grey_val * 25 // 268)
        return 232 + grey_idx
    ri = min(5, r * 6 // 257)
    gi = min(5, g * 6 // 257)
    bi = min(5, b * 6 // 257)
    return 16 + (ri * 36) + (gi * 6) + bi


# ── 3. 结构化数据生成 ───────────────────────────────────────────
def img_to_char_matrix(
    image_path: str,
    width: int = 160,
    use_chinese: bool = False,
    custom_chars: str | None = None,
    aspect_ratio: float = 0.5,
) -> tuple[list[list[tuple[str, int, int, int]]], int, int]:
    """
    Convert image to a character matrix with RGB colours.
    Returns: (matrix, img_w, img_h) where matrix[y][x] = (char, r, g, b)
    """
    ramp = get_ramp(use_chinese, custom_chars)
    ramp_len = len(ramp)

    img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = img.size
    new_h = int(orig_h / orig_w * width * aspect_ratio)
    if new_h < 1:
        new_h = 1
    img_small = img.resize((width, new_h), Image.LANCZOS)

    matrix = []
    for y in range(new_h):
        row = []
        for x in range(width):
            r, g, b = img_small.getpixel((x, y))
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            char_idx = min(int(lum / 255 * (ramp_len - 1)), ramp_len - 1)
            ch = ramp[char_idx]
            row.append((ch, r, g, b))
        matrix.append(row)

    return matrix, width, new_h


# ── 4. 颜色工具 ─────────────────────────────────────────────────
def _hex_color(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def _ans256_to_hex(idx: int) -> str:
    """Convert xterm 256-colour index back to #RRGGBB (approximate)."""
    if idx < 16:
        PAL = [
            (0,0,0),(128,0,0),(0,128,0),(128,128,0),
            (0,0,128),(128,0,128),(0,128,128),(192,192,192),
            (128,128,128),(255,0,0),(0,255,0),(255,255,0),
            (0,0,255),(255,0,255),(0,255,255),(255,255,255),
        ]
        r, g, b = PAL[idx]
    elif idx < 232:
        idx -= 16
        r = (idx // 36) * 51
        g = ((idx % 36) // 6) * 51
        b = (idx % 6) * 51
    else:
        v = (idx - 232) * 10 + 8
        r = g = b = v
    return _hex_color(r, g, b)

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    """#RRGGBB → (r, g, b)."""
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def _rgb_to_tk_color(r: int, g: int, b: int) -> str:
    return _hex_color(r, g, b)

def _find_font(size: int, prefer_chinese: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Find a suitable monospace font on the system."""
    font_dir = os.environ.get("WINDIR", "C:\\Windows") + "\\Fonts\\"
    candidates = []
    if prefer_chinese:
        candidates = [
            font_dir + "msyh.ttc",      # Microsoft YaHei
            font_dir + "simhei.ttf",    # SimHei
            font_dir + "simsun.ttc",    # SimSun
            font_dir + "msyhbd.ttc",    # Microsoft YaHei Bold
            font_dir + "consola.ttf",   # Consolas
        ]
    else:
        candidates = [
            font_dir + "consola.ttf",
            font_dir + "cour.ttf",      # Courier New
            font_dir + "lucon.ttf",     # Lucida Console
            font_dir + "msyh.ttc",
            font_dir + "simhei.ttf",
        ]
    for fp in candidates:
        if os.path.isfile(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    # Fallback
    try:
        return ImageFont.truetype("", size)
    except Exception:
        return ImageFont.load_default()


# ═══════════════════════════════════════════════════════════════
#  GUI
# ═══════════════════════════════════════════════════════════════

PRESETS = {
    "ASCII 经典 (暗→亮)": "".join(ASCII_RAMP),
    "方块字符 █▓▒░": "█▓▒░ ",
    "单字符 █ (同字形)": "█",
    "单字符 我": "我",
}

BG_PRESETS = {
    "黑色 #1e1e1e": "#1e1e1e",
    "纯黑 #000000": "#000000",
    "白色 #ffffff": "#ffffff",
    "深灰 #333333": "#333333",
    "浅灰 #cccccc": "#cccccc",
    "自定义 RGB...": None,
}


class CharArtGUI:
    """Tkinter GUI for the character art generator."""

    def __init__(self, root: tk.Tk, initial_image: str | None = None):
        self.root = root
        self.root.title("字符图生成器 — by αLICE")
        self.root.geometry("1000x820")
        self.root.minsize(780, 600)

        # 图标
        self._set_icon()

        # State
        self._running = False
        self._thread = None
        self._matrix = None
        self._matrix_w = 0
        self._matrix_h = 0
        self._bg_color = "#1e1e1e"       # 当前背景色 hex
        self._custom_bg = "#1e1e1e"      # 自定义背景色缓存

        self._build_ui()

        if initial_image:
            self.script_var.set(initial_image)
            self.root.after(200, self._generate)

    def _set_icon(self):
        """尝试加载 bbbb.ico 图标."""
        icon_paths = [
            os.path.join(os.path.dirname(__file__), "bbbb.ico"),
            os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "bbbb.ico"),
            "d:/BUAA/科研/apps/Vi2PDF/bbbb.ico",
        ]
        for p in icon_paths:
            if os.path.isfile(p):
                try:
                    self.root.iconbitmap(default=p)
                    return
                except Exception:
                    pass

    # ── UI ─────────────────────────────────────────────────
    def _build_ui(self):
        pad = {"padx": 12}

        # 标题
        title = ttk.Label(
            self.root,
            text="字符图生成器 — 256 色字符画",
            font=("Microsoft YaHei UI", 14, "bold"),
        )
        title.pack(anchor=tk.W, **pad, pady=(12, 8))

        # ── 控制面板 ──
        ctrl = ttk.LabelFrame(self.root, text=" 控制面板 ", padding="8 8 8 8")
        ctrl.pack(fill=tk.X, **pad)

        # 行0: 图片选择
        r0 = ttk.Frame(ctrl)
        r0.pack(fill=tk.X, pady=2)
        ttk.Label(r0, text="图片文件：", width=10).pack(side=tk.LEFT)
        self.script_var = tk.StringVar()
        ttk.Entry(r0, textvariable=self.script_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(r0, text="浏览...", width=8,
                   command=self._browse_image).pack(side=tk.RIGHT)

        # 行1: 宽度 + 宽高比 + 字符预设
        r1 = ttk.Frame(ctrl)
        r1.pack(fill=tk.X, pady=2)

        ttk.Label(r1, text="宽度：", width=10).pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=160)
        ttk.Spinbox(r1, textvariable=self.width_var,
                    from_=30, to=500, increment=5, width=6,
                    command=self._generate).pack(side=tk.LEFT)

        ttk.Label(r1, text="  宽高比：").pack(side=tk.LEFT, padx=(12, 0))
        self.ratio_var = tk.StringVar(value="0.50")
        ttk.Spinbox(r1, textvariable=self.ratio_var,
                    from_=0.1, to=2.0, increment=0.05, width=5,
                    command=self._generate).pack(side=tk.LEFT)

        ttk.Label(r1, text="  预设：").pack(side=tk.LEFT, padx=(12, 0))
        self.preset_var = tk.StringVar(value=list(PRESETS.keys())[0])
        preset_cb = ttk.Combobox(r1, textvariable=self.preset_var,
                                 values=list(PRESETS.keys()),
                                 state="readonly", width=22)
        preset_cb.pack(side=tk.LEFT, padx=2)
        preset_cb.bind("<<ComboboxSelected>>", self._on_preset)

        # 行2: 自定义字符
        r2 = ttk.Frame(ctrl)
        r2.pack(fill=tk.X, pady=2)
        ttk.Label(r2, text="自定义字符：", width=10).pack(side=tk.LEFT)
        self.chars_var = tk.StringVar(value="".join(ASCII_RAMP))
        ttk.Entry(r2, textvariable=self.chars_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(r2, text="（首=暗 → 尾=亮）",
                  foreground="gray").pack(side=tk.LEFT, padx=4)

        # 行3: 背景颜色
        r3 = ttk.Frame(ctrl)
        r3.pack(fill=tk.X, pady=2)
        ttk.Label(r3, text="背景颜色：", width=10).pack(side=tk.LEFT)

        self.bg_preset_var = tk.StringVar(value=list(BG_PRESETS.keys())[0])
        bg_cb = ttk.Combobox(r3, textvariable=self.bg_preset_var,
                             values=list(BG_PRESETS.keys()),
                             state="readonly", width=18)
        bg_cb.pack(side=tk.LEFT)
        bg_cb.bind("<<ComboboxSelected>>", self._on_bg_preset)

        # RGB 值显示 / 自定义按钮
        self.bg_color_swatch = tk.Label(r3, text="  ", bg="#1e1e1e",
                                        relief=tk.SUNKEN, width=3)
        self.bg_color_swatch.pack(side=tk.LEFT, padx=(6, 4))

        self.bg_r_label = ttk.Label(r3, text="R:")
        self.bg_r_label.pack(side=tk.LEFT, padx=(0, 0))
        self.bg_r_var = tk.StringVar(value="30")
        self.bg_r_entry = ttk.Entry(r3, textvariable=self.bg_r_var, width=4)
        self.bg_r_entry.pack(side=tk.LEFT, padx=1)

        self.bg_g_label = ttk.Label(r3, text="G:")
        self.bg_g_label.pack(side=tk.LEFT, padx=(4, 0))
        self.bg_g_var = tk.StringVar(value="30")
        self.bg_g_entry = ttk.Entry(r3, textvariable=self.bg_g_var, width=4)
        self.bg_g_entry.pack(side=tk.LEFT, padx=1)

        self.bg_b_label = ttk.Label(r3, text="B:")
        self.bg_b_label.pack(side=tk.LEFT, padx=(4, 0))
        self.bg_b_var = tk.StringVar(value="30")
        self.bg_b_entry = ttk.Entry(r3, textvariable=self.bg_b_var, width=4)
        self.bg_b_entry.pack(side=tk.LEFT, padx=1)

        ttk.Button(r3, text="应用", width=5,
                   command=self._apply_custom_bg).pack(side=tk.LEFT, padx=(6, 2))
        ttk.Button(r3, text="调色板...", width=8,
                   command=self._pick_color).pack(side=tk.LEFT, padx=2)

        ttk.Label(r3, text="  ← 更改后点「应用」刷新",
                  foreground="gray").pack(side=tk.LEFT, padx=4)

        # 行4: 按钮区
        r4 = ttk.Frame(ctrl)
        r4.pack(fill=tk.X, pady=(6, 0))

        self.gen_btn = ttk.Button(r4, text="▶  生成预览",
                                  command=self._generate, width=14)
        self.gen_btn.pack(side=tk.LEFT)

        self.stop_btn = ttk.Button(r4, text="■  停止",
                                   command=self._stop, state=tk.DISABLED,
                                   width=10)
        self.stop_btn.pack(side=tk.LEFT, padx=6)

        self.progress = ttk.Progressbar(r4, mode="indeterminate", length=120)
        self.progress.pack(side=tk.LEFT, padx=8)

        self.status_var = tk.StringVar(value="就绪 — 选择图片后点击「生成预览」")
        ttk.Label(r4, textvariable=self.status_var,
                  foreground="#555").pack(side=tk.LEFT, padx=4)

        # 导出按钮（右侧）
        self.save_png_btn = ttk.Button(r4, text="🖼 导出图片",
                                       command=self._export_image,
                                       state=tk.DISABLED, width=14)
        self.save_png_btn.pack(side=tk.RIGHT, padx=2)
        self.save_html_btn = ttk.Button(r4, text="💾 导出 HTML",
                                        command=self._export_html,
                                        state=tk.DISABLED, width=14)
        self.save_html_btn.pack(side=tk.RIGHT, padx=2)
        self.save_txt_btn = ttk.Button(r4, text="📄 导出 TXT",
                                       command=self._export_txt,
                                       state=tk.DISABLED, width=14)
        self.save_txt_btn.pack(side=tk.RIGHT, padx=2)

        # ── 预览区 ──
        preview_frame = ttk.LabelFrame(self.root, text=" 预览 ", padding="4 4 4 4")
        preview_frame.pack(fill=tk.BOTH, expand=True, **pad, pady=(8, 4))

        self.preview = tk.Text(
            preview_frame,
            font=("Consolas", 5),
            wrap=tk.NONE,
            state=tk.DISABLED,
            bg=self._bg_color,
            cursor="arrow",
        )
        v_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL,
                                 command=self.preview.yview)
        h_scroll = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL,
                                 command=self.preview.xview)
        self.preview.configure(yscrollcommand=v_scroll.set,
                               xscrollcommand=h_scroll.set)

        self.preview.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)

        # 鼠标滚轮缩放字号
        self._font_size = 5
        self.preview.bind("<Control-MouseWheel>", self._on_zoom)
        self.preview.bind("<Control-Button-4>", self._on_zoom)
        self.preview.bind("<Control-Button-5>", self._on_zoom)

        # ── 底部状态栏 ──
        bottom = ttk.Frame(self.root)
        bottom.pack(fill=tk.X, **pad, pady=(0, 8))

        self.info_var = tk.StringVar(value="")
        ttk.Label(bottom, textvariable=self.info_var,
                  foreground="#888").pack(side=tk.LEFT)

        # by αLICE 署名（右下角）
        credit = tk.Label(
            bottom, text="by αLICE",
            font=("Microsoft YaHei UI", 8),
            foreground="#888",
        )
        credit.pack(side=tk.RIGHT, padx=(4, 0))

        ttk.Label(bottom, text="Ctrl+滚轮 缩放  |  ",
                  foreground="#aaa").pack(side=tk.RIGHT)

    # ── 事件处理 ───────────────────────────────────────────
    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff"),
                ("所有文件", "*.*"),
            ],
        )
        if path:
            self.script_var.set(path)
            self._generate()

    def _on_preset(self, event=None):
        name = self.preset_var.get()
        chars = PRESETS.get(name, "")
        if chars:
            self.chars_var.set(chars)
        self._generate()

    def _on_bg_preset(self, event=None):
        name = self.bg_preset_var.get()
        hex_val = BG_PRESETS.get(name)
        if hex_val is not None:
            # 预设颜色
            self._bg_color = hex_val
            self._custom_bg = hex_val
            r, g, b = _hex_to_rgb(hex_val)
            self.bg_r_var.set(str(r))
            self.bg_g_var.set(str(g))
            self.bg_b_var.set(str(b))
            self._update_bg_swatch()
            self._apply_bg_to_preview()
        # 自定义 → 不做任何事，等用户调色后点应用

    def _update_bg_swatch(self):
        self.bg_color_swatch.configure(bg=self._bg_color)

    def _apply_custom_bg(self):
        """将 RGB 输入框的值应用为背景色."""
        try:
            r = max(0, min(255, int(self.bg_r_var.get())))
            g = max(0, min(255, int(self.bg_g_var.get())))
            b = max(0, min(255, int(self.bg_b_var.get())))
        except ValueError:
            return
        self._bg_color = _hex_color(r, g, b)
        self._custom_bg = self._bg_color
        self._update_bg_swatch()
        self._apply_bg_to_preview()

    def _pick_color(self):
        """打开系统调色板."""
        result = colorchooser.askcolor(color=self._bg_color, title="选择背景颜色")
        if result and result[1]:
            self._bg_color = result[1]
            self._custom_bg = self._bg_color
            r, g, b = _hex_to_rgb(self._bg_color)
            self.bg_r_var.set(str(r))
            self.bg_g_var.set(str(g))
            self.bg_b_var.set(str(b))
            self._update_bg_swatch()
            self._apply_bg_to_preview()

    def _apply_bg_to_preview(self):
        """实时更新预览区背景色."""
        self.preview.configure(bg=self._bg_color)
        # 如果设为白色等亮色，调整文字颜色可能需要 — 但字符本身已有颜色

    def _on_zoom(self, event):
        """Ctrl+滚轮缩放字号."""
        if event.delta > 0 or event.num == 4:
            self._font_size = min(20, self._font_size + 1)
        else:
            self._font_size = max(2, self._font_size - 1)
        self.preview.configure(font=("Consolas", self._font_size))
        self._rerender_preview()

    # ── 生成逻辑 ───────────────────────────────────────────
    def _generate(self):
        """在后台线程中生成字符矩阵."""
        path = self.script_var.get().strip()
        if not path:
            return
        if not os.path.isfile(path):
            messagebox.showwarning("提示", "图片文件不存在。")
            return

        self._running = True
        self.gen_btn.configure(state=tk.DISABLED, text="⏳ 生成中...")
        self.stop_btn.configure(state=tk.NORMAL)
        self.progress.start(8)
        self.status_var.set("正在处理图片...")

        width = self.width_var.get()
        try:
            ratio = float(self.ratio_var.get())
        except ValueError:
            ratio = 0.5

        chars = self.chars_var.get()

        self._thread = threading.Thread(
            target=self._run_generate,
            args=(path, width, chars, ratio),
            daemon=True,
        )
        self._thread.start()

    def _run_generate(self, path, width, chars, ratio):
        try:
            matrix, mw, mh = img_to_char_matrix(
                path, width=width,
                custom_chars=chars if chars else None,
                aspect_ratio=ratio,
            )
            self._matrix = matrix
            self._matrix_w = mw
            self._matrix_h = mh
            self.root.after(0, self._render_preview)
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ 错误: {e}"))
            self.root.after(0, self._reset_ui)

    def _render_preview(self):
        """在主线程渲染预览."""
        if self._matrix is None:
            self._reset_ui()
            return

        pw = self.preview
        pw.configure(state=tk.NORMAL, bg=self._bg_color)
        pw.delete("1.0", tk.END)

        # 清除旧 tag
        for tag in pw.tag_names():
            pw.tag_delete(tag)

        # 按颜色分组，批量插入
        for row_idx, row in enumerate(self._matrix):
            if row_idx > 0:
                pw.insert(tk.END, "\n")

            i = 0
            while i < len(row):
                ch, r, g, b = row[i]
                col_idx = rgb_to_ansi256(r, g, b)
                tag = f"c{col_idx}"

                if tag not in pw.tag_names():
                    hex_color = _ans256_to_hex(col_idx)
                    pw.tag_configure(tag, foreground=hex_color)

                buf = [ch]
                j = i + 1
                while j < len(row):
                    ch2, r2, g2, b2 = row[j]
                    if rgb_to_ansi256(r2, g2, b2) == col_idx:
                        buf.append(ch2)
                        j += 1
                    else:
                        break
                pw.insert(tk.END, "".join(buf), tag)
                i = j

        pw.configure(state=tk.DISABLED)

        self.info_var.set(
            f"尺寸: {self._matrix_w}×{self._matrix_h} 字符  |  "
            f"背景: {self._bg_color}"
        )

        self.save_png_btn.configure(state=tk.NORMAL)
        self.save_html_btn.configure(state=tk.NORMAL)
        self.save_txt_btn.configure(state=tk.NORMAL)
        self._reset_ui()
        self.status_var.set("✅ 预览就绪 — 可用 Ctrl+滚轮 缩放")

    def _rerender_preview(self):
        """字号改变时重新排版."""
        if self._matrix is None:
            return
        self._render_preview()

    def _stop(self):
        self._running = False
        self.status_var.set("用户已停止")
        self._reset_ui()

    def _reset_ui(self):
        self._running = False
        self.progress.stop()
        self.gen_btn.configure(state=tk.NORMAL, text="▶  生成预览")
        self.stop_btn.configure(state=tk.DISABLED)

    # ── 导出：图片 ──────────────────────────────────────────
    def _export_image(self):
        """将字符矩阵渲染为 PNG 图片（目标 ~1280×720）。"""
        if self._matrix is None:
            return

        path = filedialog.asksaveasfilename(
            title="导出图片",
            defaultextension=".png",
            filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg"), ("所有文件", "*.*")],
        )
        if not path:
            return

        try:
            rows = len(self._matrix)
            cols = self._matrix_w

            # 判断是否含中文，选择字体
            sample_char = self._matrix[0][0][0]
            has_cjk = any('一' <= c <= '鿿' or '　' <= c <= '〿'
                         or '＀' <= c <= '￯' for c in self.chars_var.get())

            # 目标图片 1280×720，计算合适的字号和 cell 尺寸
            # 对ASCII: char_w ≈ font_size * 0.6, char_h ≈ font_size
            # 对中文: char_w ≈ font_size, char_h ≈ font_size
            char_width_ratio = 1.0 if has_cjk else 0.6

            # 计算字号使图片接近 1280×720
            target_w = 1280
            target_h = 720
            font_size_w = target_w / (cols * char_width_ratio)
            font_size_h = target_h / rows
            font_size = int(min(font_size_w, font_size_h))
            font_size = max(6, min(font_size, 48))

            font = _find_font(font_size, prefer_chinese=has_cjk)

            # 精确计算 cell 尺寸
            # 使用 ImageDraw.textbbox 测一个字符
            tmp_img = Image.new("RGB", (1, 1))
            draw = ImageDraw.Draw(tmp_img)
            test_char = "█" if has_cjk else "@"
            bbox = draw.textbbox((0, 0), test_char, font=font)
            cell_w = bbox[2] - bbox[0]
            cell_h = bbox[3] - bbox[1]

            # 实际图片尺寸
            img_w = cell_w * cols
            img_h = cell_h * rows

            bg_r, bg_g, bg_b = _hex_to_rgb(self._bg_color)
            img = Image.new("RGB", (img_w, img_h), (bg_r, bg_g, bg_b))
            draw = ImageDraw.Draw(img)

            # 逐字符绘制
            for y, row in enumerate(self._matrix):
                for x, (ch, r, g, b) in enumerate(row):
                    px = x * cell_w
                    py = y * cell_h
                    draw.text((px, py), ch, fill=(r, g, b), font=font)

            img.save(path)
            self.status_var.set(f"✅ 已导出图片: {os.path.basename(path)} ({img_w}×{img_h})")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    # ── 导出：HTML ──────────────────────────────────────────
    def _export_html(self):
        """导出为 HTML 文件."""
        if self._matrix is None:
            return

        path = filedialog.asksaveasfilename(
            title="导出 HTML",
            defaultextension=".html",
            filetypes=[("HTML 文件", "*.html"), ("所有文件", "*.*")],
        )
        if not path:
            return

        try:
            lines = []
            for row in self._matrix:
                parts = []
                for ch, r, g, b in row:
                    hex_c = _hex_color(r, g, b)
                    parts.append(
                        f'<span style="color:{hex_c}">{_html_escape(ch)}</span>'
                    )
                lines.append("".join(parts))

            body = "<br>".join(lines)
            html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>字符图 — by αLICE</title>
<style>
  body {{
    background: {self._bg_color};
    font-family: "Consolas", "Microsoft YaHei", "SimHei", monospace;
    font-size: 8px;
    line-height: 1.0;
    letter-spacing: 0;
    white-space: nowrap;
    margin: 12px;
  }}
</style>
</head>
<body>{body}</body>
</html>"""
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            self.status_var.set(f"✅ 已导出 HTML: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    # ── 导出：TXT ───────────────────────────────────────────
    def _export_txt(self):
        """导出为纯文本文件."""
        if self._matrix is None:
            return

        path = filedialog.asksaveasfilename(
            title="导出 TXT",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
        )
        if not path:
            return

        try:
            lines = ["".join(ch for ch, _, _, _ in row) for row in self._matrix]
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self.status_var.set(f"✅ 已导出 TXT: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))


def _html_escape(s: str) -> str:
    """Escape characters for HTML body."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ═══════════════════════════════════════════════════════════════
#  入口
# ═══════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    CharArtGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
