# Dexplorer

Dex is a personal project for an full on terminal based file explorer built in Python. It was ispired by other terminal tools and other competitors Dex scopes to combine practicality with a easy to use TUI GUI.  
Our goal was never to replace dominating file managers but to provide a lightweight and fun experience browsing managing files and cleaning trash inside your terminal.  
Dex unlike many other TUIs focuses on simplicity and accessibility rather bloat and other useless stuff.

## What Dex is not

Dex is not:  
- A non terminal GUI file manager and universal tool for every use case.  

Instead it’s a light optimized terminal tool designed for quick navigation and file ops with the option to make it better via scripts.

## Features

- File exploring: navigate directories with minimal keystrokes.  
- Trash system: move files to trash restore them or wipes everything clean (with warning).  
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

## Controls

Default navigation is single-key driven:  

- 1 / 2 - Move up/down  
- Enter - Open file or directory  
- 4 - Back  
- h - Help  
- q - Quit  

Additional features, renaming, moving, trashing, restoring, and more (see help menu).

## Modes

- Explorer mode: Default file navigation.  
- Trash mode: Browse and restore or delete trashed files.  
- Search mode: Accurate search with quick preview (unlike other file managers).  
- Sort mode: Easy to use sorting of directory entries.  

## Installation

```
git clone https://github.com/1020304050607/Dexplorer
cd Dexplorer 
chmod +x Dexplorer.sh
./Dexplorer
```
Requirements
Python 3.7+

mpv (optional, for media)

xdg-open (optional, for opening files)

From there:

Use 1/2 to move

Press Enter to open

x to trash

T to enter trash menu

3 to search

Screenshots / Demo
<img width="1368" height="768" alt="2025-09-06_21-30-17" src="https://github.com/user-attachments/assets/1f70ec51-92ab-4653-ae1e-71f5241d6556" /> <img width="1368" height="768" alt="2025-09-06_21-30-43" src="https://github.com/user-attachments/assets/c4789f83-b761-4bc3-a768-037efa631b33" /> <img width="1368" height="768" alt="2025-09-06_21-30-25" src="https://github.com/user-attachments/assets/d062870c-67b3-49f0-b510-5960db48d11d" /> <img width="1368" height="768" alt="2025-09-06_21-31-23" src="https://github.com/user-attachments/assets/7765ced3-d3b9-4c3e-b4f4-cb3014153873" /> <img width="1368" height="768" alt="2025-09-06_21-31-41" src="https://github.com/user-attachments/assets/e4785143-2018-4ac6-b5cf-a16b9b1b423a" />
Dex is still growing. Contributions scripts are allowed.
Open issues, ideas, or share demos in the Discussions.
