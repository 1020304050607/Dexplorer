#!/usr/bin/env python3
import os, sys, time, shutil, subprocess
from pathlib import Path
import tty, termios

TRASH = Path.home() / ".local/share/Trash/files"
if not TRASH.exists(): TRASH.mkdir(parents=True)
SEL = 0
BATCH = 20
CUR = Path.home()
SORT = "name"
ORDER = "asc"
SHOW_HIDDEN = False
BUFFER = {"mode": None, "items": []}
EDITOR = os.environ.get("EDITOR") or shutil.which("vim") or shutil.which("nano") or "nano"
MPV = shutil.which("mpv") or "mpv"
FEH = shutil.which("feh") or "feh"
MEDIA_VIEWER = "mpv"  # Default to mpv, toggle with '9'
SHOW_DELETE_CONFIRM = True

def file_size(n):
    try:
        n = int(n)
        if n < 1024: return f"{n}B"
        elif n < 1024**2: return f"{n/1024:.1f}K"
        elif n < 1024**3: return f"{n/1024**2:.1f}M"
        else: return f"{n/1024**3:.1f}G"
    except ValueError:
        return "-"

def get_entries(path):
    result = []
    try:
        sources = list(path.glob("*"))
        if SHOW_HIDDEN:
            sources += list(path.glob(".*"))
        for entry in sources:
            if entry.name not in (".", "..") and entry.exists():
                result.append(entry)
    except PermissionError:
        print(f"[oops] No access to {path}")
    return result

def draw(entries):
    os.system("clear")
    print(f"Dexplorer v1.1 - made by Dveloper (watch the trash!)")
    print(f"current path: {CUR} | viewer: {MEDIA_VIEWER}\n")
    print(f"{'#':<4}{'name':<55}{'size':<8}{'modified':<20}")
    if not entries:
        print("(empty folder)")
        return
    start = (SEL // BATCH) * BATCH
    end = min(start + BATCH, len(entries))
    for idx, ent in enumerate(entries[start:end], start=start):
        size = "-"
        mtime = "-"
        try:
            if ent.is_file():
                size = file_size(ent.stat().st_size)
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ent.stat().st_mtime))
        except (PermissionError, FileNotFoundError):
            pass
        prefix = "> " if idx == SEL else "  "
        print(f"{prefix}{idx+1:<3}{ent.name:<55}{size:<8}{mtime:<20}")
    print("\ncontrols: 1 up 2 down Enter open 4 back 3 search 9 toggle viewer h help q quit")

def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def show_help():
    os.system("clear")
    print("""
Dexplorer v1.1 Help - Keybindings

Navigation:
  1 - Move up
  2 - Move down
  Enter - Open file/dir
  4 - Go back
  3 - Search files
  9 - Toggle media viewer (mpv/feh)

File Operations:
  n - New file
  d - New directory
  p - New Python script
  b - New Bash script
  g - New project (dir + script)
  r - Rename file
  m - Move file to path

Copy/Paste:
  c - Copy file
  t - Cut file
  l - Paste file(s)
  u - Clear copy buffer

Edit/View:
  e - Edit in $EDITOR
  o - Open with xdg-open
  v - View with current media viewer
  S - Sudo edit
  9 - Toggle mpv/feh for media

Trash:
  x - Move to trash
  T - View trash
  R - Restore from trash
  r - Delete one from trash
  A - Empty trash

Sort & Display:
  5 - Sort (name/size/mtime/type/order)
  h - Toggle hidden files
  q - Quit
""")
    input("enter to continue")

def open_file(entry):
    if entry.is_dir():
        return entry
    ext = entry.suffix.lower()
    media = {".png", ".jpg", ".jpeg", ".gif"}
    videos = {".mp4", ".mkv", ".webm"}
    try:
        if ext in media:
            if MEDIA_VIEWER == "feh":
                subprocess.run([FEH, str(entry)], check=True)
            else:
                subprocess.run([MPV, str(entry)], check=True)
        elif ext in videos:
            subprocess.run([MPV, str(entry)], check=True)
        else:
            subprocess.run([EDITOR, str(entry)], check=True)
    except subprocess.CalledProcessError:
        print(f"[oops] Couldn't open {entry.name}")
    return entry

def move_to_trash(entry):
    try:
        destination = TRASH / entry.name
        shutil.move(str(entry), destination)
        print(f"Moved {entry.name} to trash")
    except (shutil.Error, OSError):
        print(f"[oops] Failed to move {entry.name} to trash")

def confirm_delete(prompt):
    global SHOW_DELETE_CONFIRM
    if not SHOW_DELETE_CONFIRM:
        return True
    choice = 1
    print(prompt)
    print("1) Yes   2) No   press . to never show again")
    while True:
        k = read_key()
        if k == "1": choice = 1
        elif k == "2": choice = 2
        elif k == ".": SHOW_DELETE_CONFIRM = False; return True
        elif k in ("\r", "\n"): return choice == 1

def trash_menu():
    trash_entries = get_entries(TRASH)
    if not trash_entries:
        print("Trash empty! 🎉")
        input("press enter to continue")
        return
    sel_trash = 0
    while True:
        os.system("clear")
        print(f"Trash view - {TRASH}\n")
        for idx, item in enumerate(trash_entries):
            if not item.exists(): continue
            size = "-"
            mtime = "-"
            try:
                if item.is_file(): size = file_size(item.stat().st_size)
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.stat().st_mtime))
            except (PermissionError, FileNotFoundError): pass
            prefix = "> " if idx == sel_trash else "  "
            print(f"{prefix}{idx+1:<3}{item.name:<55}{size:<8}{mtime:<20}")
        print("\n1 up 2 down Enter open b back R restore r remove one A remove all")
        ch = read_key()
        if ch == "1": sel_trash = max(0, sel_trash-1)
        elif ch == "2": sel_trash = min(len(trash_entries)-1, sel_trash+1)
        elif ch in ("\r", "\n"): open_file(trash_entries[sel_trash])
        elif ch.lower() == "b": break
        elif ch.lower() == "r":
            if confirm_delete(f"Delete {trash_entries[sel_trash].name}?"):
                try:
                    trash_entries[sel_trash].unlink(missing_ok=True)
                    trash_entries.pop(sel_trash)
                    sel_trash = min(sel_trash, len(trash_entries)-1)
                    print(f"Deleted {trash_entries[sel_trash].name}")
                except PermissionError:
                    print(f"[oops] Can't delete {trash_entries[sel_trash].name}")
        elif ch.upper() == "A":
            if confirm_delete("Delete ALL files in trash?"):
                for it in trash_entries:
                    try: it.unlink(missing_ok=True)
                    except PermissionError: pass
                trash_entries = []
                print("Trash emptied! 🗑️")
                input("press enter")
                break
        elif ch.upper() == "R":
            try:
                restore = trash_entries[sel_trash]
                shutil.move(str(restore), CUR/restore.name)
                trash_entries.pop(sel_trash)
                sel_trash = min(sel_trash, len(trash_entries)-1)
                print(f"Restored {restore.name} to {CUR}")
            except (shutil.Error, OSError):
                print("Restore failed, maybe name conflict?"); input("press enter")

def main():
    global CUR, SEL, SORT, ORDER, SHOW_HIDDEN, BUFFER, MEDIA_VIEWER
    while True:
        entries = get_entries(CUR)
        if SEL >= len(entries): SEL = max(0, len(entries)-1)
        draw(entries)
        key = read_key()
        if key == "1": SEL = max(0, SEL-1)
        elif key == "2": SEL = min(len(entries)-1, SEL+1)
        elif key in ("\r", "\n"): 
            if entries: CUR = open_file(entries[SEL]) or CUR
        elif key == "4": CUR = CUR.parent; SEL = 0
        elif key == "h": show_help()
        elif key == "q": break
        elif key == "n": 
            nm = input("name: "); 
            try: (CUR/nm).touch()
            except OSError: print(f"[oops] Can't create {nm}")
        elif key == "d": 
            nm = input("dirname: "); 
            try: (CUR/nm).mkdir(exist_ok=True)
            except OSError: print(f"[oops] Can't create dir {nm}")
        elif key == "p": 
            nm = input("py name: "); 
            p = CUR/(nm+".py")
            try: 
                p.write_text("print('hello')"); 
                p.chmod(0o755)
            except OSError: print(f"[oops] Can't create {nm}.py")
        elif key == "b": 
            nm = input("sh name: "); 
            p = CUR/(nm+".sh")
            try: 
                p.write_text("echo hello"); 
                p.chmod(0o755)
            except OSError: print(f"[oops] Can't create {nm}.sh")
        elif key == "g": 
            nm = input("prog name: "); 
            pd = CUR/nm
            try: 
                pd.mkdir(exist_ok=True); 
                (pd/(nm+".sh")).write_text("echo run"); 
                (pd/(nm+".sh")).chmod(0o755)
            except OSError: print(f"[oops] Can't create project {nm}")
        elif key == "c": BUFFER = {"mode": "copy", "items": [str(entries[SEL])]}
        elif key == "t": BUFFER = {"mode": "cut", "items": [str(entries[SEL])]}
        elif key == "l":
            for item_path in BUFFER["items"]:
                src = Path(item_path)
                dst = CUR/src.name
                try:
                    if BUFFER["mode"] == "cut": 
                        shutil.move(str(src), dst)
                        print(f"Moved {src.name} to {dst}")
                    else: 
                        shutil.copy2(str(src), dst)
                        print(f"Copied {src.name} to {dst}")
                except (shutil.Error, OSError): 
                    print(f"[oops] Can't paste {src.name}")
            if BUFFER["mode"] == "cut": BUFFER = {"mode": None, "items": []}
        elif key == "u": 
            BUFFER = {"mode": None, "items": []}
            print("Copy buffer cleared")
        elif key == "r": 
            nn = input("new name: "); 
            try: 
                entries[SEL].rename(CUR/nn)
                print(f"Renamed to {nn}")
            except OSError: print(f"[oops] Can't rename to {nn}")
        elif key == "m": 
            dest = Path(input("move to path: "))
            try: 
                shutil.move(str(entries[SEL]), dest)
                print(f"Moved to {dest}")
            except (shutil.Error, OSError): print(f"[oops] Can't move to {dest}")
        elif key == "x": move_to_trash(entries[SEL])
        elif key.upper() == "T": trash_menu()
        elif key == "e": 
            try: 
                subprocess.run([EDITOR, str(entries[SEL])], check=True)
                print(f"Edited {entries[SEL].name}")
            except subprocess.CalledProcessError: print(f"[oops] Can't edit {entries[SEL].name}")
        elif key == "v": 
            try: 
                if entries[SEL].suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mkv", ".webm"}:
                    viewer = FEH if MEDIA_VIEWER == "feh" and entries[SEL].suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"} else MPV
                    subprocess.run([viewer, str(entries[SEL])], check=True)
                    print(f"Viewed {entries[SEL].name} with {viewer}")
                else:
                    print(f"[oops] Not a supported media file")
            except subprocess.CalledProcessError: print(f"[oops] Can't view {entries[SEL].name}")
        elif key == "o": 
            try: 
                subprocess.run(["xdg-open", str(entries[SEL])], check=True)
                print(f"Opened {entries[SEL].name}")
            except subprocess.CalledProcessError: print(f"[oops] Can't open {entries[SEL].name}")
        elif key == "S": 
            try: 
                subprocess.run(["sudo", EDITOR, str(entries[SEL])], check=True)
                print(f"Sudo edited {entries[SEL].name}")
            except subprocess.CalledProcessError: print(f"[oops] Can't sudo edit {entries[SEL].name}")
        elif key == "9":
            MEDIA_VIEWER = "feh" if MEDIA_VIEWER == "mpv" else "mpv"
            print(f"Media viewer set to {MEDIA_VIEWER}")
        elif key == "3":
            term = input("search: ").strip()
            scope = input("scope a=all/d=dir: ").lower()
            found = []
            try:
                if scope == "a":
                    for f in Path("/").rglob(f"*{term}*"): found.append(f)
                else:
                    for f in CUR.rglob(f"*{term}*"): found.append(f)
            except PermissionError:
                print(f"[oops] No access for search")
            if not found: print("No results"); input("enter"); continue
            sel_search = 0
            while True:
                os.system("clear")
                print(f"Search results for '{term}' ({len(found)} found):\n")
                for idx, f in enumerate(found):
                    size = "-"
                    mtime = "-"
                    try: 
                        if f.is_file(): size = file_size(f.stat().st_size)
                        mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(f.stat().st_mtime))
                    except (PermissionError, FileNotFoundError): pass
                    prefix = "> " if idx == sel_search else "  "
                    print(f"{prefix}{idx+1:<3}{f.name:<55}{size:<8}{mtime:<20}")
                print("\n1 up 2 down Enter open b back")
                ch = read_key()
                if ch == "1": sel_search = max(0, sel_search-1)
                elif ch == "2": sel_search = min(len(found)-1, sel_search+1)
                elif ch in ("\r", "\n"):
                    if found: CUR = open_file(found[sel_search]) or CUR
                    break
                elif ch.lower() == "b": break
        elif key == "5":
            option = input("sort name/size/mtime/type(n/s/m/t) order(o) hidden(h): ")
            sort_map = {"n": "name", "s": "size", "m": "mtime", "t": "type"}
            if option in sort_map: 
                SORT = sort_map[option]
                print(f"Sorted by {SORT}")
            elif option == "o": 
                ORDER = "desc" if ORDER == "asc" else "asc"
                print(f"Order set to {ORDER}")
            elif option == "h": 
                SHOW_HIDDEN = not SHOW_HIDDEN
                print(f"Hidden files {'shown' if SHOW_HIDDEN else 'hidden'}")

if __name__ == "__main__":
    main()
