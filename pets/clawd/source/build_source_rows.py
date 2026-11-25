"""Adapt the repository's original Clawd GIF frames to Pets cell geometry."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SOURCE = ROOT / 'source-gifs'
OUT = ROOT / 'run' / 'frames'
CELL = (192, 208)
SOURCE_CROP = (50, 60, 430, 440)

# Every visual comes from an original Mascot Studio GIF frame. Frame selection
# maps source actions onto the nine activity states required by ChatGPT Pets.
ROWS = {
    'idle': ('idle-fluid', [0, 2, 4, 8, 12, 15]),
    'running-right': ('walking-fluid', [0, 1, 3, 4, 6, 7, 9, 10]),
    'waving': ('greeting-fluid', [0, 4, 10, 19]),
    'jumping': ('done', [40, 1, 2, 3, 40]),
    'failed': ('error', [0, 1, 2, 3, 4, 5, 0, 5]),
    'waiting': ('waiting-for-you-fluid', [0, 2, 4, 6, 8, 9]),
    'running': ('typing-fluid', [0, 3, 6, 9, 12, 17]),
    'review': ('testing', [0, 1, 2, 4, 6, 7]),
}

def normalize(frame: Image.Image, jump=False) -> Image.Image:
    frame = frame.convert('RGBA')
    if jump:
        # The source celebration has detached confetti. Keep only the original
        # Clawd pixels (coral body and black eyes), without drawing new pixels.
        px = frame.load()
        for y in range(frame.height):
            for x in range(frame.width):
                r, g, b, a = px[x, y]
                if not a or not ((r, g, b) == (221, 119, 91) or (r, g, b) == (0, 0, 0)):
                    px[x, y] = (0, 0, 0, 0)
    scaled = frame.crop(SOURCE_CROP).resize((192, 192), Image.Resampling.NEAREST)
    cell = Image.new('RGBA', CELL, (0, 0, 0, 0))
    cell.alpha_composite(scaled, (0, 8))
    return cell

for state, (name, indexes) in ROWS.items():
    folder = OUT / state
    folder.mkdir(parents=True, exist_ok=True)
    gif = Image.open(SOURCE / f'{name}.gif')
    for j, index in enumerate(indexes):
        gif.seek(index)
        normalize(gif.copy(), jump=state == 'jumping').save(folder / f'{j:02d}.png')

# Mirror each already-approved rightward pose in place, preserving frame order.
left = OUT / 'running-left'
left.mkdir(parents=True, exist_ok=True)
for f in sorted((OUT / 'running-right').glob('*.png')):
    Image.open(f).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(left / f.name)

base = Image.open(OUT / 'idle' / '00.png')
base.save(ROOT / 'run' / 'decoded' / 'base.png')
base.save(ROOT / 'run' / 'references' / 'canonical-base.png')
