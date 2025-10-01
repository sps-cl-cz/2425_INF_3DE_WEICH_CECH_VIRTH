import hashlib
import glob
import argparse 
import time
from datetime import datetime

# vytvoření prázdného .check souboru
def init():
    print("Inicializace sledování...")
    for i in range(5):
        print(i + 1)
        time.sleep(1)
    with open('hash.check', 'w') as file:
        file.write("")
    print("Inicializace dokončena")

# vypočítání hashe
def vypocti_sha1(pathspec):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sha1_hash = hashlib.sha1()
    hash_souboru = ""

    # vypočítání hashe
    with open(pathspec, "rb") as f:
        for bajtovy_blok in iter(lambda: f.read(4096), b""):
            sha1_hash.update(bajtovy_blok)

        hash_souboru = sha1_hash.hexdigest()
        print(f"SHA-1 hash souboru: {hash_souboru}")

    with open('hash.check', 'r') as file:
            content = file.readlines()
            if not any(hash_souboru in line for line in content): # V případě, že hash v .check souboru ještě není, napíše ho na nový řádek
                with open('hash.check', 'a') as f:
                    f.write(f"{hash_souboru} {pathspec} {timestamp}\n") # Co napíše do souboru hash.check
        
def add_soubor(pathspec):
    print("Přidávání souboru...")
    for i in range(5):
        print(i + 1)
        time.sleep(1)

    matched_files = glob.glob(pathspec)

    if not matched_files:
        print(f"Nebyly nalezeny žádné soubory odpovídající vzoru: {pathspec}")
        return
    
    print(f"Bylo nalezeno {len(matched_files)} souborů")
    for file in matched_files:
        print(f"Prídávání souboru {file}")
        vypocti_sha1(file)
    
    print("Přidávání dokončeno")

def remove_soubor(pathspec):
    print("Odstraňování souboru...")
    for i in range(5):
        print(i + 1)
        time.sleep(1)
    with open('hash.check', 'w+') as file:
        matched_files = glob.glob(pathspec)
        content = file.readline()
        for f in matched_files:
            if content == f:
                content = ""
                file.remove(file.readline())
    print("Odstraňování dokončeno")

def status_souboru():
    print("Kotrolování souborů...")
    for i in range(5):
        print(i + 1)
        time.sleep(1)
    # Zobrazí stav sledovaných souborů.
    try:
        with open('hash.check', 'r') as file:
            content = file.readlines()
            if content:
                ok_count = 0
                change_count = 0
                error_count = 0
                for line in content:
                    sha1_hash, path, timestamp = line.strip().split(" ", 2)
                    try:
                        # Zkontroluje jestli soubor existuje
                        with open(path, 'rb') as f:
                            current_hash = hashlib.sha1(f.read()).hexdigest()
                            if current_hash == sha1_hash:
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                                print(f"[OK] {sha1_hash} {timestamp} {path}")
                                ok_count += 1
                            else:  
                                print(f"[CHANGE] {sha1_hash} {timestamp} {path}")
                                print(f"NEW HASH: {current_hash}")
                                change_count += 1
                    except FileNotFoundError:
                        print(f"[ERROR] Soubor nebyl nalezen: {path}")
                        error_count += 1

                print(f"\n{ok_count} OK, {change_count} CHANGE, {error_count} ERROR")
            else:
                print("Žádné soubory nejsou sledovány.")
    except FileNotFoundError:
        print("Soubor 'hash.check' nebyl nalezen. Ujistěte se, že byl inicializován.")

def show_help():
    parser = argparse.ArgumentParser(usage="check.py <příkaz>")

    subparsers = parser.add_subparsers(title = None, metavar = "Dostupné příkazy:")

    init_parser = subparsers.add_parser("check.py init", help = "Inicializuje sledování", usage = "check.py init")
    add_parser = subparsers.add_parser("add <pathspec>", help = "přidá soubor ke sledování", usage = "check.py add <pathspec>")
    add_parser.add_argument("pathspec", help = "Cesta k souboru nebo vzor pro soubor (např. *.txt)")
    remove_parser = subparsers.add_parser("check.py remove <pathspec>", help = "Odebere soubor ze sledování", usage = "check.py remove <pathspec>")
    status_parser = subparsers.add_parser("check.py status", help = "zobrazí stav sledovaných souborů", usage = "check.py status")
    exit_parser = subparsers.add_parser("check.py exit", help = "Ukončí program", usage = "check.py exit")

    parser.print_help()

# volání funkce pro určitý příkaz
def check_input(command, pathspec):
    try:
        match command:
            case "init":
                init()
            case "add":
                add_soubor(pathspec)
            case "remove":
                remove_soubor(pathspec)
            case "status":
                status_souboru()
            case "-h":
                show_help()
            case "exit":
                exit()
            case _:
                print("Invalid command. Use 'check.py -h' to show help")
    except Exception as e:
        print(e)


def main ():

    while True:
        user_input = input("Zadejte příkaz: ").strip()
        
        # V případě, že cesta k souboru obsahuje mezery, tak se cesta nerozdělí, protože je vždy zadávána jako 3. část
        input_parts = user_input.split(maxsplit=2)

        #Pokud uživatel nezadná určitou část příkazu, nastaví se na prázdný string
        checkpy = input_parts[0].lower() if len(input_parts) > 0 else ""

        if len(input_parts) > 1:
            command = input_parts[1].lower()
        else:
            command = ""

        if len(input_parts) > 2:
            pathspec = input_parts[2].lower()
        else:
            pathspec = ""

        if checkpy == "check.py":
            check_input(command, pathspec)
        else:
            print("Invalid prefix. Use 'check.py -h' to show help")

if __name__ == "__main__":
    main()