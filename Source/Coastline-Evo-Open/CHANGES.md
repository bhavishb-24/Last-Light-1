# Coastline Evo Open World changes

## INPUT V29

- Cutscenes retain both portraits between speakers. Only the text, speaker name, and animated mouth change.
- Blocked forward steps on foot can reuse the street picture and update the HUD. Ambient animation waits for the next world redraw.

## INPUT V28

- Four story moments now have illustrated location shots and back-and-forth dialogue with animated speaker portraits. Press ENTER to advance.

## INPUT V27

- New Story opens with an illustrated West Quay sunset and a picture of the WAVE studio before the controls screen.

## INPUT V26

- Phone browsing refreshes only the relevant tiles and app hint. Shops retain their headers and update the item preview, cash, and status only as needed. The taxi list refreshes only the destination name.

## INPUT V25

- Atlas draws once per opening. Edge ticks and the district label show the cursor while browsing.
- Small turns on foot can update just the lower HUD. The 3D camera catches up after about 34 degrees of accumulated turning or on the next movement. Driving still follows every turn.

## INPUT V24

- Restores V21 Fast 3D detail while keeping the V23 HUD and GPS.

## INPUT V23

- The lower 3D HUD remains on screen between moves. Its prompts and navigation update independently. The GPS includes a north-up street strip and a direct destination bearing, not a calculated road route. Alerts take priority over the strip.

## INPUT V22

- Fast 3D uses fewer skyline, facade, palm and road marking draws. Storefront signs, expressway geometry and both 3D cameras remain available. Enable Fast under Settings or press 2nd in the journal.
- Replace all five game files. [Roll back to V21](https://github.com/bhavishb-24/Last-Light/raw/cc34042/01-REQUIRED-Last-Light-Evo-Game.zip).

## INPUT V21

- Added animated portraits for Mara, Ivo, Ana, Kit and Red in dialogue. Only the mouth area redraws during the brief animation. ENTER continues or dismisses the dialogue.
- Replace all five game files. The optional intro pack can stay installed.
- [Roll back to V20](https://github.com/bhavishb-24/Last-Light/raw/34cd121/Coastline-Evo-Open.zip).

## INPUT V20

- Nearby Full mode facades add awnings, split windows and country driveways. Storefronts use their building colors. Clear skies gain an extra horizon band in Full, and tower windows glow after dark.
- Pedestrians shift position as game time advances. Full shows fewer pedestrians at night. The world still redraws in response to input.
- Five interiors gain scenic windows. Walk two tiles up and three left from the entrance to read the local board with ENTER.
- Four landmark encounters in The Relief Tape are named on screen. Beacon Point adds a final relay puzzle. Matches are required before the campaign reward.
- Replace all five Python files. [Roll back to V19](https://github.com/bhavishb-24/Last-Light/raw/76b7ce5/Coastline-Evo-Open.zip).

## INPUT V19

- The city now has 20 districts and 46 solid building footprints. Downtown has new tall blocks. Cypress Row, Orchard End, Sawgrass and Beacon Point have pitched-roof homes, greenery and quieter roads. The east exit ramp descends toward the new districts.
- All 20 marked venues have a walkable 2D interior. Press ENTER at the door, take three steps UP, then press ENTER at the counter. CLEAR leaves the room. Story triggers take priority at their destination.
- In a car, TRACE cycles chase view, first-person cockpit and top-down. On foot, TRACE switches between the original 3D and top-down views.
- Both Dead Air endings lead into The Relief Tape. Its 18 counter objectives, including three relay puzzles, complete a campaign route through every district. Check ALPHA for the next objective.
- Replace all five Python files. Old checkpoint codes load in V19. V19 codes with a slash suffix or a position in a new district require V19. The optional fullscreen intro pack works with V19.
- [Roll back to V18](https://github.com/bhavishb-24/Last-Light/raw/67fbe10/Coastline-Evo-Open.zip). Use a pre-V19 checkpoint for rollback.

## INPUT V18

- Lena and Sol have distinct original sprites in the title menu and on foot. Lena has a tied-back silhouette and plum streetwear. Sol has a broad silhouette, short hair and pale coastal streetwear. Walking animates the legs and hands.
- Replace EVOSPORT.py and EVOVIEW.py from V17. The optional fullscreen intro pack still works. [Roll back to V17](https://github.com/bhavishb-24/Last-Light/raw/a9237d2/Coastline-Evo-Open.zip).

## V17 fullscreen frame clarity update

- Rebuilt only EVFS010.py, EVFS012.py, EVFS014.py and EVFS016.py from clearer moments in the same sequence. The four frames share the previous fast pack’s draw budget. The full pack uses 3,373 drawing rectangles, compared with 24,313 in the first fullscreen pack.
- Replace only those four files. [Previous fast pack](https://github.com/bhavishb-24/Last-Light/raw/7a673da/Coastline-Evo-Fullscreen-Intro.zip).

## V17 fullscreen pack diagnostics

- Replace EVFSPLAY.py from the current fullscreen ZIP. The player ignores ENTER for the first 0.9 seconds and displays the frame name and exception if loading or drawing fails. Acknowledge an error with ENTER to continue to the title. Successful playback still has no overlay.

## V17 fullscreen pack update

- The faster pack uses fewer and larger drawing regions. It draws every sampled frame in order and completes the active frame even if the original 20-second target has elapsed.
- Replace all ten files from the [Fullscreen Intro Pack](../../02-OPTIONAL-Animated-Loading-Screen.zip). ENTER still skips, with no text over the frames. The five V17 game files already support the update.

## INPUT V17

- An optional fullscreen pack shows nine frames from the supplied MP4 in source order when you launch EVOOPEN. No prompts or progress bar appear over the frames. ENTER still skips.
- The pack crops the frames to fill the 320 × 210 drawing area and reduces the palette to speed up drawing. It skips slots when playback falls behind the 20-second timeline.
- From V16, replace EVOOPEN.py and EVOSPORT.py from the standard ZIP and install all ten files from Coastline-Evo-Fullscreen-Intro.zip. Without the pack, the game uses the built-in 2D intro. [Roll back to V16](https://github.com/bhavishb-24/Last-Light/raw/dbe6526/Coastline-Evo-Open.zip).

## INPUT V16

- The 20-second 2D intro follows the reference's shot rhythm more closely: a split-panel collage, dark pause, six stars, citrus market, green palms, a pastel waterfront, orange street scene and WAVE emblem. Artwork is drawn in code using Coastline's characters and graphics.
- From V15, replace EVOSPORT.py. The ZIP still contains five Python files. [Roll back to V15](https://github.com/bhavishb-24/Last-Light/raw/09e61f7/Coastline-Evo-Open.zip).

## INPUT V15

- The loading screen uses original color artwork in a 2D sequence inspired by the reference clip: illustrated collage, animated stars, two coastal cards and a WAVE radio end card.
- The sequence lasts up to 20 seconds. Press ENTER to skip to the title menu.
- Replace EVOSPORT.py and EVOVIEW.py from V14. The ZIP still contains five Python files. [Roll back to V14](https://github.com/bhavishb-24/Last-Light/raw/167015f/Coastline-Evo-Open.zip).

## INPUT V14

- EVOOPEN starts with a 3D loading animation through West Quay, downtown, the expressway and Northgate. It uses the game renderer and skips scheduled frames if drawing falls behind. The intro targets up to 5 FPS and runs for about 20 seconds, with ENTER to skip.
- From V13, replace EVOSPORT.py and EVOVIEW.py together. The standard ZIP includes five Python files. The title settings and checkpoint format are unchanged. [Roll back to V13](https://github.com/bhavishb-24/Last-Light/raw/46a6607/Coastline-Evo-Open.zip).

## INPUT V13

- EVOOPEN starts with an original animated Coastline intro capped at 20 seconds. Press ENTER to skip.
- The illustrated title menu offers New story, Load save, Settings and Quit. Settings choose Fast or Full graphics, Fine, Normal or Sharp turning, and a 3D or top-down starting view. These options apply to the game you start or load.
- From V12, replace EVOOPEN.py and EVOSPORT.py. The ZIP contains five Python files. Checkpoint codes still work. [Roll back to V12](https://github.com/bhavishb-24/Last-Light/raw/9062894/Coastline-Evo-Open.zip).

## INPUT V12

- The 3D HUD draws a GPS arrow and distance to your pin or active objective. Ramp approaches have destination signs.
- Press RIGHT in the ALPHA journal to switch between Fine, Normal and Sharp turning. Normal is the default, and the setting lasts for the session.
- Nearby prompts name activities such as fishing, the safehouse and pool.
- DEL opens a six-tile phone with icons for GPS, taxi, deposit, withdraw, scanner and delivery. Use the arrows to select a tile and ENTER to open it.
- From V11, replace EVOOPEN.py, EVOVIEW.py and EVOMENU.py. The ZIP still contains five Python files. [Roll back to V11](https://github.com/bhavishb-24/Last-Light/raw/ec6185b/Coastline-Evo-Open.zip).

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
