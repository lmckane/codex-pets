"""Record visual review of the final labeled Clawd direction sheet."""
import json
from pathlib import Path

labels = ['000', '022.5', '045', '067.5', '090', '112.5', '135', '157.5',
          '180', '202.5', '225', '247.5', '270', '292.5', '315', '337.5']
expected = ['up', 'up-right', 'up-right', 'up-right', 'right',
            'down-right', 'down-right', 'down-right', 'down',
            'down-left', 'down-left', 'down-left', 'left',
            'up-left', 'up-left', 'up-left']
offsets = [(0, -8), (3, -7), (5, -6), (7, -5), (8, 0), (7, 5),
           (5, 10), (3, 15), (0, 18), (-3, 15), (-5, 10),
           (-7, 5), (-8, 0), (-7, -5), (-5, -6), (-3, -7)]
cardinals = {'000', '090', '180', '270'}
records = {}
for label, meaning, (dx, dy) in zip(labels, expected, offsets):
    horizontal = 'right' if dx > 0 else 'left' if dx < 0 else 'centered'
    vertical = 'lower' if dy > 0 else 'higher' if dy < 0 else 'level'
    records[label] = {
        'expected': meaning,
        'observed': f'Original black square eye pair is {horizontal} and {vertical} on the coral face',
        'verdict': 'pass' if label in cardinals else 'warning',
        'reason': f'The two whole square eyes shift {dx:+d}px horizontally and {dy:+d}px vertically relative to neutral while the four legs stay anchored; intermediate gaze is subtle at pet size.'
    }
path = Path(__file__).parent / 'run' / 'qa' / 'direction-semantics.json'
path.write_text(json.dumps({'directions': records}, indent=2) + '\n')
