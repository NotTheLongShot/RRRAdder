# RRRAdder

If you're like me you probably have felt guilty leaving your wing in combat with empty guns or bingo fuel, even if
you've already shot down more than they have put together. No longer must you feel that pain! Simply land at an airfield
(see instructions for how to specify, but by default this will be any friendly active airfield in the mission box),
turn your engine off, and instruct the invisible ground crew to resupply you!

This script adds a maintenance truck to airfields in Pat Wilson's Campaign Generator IL-2 Great Battles: Flying Circus
careers. These zones allow you to rearm, refuel, and repair (RRR) your plane as well as heal your pilot (cheating).

## What does it do?
The script inserts one or more of a set of hand-placed maintenance vehicles onto airfields in the Arras Spring 1918 map.
It is written to be able to automatically do this for the latest mission in a PWCG campaign specified in a config file,
but it can also be used on any `.mission` file.

To do this it formats and appends a set of sections of text (see `RRRAdder.py` lines 74-140) to your `.mission` file
that instruct the game to insert vehicles and 'linked entities' that can perform the rearm/refuel/repair/heal function.

Then, because the game reads a `.msnbin` binary file that is generated from the `.mission` text file, the script can run
a program from 1C Studios (included in your game installation) called `MissionResaver.exe` that will create an updated
`.msnbin` file.

## **WARRANTY**
**Except as represented in this agreement, all work product by NotTheLongShot is provided “AS IS”. Other than as
provided in this agreement, NotTheLongShot makes no other warranties, express or implied, and hereby disclaims all
implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose.**


## Installation and use

### Installation
1. Download and install Python >=3.6.
   - There are no package dependencies outside the standard library.
2. Download the zipped repository from GitHub and unzip it into your installation directory, e.g.
   `C:\Program Files (x86)\1C Game Studios\IL-2 Sturmovik Great Battles\`
   1. You can put it elsewhere, just make sure to put the absolute path to the `data\Missions\PWCG` directory in the
      config file.

### Setup
1. Edit the `config.json` file to include:
   1. The `pwcg_missions_dir`, the directory for PWCG misisons. If you have put it in the IL-2 installation folder this
      can be left as the default relative path.
      1. Even if you are not using this with PWCG, please point this at a directory (doesn't have to exist) within the
         `data\Missions` directory, because the script uses this path to find `MissionResaver.exe` later.
      2. Make sure you use double-backslashes (`\\`) to delimit Windows paths!
   2. The `campaign_name` of your PWCG career; e.g. `D2`, `biggles_flies_again`, etc.
   3. Whether you want to `use_only_friendly`
      1. You can't use enemy locations anyway and nor can enemy AI, so you should probably leave it as `true` unless
         you're doing some kind of PvP coop.
      2. Countries are friendly to each other if they start with the same number (see Notes > Valid overrides) but I 
         haven't checked if they will 'maintain' one another.
   4. Whether you want to `run_missionresaver`. `MissionResaver.exe` is part of your IL-2: Great Battles installation
      and converts plaintext (`.mission`) files into mission binary (`.msnbin`) files. RRRAdder can run this command for
      you as a subprocess but if you're uncomfortable with that, set this to `false` and it will print the necessary 
      command but not run it.
   5. The `maintenanceRadius` - the area around the truck in which you can receive maintenance.
      1. Values between 10 and 80 will mean you probably have to taxi to somewhere near the truck.
      2. Values between 200 and 500 will probably mean you can get maintainance almost anywhere on the field, except in
         very large airfields.
   6. Which of the facilities you want - `rearm`/`refuel`/`repair`/`heal`.
      1. These must either be `true`/`false` (**case sensitive**) or `0`/`1`.
      2. Healing is cheating.
      3. TODO: does this actually do anything?
   7. The `rearmTime`, `refuelTime`, `repairTime`, and `healTime` multipliers. These should be >`0.0` for the facilities
      you have enabled.
      1. These do have an effect in some sense. If you set refuelTime to 1000000, refuelling becomes near-instantanious,
         but this is opposite of the expected behaviour as either a base time in seconds (or ticks of 20ms?) or a
         multiplier of an existing base time, as suggested by the STEditor UI.
   8. Which `airfields` you want to include.
      1. Leaving this list empty will include all locations.
      2. `home` will make the script include the closest airfield to your spawn point - your home field unless
         you're doing an air start.
      3. `active_in_mission_box` will include all airfields that are active (not abandoned) and within the mission box
         (depending on your PWCG CPU usage settings) as denoted by airfields that are <1 km away from an AA gun.
      4. Specific airfield names. A variety of airfield names are valid. For example, the airfield in square `1004.1`,
         can be included in the following ways:
         1. The specific airfield name given in the map (e.g. `Braizieux`). Some of these are only visible if you
            zoom in.
         2. The nearby town name used by PWCG (e.g. `Warley Bailion` and `Warloy Bailion`)
         3. The map spelling of the same town if it differs (e.g. `Warloy Baillon`).
         - If there are multiple airfields with related names (e.g. square `0711.1`, `Avesnes-le-Sec Ouest`) use the
            map airfield name (`Avesnes-le-Sec Ouest`) OR the PWCG spelling (`Avesnes Le Sec 3`), but NOT the map 
            spelling of the town name (`Avesnes-le-Sec`) if it differs.
      6. Airfield names are **case-sensitive *and* hyphen-sensitive**. If in doubt, look up the map name.
      7. If `use_only_friendly` is enabled, any airfields in your selection that are registered to the opposing forces
         will be ignored.
   9. `overrides` - see Notes > Valid overrides
- **N.B.** you can have more than one config.json file (e.g. one for each of your campaigns or pilots) in the directory - 
   see Usage pt. 4.ii and 4.iv.

### Usage
1. Generate the mission in PWCG and wait until it has finished creating the file.
2. Open a Command Prompt window by pressing the Windows key and typing `cmd`
3. Get the path of the script by Shift + Right-clicking on the file and selecting `Copy as path`:
4. Type `python ` into the prompt, paste your script path with `Ctrl+V`, then complete the command as follows:
   1. if you have just one config file and want to modify the latest mission in that campaign, don't add anything:
      - e.g. `python "C:\Program Files (x86)\1C Game Studios\IL-2 Sturmovik Great Battles\RRRAdder\RRRAdder.py"`
   2. If you have multiple config files and want to modify the latest mission in a campaign associated with your chosen 
      config, use the `-c` or `--config` argument:
      - e.g. `python "C:\Program Files (x86)\1C Game Studios\IL-2 Sturmovik Great Battles\RRRAdder\RRRAdder.py" -c my_config.json`
   3. If you want to modify a specific mission file regardless of the campaign it's in, use the `-m` or `--mission`
      argument:
      - e.g. `python "C:\Program Files (x86)\1C Game Studios\IL-2 Sturmovik Great Battles\RRRAdder\RRRAdder.py" -m my_mission.mission`
   5. If you have multiple config files and want to modify a specific mission regardless of the campaign it's in:
      - e.g. `python "C:\Program Files (x86)\1C Game Studios\IL-2 Sturmovik Great Battles\RRRAdder\RRRAdder.py" -c my_config.json -m my_mission.mission`
5. The program will wait to quit until you press the enter key. This is so if you put the command in a shortcut (see pt
   7) then you have a chance to check the output.
   - It doesn't matter if you forget to hit enter before loading the mission in IL-2
   - If you don't like this step, open your `RRRAdder.py` file in a text editor and delete line 540.
6. If you have elected not to have RRRAdder run `MissionResaver.exe`, run the suggested command to complete the mission
   setup.
   - NOTE: IL-2 will not see changes to the `.mission` file until it has been converted into a `.msnbin` file.
7. If you don't want to type out the command every time, you can set up a desktop shortcut as follows:
   1. Right-click on your desktop > New > Shortcut.
   2. In the location box, type or paste the command you used above.
      - There's no point in doing this if you're using the -m flag as per pt 4.iii or 4.iv.
   3. Click next and give it a name like RRRAdder or your campaign name if you're using a specific config file.
   4. You can now double-click it directly, or (given your desktop may be inaccessible when you're in IL-2) move it to
      the Start Menu (usually `C:\Users\<your username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`) or pin
      it to the Taskbar.

#### Ingame
  1. Load your latest PWCG mission in IL-2 Sturmovik: Great Battles.
  2. To use the maintenance zone, park your plane within the maintainance radius and switch the engine off. 
     1. I have placed the trucks approximately in the middle of the rows of hangers. Large airfields have two or three
        trucks. 
     2. If it's being finnicky, expand the `maintenanceRadius` parameter.
     3. The default keybindings are `RCtrl + A` (rearm) and `RCtrl + F` (refuel). They can be rebound in Weapons
        controls and Plane Engine controls respectively (at the end of the list). I think repair and healing happen
        automatically.


## Notes

### Valid overrides:
- `country` (type `int`). So far all the airfields west of the front are Great Britain WW1 (`302`) and all the ones
  east are Germany WW1 (`401`). If you're playing as French or American, you will want to override this to France WW1
  (`301`) or United States WW1 (`303`). The game also technically supports Belgium WW1 (`304`), Russia WW1 (`305`),
  and Austria-Hungary WW1 (`402`), but presumably these will not mean anything until FC Vol III and IV.
  - Overrides are applied at the last minute so the `use_only_friendly` parameter will be applied before everything is
    turned friendly.
- Positions (type `float`) (these will move all trucks to the same position - better to modify
  `data\vehicle_location.json`:
  - `xpos` - North-South position.
  - `ypos` - height above sea level.
  - `zpos` - West-East position.
- Euler rotation (type `float`).
  - `xori` - rotation around long axis (roll).
  - `yori` - rotation around vertical axis (yaw).
  - `zori` - rotation around short axis (pitch).
- `vulnerable` (`0` or `1`) - allows the trucks to be destroyed. Default `1`.
- `engageable` (`0` or `1`) - allows the trucks to be engaged by the AI. Default `1`.

### Testing
I have tested this with the following settings:
  - Non-Steam IL-2 Sturmovik: Great Battles v4.702c with Flying Circus Vol I+II and Battle of Bodenplatte enabled.
  - Pat Wilson's Campaign Generator: Flying Circus v13.7.0
  - A Jasta 6 (Cambrai North/Epinoy) career in late August '18 onwards.
  - Rearming and refuelling but not healing or repair.


## Troubleshooting
- If Windows automatically opens the Store app when you run a command starting with `python`, try `python3`. If that
  doesn't work, your python installation has gone wrong.
- `x86 : The term 'x86' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the
   spelling of the name, or if a path was included, verify that the path is correct and try again.` or similar: put
   quotation marks (`"`) round all your file paths.
- If your config file gets too messed up, or you want to make a new one, you can reset it by running
  `python path\to\RRRAdder\recreate_default_config.py`. If you want it to write somewhere specific, you can specify that
  as in`python recreate_default_config.py new_default_config.py`.
  - N.B. it will overwrite whatever file is at the location specified, or if none is specified it will overwrite
    `config.json`.


## TODO
- More options for choosing airfields?
- Placing fuel tankers and ambulances?
- Expand the code to add decorative spare planes to airfields depending on your squadron inventory? The home airfield
  always feels a bit empty.
- WW2 maps - someone else can do this if they like, I don't believe in planes with one wing and a canopy
  (cheating).
