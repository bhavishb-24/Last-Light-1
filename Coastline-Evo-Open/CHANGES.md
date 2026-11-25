# Coastline Evo Open World changes

## INPUT V11

- The 3D renderer clips polygons without a temporary vertex list and reuses coordinates already projected during visibility checks. Fast and Full retain their existing artwork and key-triggered redraw behavior.
- The HUD shows relative steering and distance to the active destination. UP means ahead, L and R indicate which way to turn, TURN means the destination is behind you, and HERE means it is nearby.
- Story conversations and the ALPHA journal name the exact signs to look for and the next action. The puzzle, prices and ending requirements are unchanged.
- From V10, replace EVODATA.py, EVOVIEW.py and EVOOPEN.py. To roll back, use the [V10 ZIP](https://github.com/bhavishb-24/Last-Light/raw/d86d0d2/Coastline-Evo-Open.zip).

## INPUT V10

- City streets have dashed yellow center lines in both Fast and Full 3D. The raised expressway has white edge lines.
- From V9, replace EVOVIEW.py and EVOOPEN.py. To revert, download the [V9 ZIP](https://github.com/bhavishb-24/Last-Light/raw/e9c93f1/Coastline-Evo-Open.zip).

## INPUT V9

- Coast Expressway now has a raised deck. The three ramps climb from street level to four game units, and the 3D camera follows the road height. The road surface has a single level at each location.
- Added street signal poles that cycle red, amber and green, and painted crosswalks near city intersections. The lights are scenery.
- Replace EVODATA.py, EVOVIEW.py and EVOOPEN.py when upgrading from V8. The five-file ZIP and checkpoint format are retained.

### Roll back to INPUT V8

Download the [V8 ZIP](https://github.com/bhavishb-24/Last-Light/raw/9b209cb/Coastline-Evo-Open.zip), replace all five Python files, and check for LAST LIGHT / INPUT V8.

## INPUT V8

- Four districts extend the city east: Northgate, East Docks, Southbank and Breakwater.
- The Coast Expressway runs north to south, with three marked at-grade merge ramps and a higher driving speed limit. The atlas shows the routes.
- V8 removes the V7 skiff and floatplane trips. The original Marina ferry is available.
- The ZIP contains five Python files. Older checkpoints load in V8. Save from one of the original 12 districts if you intend to load that code in V6.

### Roll back to INPUT V6

Download the [V6 ZIP](https://github.com/bhavishb-24/Last-Light/raw/636cf9b/Coastline-Evo-Open.zip), replace the five Python files, and check for LAST LIGHT / INPUT V6.

## INPUT V7

- The Marina offers a controllable skiff and floatplane on a compact 2D bay chart.
- The skiff can collect a dock log at the gold buoy and earn $20 by docking at Sun Pier. Boats avoid the shoals, while the plane can cross them at altitude. Press 2nd to descend before landing.
- The existing ferry remains available. These are shorter trips than the full edition's 3D coastal travel.
- Updated Python files: EVOOPEN.py and EVOSPORT.py. The ZIP still contains five Python files. Checkpoint format is unchanged.

### Roll back to INPUT V6

Download the [V6 ZIP](https://github.com/bhavishb-24/Last-Light/raw/636cf9b/Coastline-Evo-Open.zip), replace the five Python files, and confirm the title says LAST LIGHT / INPUT V6.

## INPUT V6

- At the West Quay safehouse, press LEFT to swap between Lena and Sol. They share progress and controls. Switching selects each lead's default jacket.
- At Palm Garden, press UP for a six-input cycling workout. Completion adds 2 to your walking speed while the 30-second game timer lasts.
- At Palm Garden, press RIGHT for three holes of mini golf. Clear all three for $15. DOWN still opens the lost record clues.
- Updated Python files: EVOOPEN.py, EVOMENU.py and EVOSPORT.py. The ZIP contains exactly five files. Character selection and the workout boost are session-only. Checkpoint format stays compatible.

### Roll back to INPUT V5

Download the [V5 ZIP](https://github.com/bhavishb-24/Last-Light/raw/1bb0056/Coastline-Evo-Open.zip) and replace the five Python files. Check that the title says LAST LIGHT / INPUT V5.

## INPUT V5

- West Quay opens the safehouse after Mara's first conversation. Rest advances the weather and clears a patrol alert. You can put on the starter jacket, read your checkpoint, or open the existing WAVE radio.
- Velvet Club offers three pool shots and pays $6 per sunk ball. The Velvet story choice takes priority whenever it is active.
- Updated files: EVOOPEN.py and EVOMENU.py. New file: EVOSPORT.py, which loads when you play pool or fish. V4 checkpoint codes work in V5.

## Roll back to INPUT V4

Copy your checkpoint code first. Download the [V4 ZIP](https://github.com/bhavishb-24/Last-Light/raw/26ff967/Coastline-Evo-Open.zip), extract it, send all four Python files, and choose Replace. Run EVOOPEN and check for LAST LIGHT / INPUT V4. V5 uses the same checkpoint format.
