"""Render visual QA from the exact validated v2 atlas bytes."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent / 'run'
ATLAS = ROOT / 'final' / 'spritesheet-extended.png'
OUT = ROOT / 'qa' / 'final-previews'
OUT.mkdir(parents=True, exist_ok=True)
atlas = Image.open(ATLAS).convert('RGBA')
names = ['idle', 'running-right', 'running-left', 'waving', 'jumping',
         'failed', 'waiting', 'running', 'review']
counts = [6, 8, 8, 4, 5, 8, 6, 6, 6]

def cell(row, column):
    return atlas.crop((column * 192, row * 208,
                       (column + 1) * 192, (row + 1) * 208))

def panel(frame, label):
    board = Image.new('RGBA', (192, 232), 'white')
    board.alpha_composite(frame, (0, 0))
    ImageDraw.Draw(board).text((8, 213), label, fill='black')
    return board.convert('RGB')

all_frames = []
for row, (name, count) in enumerate(zip(names, counts)):
    frames = [panel(cell(row, i), f'{name} {i + 1}/{count}') for i in range(count)]
    frames[0].save(OUT / f'{name}.gif', save_all=True, append_images=frames[1:],
                   duration=150, loop=0, disposal=2)
    all_frames.extend(frames)

all_frames[0].save(OUT / 'all-states.gif', save_all=True,
                   append_images=all_frames[1:], duration=160, loop=0, disposal=2)
jump = [panel(cell(0, 0), 'idle')] + [panel(cell(4, i), f'jump {i + 1}/5')
                                        for i in range(5)] + [panel(cell(0, 0), 'idle')]
jump[0].save(OUT / 'idle-jump-idle.gif', save_all=True,
             append_images=jump[1:], duration=170, loop=0, disposal=2)
labels = ['000', '022.5', '045', '067.5', '090', '112.5', '135', '157.5',
          '180', '202.5', '225', '247.5', '270', '292.5', '315', '337.5']
looks = [panel(cell(9 + i // 8, i % 8), f'look {labels[i]}') for i in range(16)]
looks[0].save(OUT / 'look-loop.gif', save_all=True,
              append_images=looks[1:], duration=180, loop=0, disposal=2)
for name, frame in [('idle', cell(0, 0)), ('wave', cell(3, 2)),
                    ('jump-peak', cell(4, 2)), ('review', cell(8, 4)),
                    ('look-right', cell(9, 4))]:
    panel(frame, name).save(OUT / f'{name}.png')
