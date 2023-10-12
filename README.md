# tuiTimer
tuiTimer is a speedcubing timer inspired by csTimer but in a TUI.

**THIS PROJECT IS IN EARLY BETA AND THERE WILL PROBABLY BE MANY BUGS**

## Installation
```
git clone https://github.com/Nqtural/tuiTimer/
cd tuiTimer
python main.py
```

## Configuration
Edit `config.py` to configure tuiTimer. All parameters must be set if the file exists.

## Usage
Run with flag `-s [PATH]` or `--session [PATH]` to resume a previous session.
### Keybinds
#### General
* Use `F1`, `F2`, `F3` and `F4` for switching tabs.
* Press `ctrl` + `c` to exit
#### Timer
* Hold `space` in the timer tab until timer turns green and then release to start timer. Stop by pressing `space` again.
#### Solves
* `+` will toggle +2 for selected solve.
* `d` will toggle DNF for selected solve.
* `delete` and `backspace` will prompt you to delete the active solve. `y` confirms deletion.
#### Algorithms
* Arrow keys `left` and `right` switches to the previous and next algorithm page respectively. `space` and arrow keys `up` and `down` switches between OLL and PLL algorithms.
* `home` will take you to the first algorithm page.
