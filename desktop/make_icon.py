"""生成 256x256 像素风问号方块图标（纯标准库，无 Pillow 依赖）。"""
import os
import struct
import zlib

SIZE = 256
GRID = 32              # 32x32 像素格
CELL = SIZE // GRID    # 每格 8px

TRANSPARENT = (0, 0, 0, 0)
DARK = (122, 74, 18, 255)
YELLOW = (248, 192, 32, 255)
LIGHT = (255, 232, 150, 255)
SHADOW = (214, 148, 16, 255)
QUESTION = (122, 74, 18, 255)

# 问号位图（每行一个字符串，'#' 为笔画）
MARK = [
    "..###..",
    ".#####.",
    "##...##",
    "##...##",
    "....###",
    "...###.",
    "..###..",
    "..###..",
    "...#...",
    ".......",
    "..###..",
]


def build_grid():
    g = [[TRANSPARENT for _ in range(GRID)] for _ in range(GRID)]

    # 外框（深棕）
    for y in range(GRID):
        for x in range(GRID):
            g[y][x] = DARK

    # 内部填充
    for y in range(2, GRID - 2):
        for x in range(2, GRID - 2):
            g[y][x] = YELLOW

    # 左上高光、右下阴影，制造立体感
    for i in range(2, GRID - 2):
        g[i][2] = LIGHT
        g[2][i] = LIGHT
        g[i][GRID - 3] = SHADOW
        g[GRID - 3][i] = SHADOW

    # 四个角铆钉
    for (cx, cy) in ((3, 3), (GRID - 4, 3), (3, GRID - 4), (GRID - 4, GRID - 4)):
        g[cy][cx] = DARK

    # 居中画问号（笔画宽度 1 格，位图 7 列 × 11 行）
    ox = (GRID - len(MARK[0])) // 2
    oy = (GRID - len(MARK)) // 2
    for ry, row in enumerate(MARK):
        for rx, ch in enumerate(row):
            if ch == "#":
                g[oy + ry][ox + rx] = QUESTION
    return g


def make_png(grid):
    rows = []
    for gy in range(GRID):
        row = bytearray()
        for gx in range(GRID):
            r, gr, b, a = grid[gy][gx]
            row += bytes((r, gr, b, a)) * CELL
        line = bytes(row) * 1
        # 每个像素格纵向重复 CELL 行
        for _ in range(CELL):
            rows.append(b"\x00" + line)
    raw = b"".join(rows)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def make_ico(png_bytes):
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png_bytes), 22)
    return header + entry + png_bytes


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out_dir, exist_ok=True)
    png = make_png(build_grid())
    ico_path = os.path.join(out_dir, "icon.ico")
    with open(ico_path, "wb") as f:
        f.write(make_ico(png))
    png_path = os.path.join(out_dir, "icon.png")
    with open(png_path, "wb") as f:
        f.write(png)
    print("icon.ico", os.path.getsize(ico_path), "bytes")
    print("icon.png", os.path.getsize(png_path), "bytes")


if __name__ == "__main__":
    main()
