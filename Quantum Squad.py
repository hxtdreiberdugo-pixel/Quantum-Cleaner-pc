import os
import time

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = ""

SUSPICIOUS = [
    "xeno",
    "solara",
    "delta",
    "swift",
    "wave",
    "krnl",
    "fluxus",
    "synapse"
]

SCAN_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads")
]

# Global list para sa report ng files
report = []


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    cls()
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "              ECLIPSE PVP SECURITY")
    print(Fore.MAGENTA + "=" * 60)


def loading():
    print(Fore.CYAN + "\nInitializing Scan...\n")
    for i in range(21):
        percent = i * 5
        print(
            "\r[" + "█" * i + "░" * (20 - i) + f"] {percent:3d}%",
            end="",
            flush=True,
        )
        time.sleep(0.07)
    print("\n")


def scan():
    global report
    report.clear()

    warning = 0
    review = 0
    ok = 0

    loading()

    for folder in SCAN_FOLDERS:

        if not os.path.isdir(folder):
            continue

        print(Fore.CYAN + f"Scanning: {folder}\n")

        try:
            files = sorted(os.listdir(folder))
        except Exception:
            continue

        for file in files:
            path = os.path.join(folder, file)

            try:
                if not os.path.isfile(path):
                    continue

                low = file.lower()

                if (
                    any(x in low for x in SUSPICIOUS)
                    or ".jpg.exe" in low
                    or ".png.exe" in low
                ):
                    print(Fore.RED + "[WARNING] " + file)
                    warning += 1
                    report.append(("WARNING", path))

                elif low.endswith((
                    ".exe",
                    ".bat",
                    ".cmd",
                    ".ps1",
                    ".vbs",
                    ".scr"
                )):
                    print(Fore.YELLOW + "[REVIEW ] " + file)
                    review += 1
                    report.append(("REVIEW", path))

                else:
                    print(Fore.GREEN + "[OK      ] " + file)
                    ok += 1
                    report.append(("OK", path))

                time.sleep(0.03)
            except Exception:
                # Laktawan ang file kung biglang nagka-error habang nag-iiscan
                continue

        print()

    print(Fore.MAGENTA + "=" * 60)
    print(Fore.GREEN + f"OK Files       : {ok}")
    print(Fore.YELLOW + f"Review Files   : {review}")
    print(Fore.RED + f"Warning Files  : {warning}")
    print(Fore.MAGENTA + "=" * 60)

    if report:
        try:
            with open("scan_report.txt", "w", encoding="utf-8") as f:
                f.write("ECLIPSE PVP SECURITY REPORT\n")
                f.write(f"Date/Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")

                for status, path in report:
                    f.write(f"[{status}] {path}\n")

            print(Fore.CYAN + "\nFull logs saved as scan_report.txt")
        except Exception as e:
            print(Fore.RED + f"\nHindi mai-save ang report: {e}")

    input("\nPress Enter to continue...")


def delete_suspicious():
    """Bura lahat ng files na may markang WARNING at REVIEW sa huling scan."""
    global report
    
    # Check agad kung walang laman ang report para iwas error
    if not report:
        print(Fore.YELLOW + "\n[!] Walang data. Mag-scan muna (Option 1) bago magbura.")
        input("\nPress Enter to continue...")
        return

    # Sinasala ang WARNING at REVIEW files para burahin
    targets = [path for status, path in report if status in ("WARNING", "REVIEW")]

    if not targets:
        print(Fore.YELLOW + "\n[!] Walang nakitang WARNING o REVIEW (executable) files sa huling scan.")
        input("\nPress Enter to continue...")
        return

    print(Fore.RED + f"\n[!] WARNING: {len(targets)} file(s) (Warning/Review) ang mabubura permanenteng.")
    for path in targets:
        print(Fore.WHITE + f" -> {path}")

    confirm = input(Fore.YELLOW + "\nSigurado ka ba na gusto mo itong burahin? (yes/no): ").lower()
    
    if confirm == "yes":
        deleted_count = 0
        for path in targets:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(Fore.GREEN + f"[DELETED] {os.path.basename(path)}")
                    deleted_count += 1
            except Exception as e:
                # Saluhin ang error (e.g. Permission Denied) para hindi mag-close ang app
                print(Fore.RED + f"[ERROR] Hindi mabora ang {os.path.basename(path)}: {e}")
        
        print(Fore.GREEN + f"\n[+] Tapos na! {deleted_count} file(s) ang matagumpay na nabura.")
        
        # Ligtas na pag-update ng report list pagkatapos ng bura
        try:
            report = [item for item in report if item[1] not in targets]
        except Exception:
            report.clear()
    else:
        print(Fore.CYAN + "\n[x] Kinansela ang pagbura.")

    input("\nPress Enter to continue...")


# Main loop ng program
try:
    while True:
        banner()

        print("1. SCAN FILE")
        print("2. DELETE --- SUSPICIOUS OR WARNING FILE")
        print("3. EXIT")

        choice = input("\n> ")

        if choice == "1":
            scan()
        elif choice == "2":
            delete_suspicious()
        elif choice == "3":
            print(Fore.CYAN + "\nSalamat sa paggamit ng Eclipse Security!")
            time.sleep(1)
            break
except KeyboardInterrupt:
    print(Fore.CYAN + "\n\nProgram forced to exit.")
except Exception as main_err:
    print(Fore.RED + f"\nFatal Error encountered: {main_err}")
    input("\nPress Enter to close...")
