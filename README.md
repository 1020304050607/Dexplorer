Dexplorer

Dex is a personal project for an full on terminal based file explorer built in Python. It was ispired by other terminal tools and other competitors Dex scopes to combine practicality with a easy to use TUI GUI.
Our goal was never to replace dominating file managers but to provide a lightweight and fun experience browsing managing files and cleaning trash inside your terminal.
Dex unlike many other TUIs focuses on simplicity and accessibility rather bloat and other useless stuff.

What Dex is not
Dex is not:
A non terminal GUI file manager and universal tool for every use case.

Instead it’s a light optimized terminal tool designed for quick navigation and file ops with the option to make it better via scripts.

Features

- File exploring: navigate directories with minimal keystrokes.

- Trash system: move files to trash restore them or wipes everything clean(with warning).

- Search: quick search files in directory or across the filesystem.

- Open with external tools:

- $EDITOR for text files

- mpv for media

- xdg-open for everything else

- File creation: new files, directories, Programming scripts, or shell scripts.

- Clipping operations: copy cut paste and clear.

- Sorting: by name size type or modification time.

- Optional: sudo editing.

- Minimal terminal design readable in any terminal.

Controls:

Default navigation is single-key driven:

1 / 2 - Move up/down

Enter - Open file or directory

4 - back

h - Help

q - Quit

Additional features, renaming, moving, trashing, restoring, and more (see help menu).

Modes:

Explorer mode: Default file navigation.

Trash mode: Browse and restore or delete trashed files.

Search mode: Accurate search with quick preview (unlike other file managers).

Sort mode: easy to use sorting of directory entries.

Installation

Dex is a single Python file. Just clone and run:

git clone https://github.com/yourname/dexplorer.git
cd dexplorer
./dex.py


Requirements:

Python 3.7+

mpv (optional, for media)

xdg-open (optional, for opening files)

Quickstart

Navigate to any directory and run:

./dex.py


From there:

Use 1/2 to move

Hit Enter to open

x to trash

T to enter trash menu

3 to search

Configuration

Dex reads environment variables for external tools:

EDITOR → Preferred text editor (falls back to vim or nano)

mpv → Media playback (default: mpv)

Other behaviors (batch size, sort order, delete confirmation) can be tweaked by editing the script directly — it’s meant to be hackable.

Screenshots / Demo

(Insert a terminal screenshot or asciinema gif here — this will massively boost stars on GitHub)

Discussion

Dex is still evolving. Contributions, scripts, and weird ASCII hacks are welcome.
Open issues, ideas, or share demos in the Discussions
.
