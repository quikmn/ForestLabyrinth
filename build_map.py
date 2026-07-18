# -*- coding: utf-8 -*-
"""Generate a self-contained index.html map for the Spirit Vale Forest Labyrinth."""
import json, os

PROJ = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(PROJ, 'data.json'), encoding='utf-8'))
maps = data['maps']

# ---- layout: schematic grid cells (col, row) -> minimize overlap ----
POS = {
    'fledgling': (0, 2), 'frost_wisp': (1, 2), 'seedling': (2, 2), 'sparkit': (3, 2), 'waypoint': (4, 2),
    'bee': (2, 1), 'sunny_meadows_2': (2, 0),
    'hound': (0, 3), 'rabbit': (0, 4), 'rooster': (1, 3), 'diggers': (1, 4), 'mandrake': (1, 5), 'fairy_glen': (0, 5),
    'sprite': (2, 3), 'sprout': (2, 4), 'bumblebee': (3, 3), 'lightning_wisp': (3, 4), 'egglet': (4, 4), 'mystic_lake_1': (5, 4),
}
DX, DY, MARGIN, HALF = 184, 162, 40, 66

ELEMENT_COLORS = {
    'Earth': '#7bb661', 'Wind': '#37c9b6', 'Water': '#4a90e2',
    'Fire': '#ef6a4c', 'Neutral': '#9aa4b2', 'Holy': '#f4c95d',
}
SECTION_COLORS = {1: '#5aa9e6', 2: '#e6a15a', 3: '#7bc86c', 4: '#c77dff'}

# card name, effect, slot, tier note   (all labyrinth cards drop at 0.5%)
CARD = {
    'waypoint': ('Pup Card', 'Grants Lv.3 Firebolt', 'Headgear', ''),
    'sparkit': ('Sparkit Card', 'Grants Lv.3 Thunderbolt', 'Headgear', ''),
    'seedling': ('Seedling Card', 'HP +100, Vit +1', 'Weapon', ''),
    'frost_wisp': ('Frost Wisp Card', 'Water Damage +6%', 'Weapon', ''),
    'fledgling': ('Fledgling Card', 'Hit +25', 'Weapon', ''),
    'hound': ('Hound Card', 'Grants Lv.1 Fireball', 'Headgear', ''),
    'rabbit': ('Rabbit Card', 'Move Spd +10%', 'Shoes', 'top-value'),
    'bee': ('Bee Card', 'MP Regen +25%', 'Weapon', ''),
    'rooster': ('Rooster Card', 'Total Hit +10', 'Headgear', ''),
    'diggers': ('Digger Card', 'Grants Lv.1 Stomp', 'Headgear', ''),
    'mandrake': ('Mandrake Card', 'Grants Lv.1 Earth Spikes', 'Headgear', ''),
    'sprout': ('Sprout Card', 'Grants Lv.3 Earthbolt', 'Headgear', ''),
    'bumblebee': ('Bumblebee Card', 'MP Regen +25%', 'Accessory', ''),
    'lightning_wisp': ('Lightning Wisp Card', 'Wind Damage +6%', 'Weapon', ''),
    'egglet': ('Egglet Card', 'Atk Spd +10%, Agi +1', 'Weapon', 'top-value'),
    'sprite': ('Sprite Card', 'Healing +10%', 'Weapon', ''),
}
DIRMAP = {'north': 'n', 'east': 'e', 'south': 's', 'west': 'w'}

nodes = {}
for nid, m in maps.items():
    c, r = POS[nid]
    cx, cy = MARGIN + HALF + c * DX, MARGIN + HALF + r * DY
    exits = {DIRMAP[k]: v for k, v in m['exits'].items()}
    if m.get('type') == 'external-exit':
        nodes[nid] = {
            'id': nid, 'name': m['name'], 'kind': 'exit', 'x': cx, 'y': cy,
            'levelRange': m.get('levelRange'), 'exits': exits,
        }
    else:
        cr = m['creatures'][0]
        cardn, cardeff, cardslot, tier = CARD.get(nid, ('', '', '', ''))
        nodes[nid] = {
            'id': nid, 'name': m['name'].replace(' Map', ''), 'kind': 'room',
            'creature': cr['name'], 'level': cr['level'], 'element': cr['element'],
            'section': m.get('labyrinthSection'), 'img': m.get('model'),
            'shape': m.get('shape'), 'density': cr.get('density'),
            'portal': bool(m.get('entrance')), 'x': cx, 'y': cy, 'exits': exits,
            'card': {'name': cardn, 'effect': cardeff, 'slot': cardslot, 'tier': tier},
        }

# undirected edges
edge_set = set()
for nid, n in nodes.items():
    for d, tgt in n['exits'].items():
        if isinstance(tgt, str):
            edge_set.add(tuple(sorted((nid, tgt))))
edges = [list(e) for e in sorted(edge_set)]

# dropdown order: rooms by section then level, then exits
rooms = [n for n in nodes.values() if n['kind'] == 'room']
rooms.sort(key=lambda n: (n.get('section') or 9, n.get('level') or 0))
order = [n['id'] for n in rooms] + [n['id'] for n in nodes.values() if n['kind'] == 'exit']

canvasW = max(n['x'] for n in nodes.values()) + HALF + MARGIN
canvasH = max(n['y'] for n in nodes.values()) + HALF + MARGIN

DATA = {
    'nodes': nodes, 'edges': edges, 'order': order,
    'canvasW': canvasW, 'canvasH': canvasH,
    'elementColors': ELEMENT_COLORS, 'sectionColors': {str(k): v for k, v in SECTION_COLORS.items()},
    'entrances': data.get('entrances', ''),
}

html = open(os.path.join(PROJ, '_template.html'), encoding='utf-8').read()
html = html.replace('/*__DATA__*/', json.dumps(DATA))
open(os.path.join(PROJ, 'index.html'), 'w', encoding='utf-8').write(html)
print('Wrote index.html  (%d nodes, %d edges, canvas %dx%d)' % (len(nodes), len(edges), canvasW, canvasH))
