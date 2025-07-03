README - Projet Gestion Déchets Électroniques API

Installation et lancement

1. Cloner le dépôt
   git clone https://github.com/hatimkd/gestionDechetsElectroniques_api.git
   cd gestionDechetsElectroniques_api

2. Créer un environnement virtuel (recommandé)
   - Sur Windows :
     python -m venv venv
     venv\Scripts\activate.bat

   - Sur Linux / macOS :
     python3 -m venv venv
     source venv/bin/activate

3. Installer les dépendances
   pip install -r requirements.txt

4. Configurer la base de données
   Modifier le fichier settings.py pour configurer ta base de données (PostgreSQL, MySQL, SQLite...).

5. Appliquer les migrations
   python manage.py migrate

6. Lancer le serveur
   python manage.py runserver

7. Tester l'API
   Par défaut, le serveur tourne sur http://127.0.0.1:8000
   Utiliser Postman ou un navigateur pour tester les endpoints.


Notes

- Assure-toi d'activer ton environnement virtuel avant d’installer les dépendances ou de lancer le serveur.
- Les fichiers PDF générés sont sauvegardés dans le dossier media/rapports.
- Pour toute question, consulte la documentation Django officielle : https://docs.djangoproject.com/

Bonne utilisation !
