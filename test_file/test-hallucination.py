import json
from config.confNeuron import confNeuron
from brain.brain import ABrain


# ==============================================================================
# SUITE DE REQUÊTES DE TEST (GARDE-FOUS ANTI-HALLUCINATION & NON-RÉGRESSION)
# ==============================================================================

TESTS_PIEGES = [
    {
        "id": "PIEGE_ACTU_1",
        "categorie": "Piège sous-chaîne ACTU ('info' dans 'informations')",
        "requete": "Donne-moi des informations sur le langage Python",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [3, 5, 15],
    },
    {
        "id": "PIEGE_ACTU_2",
        "categorie": "Piège sous-chaîne ACTU ('actu' dans 'actuellement')",
        "requete": "Que fais-tu actuellement ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [3, 15],
    },
    {
        "id": "PIEGE_HEURE_1",
        "categorie": "Piège HEURE (question de durée avec le mot 'heures')",
        "requete": "Combien d'heures dure un vol entre Paris et Tokyo ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [15],
    },
    {
        "id": "PIEGE_TEMP_1",
        "categorie": "Piège TEMPERATURE (question scientifique avec 'température')",
        "requete": "Quelle est la température de fusion du fer ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [4, 15],
    },
    {
        "id": "PIEGE_RADIO_1",
        "categorie": "Piège RADIO (question historique avec le mot 'radio')",
        "requete": "Qui a inventé la radio ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [22, 15],
    },
    {
        "id": "PIEGE_ARRET_1",
        "categorie": "Piège ARRET (question Python avec le verbe 'arrêter')",
        "requete": "Comment arrêter une boucle infinie en Python ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [15],
    },
    {
        "id": "PIEGE_WORK_1",
        "categorie": "Piège WORK (demande de script dans le chat sans projet ouvert)",
        "requete": "Écris-moi un petit script Python qui affiche bonjour",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [15, 16],
    },
    {
        "id": "PIEGE_MEMOIRE_1",
        "categorie": "Piège MEMOIRE (question matérielle avec le mot 'mémoire')",
        "requete": "Combien de mémoire RAM faut-il pour faire tourner Linux ?",
        "attendu_intent": "COMPLEXE",
        "attendu_neuron": "IA",
        "interdit_val_out": [5, 15],
    },
]

TESTS_NORMAUX = [
    {
        "id": "NORMAL_HEURE",
        "categorie": "Commande normale Fast-Track HEURE",
        "requete": "Quelle heure est-il ?",
        "attendu_intent_prefix": "HEURE",
        "attendu_neuron": "core",
    },
    {
        "id": "NORMAL_METEO",
        "categorie": "Commande normale Fast-Track METEO",
        "requete": "Quel temps fait-il à Paris ?",
        "attendu_intent_prefix": "METEO",
        "attendu_neuron": "core",
    },
    {
        "id": "NORMAL_ACTU",
        "categorie": "Commande normale Fast-Track ACTU TECH",
        "requete": "Donne-moi les actualités tech",
        "attendu_intent_prefix": "ACTU",
        "attendu_neuron": "core",
    },
    {
        "id": "NORMAL_CALC",
        "categorie": "Commande normale IARouter CALCULATRICE",
        "requete": "Calcule 25 fois 14",
        "attendu_intent_prefix": "COMPLEXE",
        "attendu_neuron": "IA",
    },
    {
        "id": "NORMAL_PROJET_LISTE",
        "categorie": "Commande normale Pré-filtre PROJET",
        "requete": "Liste mes projets",
        "attendu_intent_prefix": "COMPLEXE",
        "attendu_neuron": "IA",
    },
    {
        "id": "NORMAL_MEMOIRE_LISTE",
        "categorie": "Commande normale Pré-filtre MEMOIRE",
        "requete": "Qu'as-tu retenu sur moi ?",
        "attendu_intent_prefix": "COMPLEXE",
        "attendu_neuron": "IA",
    },
]


def init_brain() -> ABrain:
    conf = confNeuron(
        name="Opale",
        lang="fr",
        icon="asset/icon.png",
        asset="asset/",
        bute="developper un algo de ChatBot qui sera inclut dans SIX et Ryley",
        createur="Pauchet Baptiste",
        listFonction=[
            "ouvrir une application",
            "aider sur les recherches de internet",
            "donner la meteo",
            "faire un résumer des actualités",
        ],
        moteurderecherche="google",
        etatService=1,
        etatTime=1,
        etatOpen=1,
        etatSearch=1,
        etatChatbot=1,
        etatApi=1,
        etatCodehelp=1,
        etatWork=1,
        etatSocket=0,
        brief_enable=0,
        lienDoc="www.google.com",
        fichierLangue="language/tutoiment/",
        fichierKeyword="keyword/",
        voiceAssistant=False,
    )
    print("Initialisation d'ABrain et chargement du modèle GGUF...")
    brain = ABrain(conf)
    brain.boot()
    model_name = brain.getGestionnaire().getUserConf().get_ia_model()
    print(f"Modèle IA actif : {model_name}\n")
    return brain


def run_test_case(brain: ABrain, test: dict, is_piege: bool = True) -> bool:
    gest = brain.getGestionnaire()
    gest_ia = gest.getGestIA()
    requete = test["requete"]
    req_clean = gest.netoyageChaine(requete.lower())

    print("-" * 70)
    print(f"[{test['id']}] {test['categorie']}")
    print(f"  Requête         : \"{requete}\"")

    # 1. Test Passe 0 (classify_intent)
    intent_p0 = gest_ia.classify_intent(req_clean)
    print(f"  Passe 0 (Intent): {intent_p0}")

    # 2. Exécution complète dans ABrain.neuron()
    brain.neuron(requete)
    neuron_used = brain.getNeuronUsed()
    val_out = brain.getValeurSortie()
    sortie = brain.getListSortie()
    reponse_finale = sortie[0] if sortie else ""
    raw_json_p1 = gest_ia.get_reponse_ia() if neuron_used == "IA" else "(Fast-Track core_neuron)"

    print(f"  Neurone utilisé : {neuron_used} (valeurOut = {val_out})")
    if neuron_used == "IA":
        print(f"  Passe 1 (Brut)  : {str(raw_json_p1).strip()}")
    print(f"  Passe 2 (Finale): {reponse_finale}")

    # 3. Vérification du verdict
    ok = True
    raisons = []

    if is_piege:
        if intent_p0 != test["attendu_intent"]:
            ok = False
            raisons.append(f"Intent attendu '{test['attendu_intent']}', obtenu '{intent_p0}'")
        if neuron_used != test["attendu_neuron"]:
            ok = False
            raisons.append(f"Neurone attendu '{test['attendu_neuron']}', obtenu '{neuron_used}'")
        if val_out in test.get("interdit_val_out", []):
            ok = False
            raisons.append(f"Code sortie interdit déclenché (valeurOut={val_out})")
    else:
        prefix = test["attendu_intent_prefix"]
        if not intent_p0.startswith(prefix):
            ok = False
            raisons.append(f"Intent devait commencer par '{prefix}', obtenu '{intent_p0}'")
        if neuron_used != test["attendu_neuron"]:
            ok = False
            raisons.append(f"Neurone attendu '{test['attendu_neuron']}', obtenu '{neuron_used}'")

    if not reponse_finale or not reponse_finale.strip():
        ok = False
        raisons.append("Réponse finale vide")

    if ok:
        print("  VERDICT         : [OK]")
    else:
        print(f"  VERDICT         : [ECHEC] -> {', '.join(raisons)}")

    return ok


def run_suite(brain: ABrain, include_pieges: bool = True, include_normaux: bool = True):
    total = 0
    succes = 0

    if include_pieges:
        print("\n================ TESTS DES PHRASES PIÈGES ================")
        for t in TESTS_PIEGES:
            total += 1
            if run_test_case(brain, t, is_piege=True):
                succes += 1

    if include_normaux:
        print("\n=============== TESTS DES COMMANDES NORMALES ==============")
        for t in TESTS_NORMAUX:
            total += 1
            if run_test_case(brain, t, is_piege=False):
                succes += 1

    print("\n" + "=" * 70)
    print(f"RÉSULTAT GLOBAL : {succes} / {total} tests réussis")
    print("=" * 70 + "\n")


def mode_interactif(brain: ABrain):
    gest = brain.getGestionnaire()
    gest_ia = gest.getGestIA()
    print("\n--- Mode Test Interactif (tape 'q' pour revenir au menu) ---")
    while True:
        req = input("\nRequête à tester > ").strip()
        if not req or req.lower() == "q":
            break
        req_clean = gest.netoyageChaine(req.lower())
        intent_p0 = gest_ia.classify_intent(req_clean)
        print(f"  [Passe 0 - classify_intent] : {intent_p0}")

        brain.neuron(req)
        neuron_used = brain.getNeuronUsed()
        val_out = brain.getValeurSortie()
        reponse = brain.getListSortie()[0]
        if neuron_used == "IA":
            print(f"  [Passe 1 - JSON IARouter]   : {str(gest_ia.get_reponse_ia()).strip()}")
        print(f"  [Neurone / Code Sortie]     : {neuron_used} / valeurOut={val_out}")
        print(f"  [Passe 2 - Réponse Finale]  : {reponse}")


def test_optimisations_ia(brain: ABrain):
    import time
    gest = brain.getGestionnaire()
    gest_ia = gest.getGestIA()
    ia_loader = gest_ia._gestIA__ia_loader

    print("\n================ TEST DES OPTIMISATIONS IA ================")

    # 1. Test du pré-classifieur Python (0 ms, sans appel LLM)
    t0 = time.perf_counter()
    intent_fast_1 = gest_ia.classify_intent("quelle heure est il")
    intent_fast_2 = gest_ia.classify_intent("liste mes projets")
    intent_fast_3 = gest_ia.classify_intent("donne moi les actualites tech")
    dt_ms = (time.perf_counter() - t0) * 1000

    ok_fast = (intent_fast_1 == "HEURE" and intent_fast_2 == "COMPLEXE" and intent_fast_3 == "ACTU TECH")
    print(f"1. Pré-filtre Python 0ms : {'[OK]' if ok_fast else '[ECHEC]'} ({dt_ms:.3f} ms pour 3 requêtes)")
    print(f"   - 'quelle heure est il'          -> {intent_fast_1}")
    print(f"   - 'liste mes projets'            -> {intent_fast_2}")
    print(f"   - 'donne moi les actualites tech'-> {intent_fast_3}")

    # 2. Vérifier chargement à la demande (Lazy Loading)
    print("\n2. Test Lazy Loading & Auto-Unload RAM :")
    if ia_loader.is_model_loaded():
        print("   - Modèle déjà chargé en RAM, déchargement manuel pour tester le Lazy Load...")
        ia_loader.unload_model(keep_instructions=True)

    etat_avant = ia_loader.is_model_loaded()
    print(f"   - État du modèle avant requête LLM : {'Chargé' if etat_avant else 'Non chargé (0 Mo RAM)'}")

    print("   - Envoi d'une requête rapide pour déclencher le chargement automatique...")
    brain.neuron("Quelle heure est-il ?")
    etat_pendant = ia_loader.is_model_loaded()
    print(f"   - État du modèle après requête     : {'Chargé [OK]' if etat_pendant else 'Non chargé [ECHEC]'}")

    # 3. Test Auto-Unload après inactivité (timeout réduit à 3s pour le test)
    print("   - Test de l'Auto-Unload (timeout temporaire fixé à 3 secondes)...")
    gest_ia.set_idle_timeout(3)
    time.sleep(4.2)
    etat_apres_idle = ia_loader.is_model_loaded()
    gest_ia.set_idle_timeout(180)
    print(f"   - État du modèle après 4s d'inactivité : {'Déchargé de la RAM [OK]' if not etat_apres_idle else 'Encore chargé [ECHEC]'}")
    print("===========================================================\n")


def test_ia_os_directory():
    import os
    import stat
    from librairy.model_downloader import model_downloader

    print("\n======== TEST DU MODE OS LINUX (/arrera/ia_model) ========")
    # 1. Mode standard (ia_os_directory=False)
    dl_user = model_downloader(ia_os_directory=False)
    dir_user = dl_user._model_downloader__modelDir
    print(f"1. Mode standard (ia_os_directory=False) :")
    print(f"   - Dossier utilisé : {dir_user}")
    print(f"   - Modèles détectés: {dl_user.get_model_download()}")

    # 2. Mode OS Linux (ia_os_directory=True)
    print("\n2. Mode OS Linux (ia_os_directory=True) :")
    dl_os = model_downloader(ia_os_directory=True)
    dir_os = dl_os._model_downloader__modelDir
    use_os_active = dl_os._model_downloader__use_os_dir

    if use_os_active and dir_os == "/arrera/ia_model/":
        mode_dir = oct(stat.S_IMODE(os.stat(dir_os).st_mode))
        json_file = os.path.join(dir_os, "model_download.json")
        mode_json = oct(stat.S_IMODE(os.stat(json_file).st_mode)) if os.path.isfile(json_file) else "N/A"
        print(f"   - Statut          : [OK] Dossier OS actif ({dir_os})")
        print(f"   - Permissions     : dossier={mode_dir} (attendu 0o777), json={mode_json} (attendu 0o666)")
        print(f"   - Modèles détectés: {dl_os.get_model_download()}")
    else:
        print(f"   - Statut          : [REPLI SÉCURISÉ ACTIF] -> {dir_os}")
        print("   - Explication     : /arrera/ia_model n'existe pas encore sur ta Fedora.")
        print("   - Pour tester le mode OS complet sur ta Fedora, lance dans un terminal :")
        print("     sudo mkdir -p /arrera/ia_model && sudo chmod 777 /arrera/ia_model")
        print("     (et optionnellement : cp ~/.config/arrera-model/*.gguf /arrera/ia_model/)")
    print("==========================================================\n")


def main():
    brain = init_brain()
    while True:
        print("\n==================================================")
        print("   SUITE DE TESTS ANN (IA, OPTIMISATIONS & OS)    ")
        print("==================================================")
        print("1. Lancer TOUTE la suite anti-hallucination (Pièges + Normaux)")
        print("2. Lancer uniquement les 8 phrases PIÈGES")
        print("3. Lancer uniquement les 6 commandes NORMALES")
        print("4. Mode interactif (inspecter Passe 0 / Passe 1 / Passe 2)")
        print("5. Tester les optimisations IA (Pré-filtre 0ms, Lazy Load, Auto-Unload RAM)")
        print("6. Tester ia_os_directory (/arrera/ia_model sous Fedora Linux)")
        print("0. Quitter")
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            run_suite(brain, include_pieges=True, include_normaux=True)
        elif choix == "2":
            run_suite(brain, include_pieges=True, include_normaux=False)
        elif choix == "3":
            run_suite(brain, include_pieges=False, include_normaux=True)
        elif choix == "4":
            mode_interactif(brain)
        elif choix == "5":
            test_optimisations_ia(brain)
        elif choix == "6":
            test_ia_os_directory()
        elif choix == "0":
            brain.shutdown()
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()

