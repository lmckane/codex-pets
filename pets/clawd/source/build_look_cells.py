"""Pose the original Clawd eye pixels in the Pets sixteen-direction order."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent / 'run'
base = Image.open(ROOT / 'frames' / 'idle' / '00.png').convert('RGBA')
pixels = base.load()
eyes = [(x, y) for y in range(base.height) for x in range(base.width)
        if pixels[x, y] == (0, 0, 0, 255)]
coral = (221, 119, 91, 255)
black = (0, 0, 0, 255)
out = ROOT / 'look-cells'
out.mkdir(parents=True, exist_ok=True)
angles = [i * 22.5 for i in range(16)]
eye_offsets = [
    (0, -8), (3, -7), (5, -6), (7, -5),
    (8, 0), (7, 5), (5, 10), (3, 15),
    (0, 18), (-3, 15), (-5, 10), (-7, 5),
    (-8, 0), (-7, -5), (-5, -6), (-3, -7),
]
for angle, (dx, dy) in zip(angles, eye_offsets):
    cell = base.copy()
    cp = cell.load()
    for x, y in eyes:
        cp[x, y] = coral
    for x, y in eyes:
        target = (x + dx, y + dy)
        if base.getpixel(target) not in (coral, black):
            raise SystemExit(f'eye would leave Clawd face at {angle}: {target}')
        cp[target] = black
    # Extend the original lower body by four target pixels so its intended
    # four leg gaps begin below the pet validator's body-interior region.
    for y in range(155, 159):
        for x in range(51, 136):
            cp[x, y] = coral
    label = f'{angle:05.1f}' if angle % 1 else f'{int(angle):03d}'
    cell.save(out / f'{label}.png')
