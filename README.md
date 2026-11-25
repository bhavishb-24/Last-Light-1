# Last Light / Coastline

An original open-world action-adventure game for the TI-84 Evo. Explore a compact South Florida-inspired city, follow Lena and Sol through a complete story, and take side trips by car, skiff, floatplane, jet ski, or airboat.

## Evo Open World edition

This smaller calculator build includes walking, driving, shops, a city map, and a story. Unzip [Coastline-Evo-Open.zip](Coastline-Evo-Open.zip), send all five Python files through TI Connect Evo, then run EVOOPEN from PRGM → Python App.

See the [version notes and rollback instructions](Coastline-Evo-Open/CHANGES.md).

### Optional clip intro

[Coastline-Evo-Clip.zip](Coastline-Evo-Clip.zip) shows two sharper stills sampled from the supplied video's first 20 seconds. Each is 96 × 54 with 16 colors. Press ENTER to skip. If you already have V13 or the earlier Clip Edition, replace only EVOSPORT.py and look for CLIP HD on the title menu.

### Native image playback test

[Download the 5 FPS test ZIP](Coastline-Evo-5FPS-Test.zip). Extract it and send CLIP00.8xv2 by itself using WebTILP first. If accepted, send the other nine pictures and replace CLIPTEST.py. The revised test uses 160 × 90 RLE pictures. Run CLIPTEST in the Python App. The test displays the slowest frame draw, late frame count and total elapsed time. It runs separately from the game.

## Compact driving edition

If the full Coastline package runs out of memory on your calculator, try the standalone [Coastline-Evo-Lite.zip](Coastline-Evo-Lite.zip). It has a 12-district route map, delivery jobs, and perspective driving. It omits on-foot exploration and the phone systems. Transfer only LASTLITE.py from the ZIP and run LASTLITE in the Python App.

## Download and install

Download [Coastline-Evo.zip](Coastline-Evo.zip) and extract it on your computer. Send all ten Python files together to your calculator with [TI Connect Evo](https://connectevo.ti.com/). On the calculator, open **PRGM → Python App**, select **COASTRUN**, and press **Run**.

Read [the play and installation guide](Coastline/PLAY.md) for controls, districts, checkpoint saves, transfer details, and activities. The original Python source files are in [Coastline/](Coastline/).

![Coastline gameplay preview](Coastline/preview.png)

The game is written in Python for the TI-84 Evo. It uses the built-in ti_draw, ti_system, and time modules. It does not write files or modify calculator variables. The story, map, characters, and artwork are original.
