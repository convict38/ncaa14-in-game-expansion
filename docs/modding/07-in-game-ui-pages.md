# In-game UI pages (EA menus): how our pages are added

Status 2026-10-29 (updated after the in-game settings test). Our own notes; no EA code, data or images are included here.

## The hook
The game's menus are EA APT movies (ActionScript 2) packed in BGFA archives. The title update carries the
`ncaa.PatchAddPod` movie, which the game loads at boot after the framework. Its only class does nothing in the
shipped game. We replace its init block with our own AS2 (assembled by our `apt_asm` tool) that:
- registers a "screen maker" first in the screen manager's list, so it can answer screen-enum lookups before EA's makers;
- installs prototype wrappers lazily (each wrapper calls EA's original method, then adds our change).

Only the title-update copy of a movie is served when the same movie also exists in the base archives, so every edit
goes into the title-update archive copy, served on the PC port through a read-only file overlay.

### Container size
The nested container that holds this movie stores payload offsets in 1 byte (x8), which caps the code at about
2 KB. New builds re-lay the container with 2-byte index fields, a layout 165 other nested containers in the same
archive already use (the loader reads field widths and alignment from each container header).

## Pages
| Page | Where | How | State |
|---|---|---|---|
| Settings tile "PC Controls & Display" | Main menu > Settings | the Origin account tile is relabelled at runtime and opens System Settings; its menu image (one entry of the title update's menu-image library) is replaced by our own icon | works in game |
| College Football Playoff | Dynasty hub > Dynasty Setup > "CFP Bracket" | an unused screen enum is mapped to EA's spreadsheet movie with our class; the 11 playoff rows are read per bowl from the league API; the row-change handler is replaced so the header card follows the row | works in game: winners from bracket progression, in-season rows labelled Projected/TBD; off-season champion and scores not readable (see below) |
| PC Controls & Display panel | System Settings, third tab | an unused settings category answered by a native C cave; the page's choices go through a 64-byte mailbox in guest memory to the PC runtime, which applies the keyboard layout and frame cap at once and writes `settings.ini` | works in game (PC port) |

## Settings flow (PC port)
Page -> EA settings adapter (vtable slots repointed to a C cave for our category only) -> mailbox (magic, version,
sequence, keys, fps, render scale, speed bundle) -> PC input code polls the sequence every 250 ms, applies keys and
fps live, rewrites only those four lines of `settings.ini`. The mailbox code runs only when a settings file is in use.

EA's settings pages save when the page is left, not on every toggle, so the runtime sees one change per visit.

## What the playoff page can read
The league API's bowl info holds the bowl id, both team ids, the game id, week, date, stadium, location, logo and
name, but no score or winner. Outside the bowl weeks the week/team game lookup returns the next season's placeholder
game (not played, no scores), so the page derives winners from the next round of the bracket, and a round whose
previous round still has open slots is shown as TBD (those slots still hold last season's teams).

## Assembler note
The game's VM reads the one-byte and two-byte integer push opcodes as signed values (stock code pushes 150 with the
two-byte form and -1 as byte 255). Our assembler now emits the byte form only for 0..127 and the short form up to 32767.
