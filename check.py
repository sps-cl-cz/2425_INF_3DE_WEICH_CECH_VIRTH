# Při kontrole zapisování potřeba zakomentovat řádek 41
# Při kontrole mazání potřeba NEMÍT zakomentovaný řádek 41
# Řádek 14 otevře .check soubor a pracuje se s ním jako s "file"
#    Lze změnit z "w" na "w+" pro zápis i čtení

import hashlib
import glob
import argparse 

hash_souboru = ""
pathspec = r"README.md" # statická pathspec určena pro testování, poté bude prázdný

# vytvoření prázdného .check souboru
def init():
    with open('test.check', 'w') as file:
        file.write("")

init()

# vypočítání hashe
def vypocti_sha1(pathspec):
    sha1_hash = hashlib.sha1()
    with open(pathspec, "rb") as f:
        for bajtovy_blok in iter(lambda: f.read(4096), b""):
            sha1_hash.update(bajtovy_blok)
            hash_souboru = sha1_hash.hexdigest()
            print(f"SHA-1 hash souboru: {hash_souboru}")
    with open('test.check', 'w') as file: # Vytvoří/přepíše soubor test.check
        file.write(hash_souboru + " " + pathspec) # Co napíše do souboru test.check
        
vypocti_sha1(pathspec)

def pridat_soubor(pathspec):
    # user zadá cestu souboru
    vypocti_sha1(pathspec)

def remove_soubor(pathspec):
    with open('test.check', 'w+') as file: # Otevře soubor test.check
        content = file.readline() # přečte řádek (asi, idk co přesně dělá .readline)
        if (content.__contains__(pathspec)):
            content = ""
            file.remove(file.readline())

remove_soubor("README.md")

def main ():
     # Nějaký pokus o automatické zobrazení nápovědy
     # Funguje polovičně
     parser = argparse.ArgumentParser(description='Sledování změn v souborech', usage="%(prog)s [options]")

     subparsers = parser.add_subparsers()
     
     parser.add_argument('-init', help="Inicializování sledování")
     add_parser = subparsers.add_parser('add', help="přidá/aktualizuje soubory ke sledování")
     add_parser.add_argument('pathspec', help="Cesta k souboru nebo vzor pro soubory (např. *.txt)")
     parser.add_argument('remove', help="odebere soubory ke sledování")
     parser.add_argument('status', help="Zobrazí stav sledovaných souborů")
     
     parser.print_help()

if __name__ == "__main__":
    main()