from config.tiger_demon import tiger_demon

VERSION = "dev"

def main():
    demon = tiger_demon("six",VERSION)
    if (demon.checkUpdate()):
        print("MAJ")
    else :
        print("Pas MAJ")

    print(f"Version local : {demon.get_local_version()}")
    print(f"Version en ligne : {demon.get_online_version()}")


if __name__ == "__main__":
    main()