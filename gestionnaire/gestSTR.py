class gestSTR :
    def __init__(self):
        pass

    def netoyage(self,c:str):
        chaine = str(c)
        chaine = chaine.replace("-"," ")
        chaine = chaine.replace('"'," ")
        chaine = chaine.replace("_"," ")
        #chaine = chaine.replace('/'," ")
        chaine = chaine.replace("é","e")
        chaine = chaine.replace("è","e")
        chaine = chaine.replace("à","a")
        chaine = chaine.replace("ç","c")
        chaine = chaine.replace("ê","e")
        chaine = chaine.replace("ô","o")
        chaine = chaine.replace("ù","u")
        chaine = chaine.replace("û","u")
        chaine = chaine.replace("î","i")
        chaine = chaine.replace("â","a")
        chaine = chaine.replace("ë","e")
        chaine = chaine.replace("ï","i")
        chaine = chaine.replace("ü","u")
        chaine = chaine.replace("ö","o")
        return chaine.lower()
    
    def firstMots(chaine:str,liste:list):
        listeMots = liste
        indexMin = float('inf')
        motsMin = ""
        for mots in listeMots:
            index = chaine.find(mots)
            if index != -1 and index < indexMin:
                indexMin = index
                motsMin = mots

        return motsMin