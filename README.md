# 🌲 Forest Labyrinth Map — Spirit Vale

An interactive room map + route finder for the **Forest Labyrinth** in *Spirit Vale*.
Click any room to see its creature, element, exits, and farm card; use the route finder
to get turn-by-turn N/E/S/W directions between any two rooms.

**[▶ Open `index.html`](index.html)** — it's fully self-contained (no server needed);
just double-click it to preview locally.

## Host it on GitHub Pages
1. Create a new GitHub repo and push this whole folder (keep the `assets/` folder — it holds the creature art).
2. Repo **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main` / `/root`.
3. Wait ~1 min, then visit `https://<your-username>.github.io/<repo-name>/`.

Minimum files needed for the live site: **`index.html`** + the **`assets/`** folder.

## Editing the map
The map is generated, so don't hand-edit `index.html`. Instead:
- **`data.json`** — the source of truth: rooms, exits, creatures, elements, sections.
- **`_template.html`** — the page design (HTML/CSS/JS).
- **`build_map.py`** — merges them → run `python build_map.py` to regenerate `index.html`.

### Exit legend in `data.json`
- `"west": "sparkit"` → that exit connects to the `sparkit` room
- `"west": false` → wall (no exit)
- `"west": null` → unexplored / unknown

## Reference data
- `ref-monsters.json` — 262 monsters (levels, elements, drop tables) scraped from spiritvale.info
- `ref-maps.json` — 48 overworld zones

## Notes
- The map is a **schematic** (not geographically to scale). Some rooms are L- or U-shaped and
  the maze has loops, so it doesn't tile onto a clean grid. For true compass directions, use a
  room's exit list or the route finder.
- Missing creature art (`rooster`, `sparkit`, `egglet`) falls back to a colored initial until
  screenshots are added to `assets/`.
