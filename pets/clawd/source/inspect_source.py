from PIL import Image, ImageDraw
from pathlib import Path

root = Path(__file__).parent / 'source-gifs'
names = ['idle-fluid', 'walking-fluid', 'greeting-fluid', 'done', 'error-fluid', 'waiting-for-you-fluid', 'typing-fluid', 'testing-fluid', 'thinking']
sheet = Image.new('RGB', (9 * 180, 2 * 190), '#eeeeee')
draw = ImageDraw.Draw(sheet)
for col, name in enumerate(names):
    gif = Image.open(root / f'{name}.gif')
    for row, idx in enumerate([0, gif.n_frames // 2]):
        gif.seek(idx)
        frame = gif.convert('RGBA')
        frame.thumbnail((160, 150), Image.Resampling.NEAREST)
        sheet.paste(frame, (col * 180 + 10, row * 190 + 10), frame)
        draw.text((col * 180 + 6, row * 190 + 165), f'{name} {idx}/{gif.n_frames}', fill='#111111')
sheet.save(Path(__file__).parent / 'source-overview.png')
