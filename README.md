# PerceCmpressorVideo


Ce projet est une application Django permettant de compresser des vidéos en utilisant `ffmpeg`. Elle permet de télécharger des vidéos, de les compresser en arrière-plan et de suivre la progression de la compression.

## Fonctionnalités

- Télécharger des vidéos.
- Compresser des vidéos en utilisant `ffmpeg`.
- Suivre la progression de la compression.
- Afficher une liste des vidéos téléchargées et compressées.
- Visionner les vidéos compressées.

## Prérequis

- Python 3.9 ou supérieur
- Django 3.2 ou supérieur
- ffmpeg

## Installation

1. Clonez le dépôt:

    ```bash
    git clone https://github.com/Kabasele754/PerceCmpressorVideo.git
    cd PerceCmpressorVideo
    ```

2. Créez et activez un environnement virtuel:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances:

    ```bash
    pip install -r requirements.txt
    ```

4. Assurez-vous que `ffmpeg` est installé sur votre système et accessible via le PATH. Vous pouvez télécharger `ffmpeg` depuis [ffmpeg.org](https://ffmpeg.org/download.html).

5. Appliquez les migrations de la base de données:

    ```bash
    python manage.py migrate
    ```

6. Créez un superutilisateur pour accéder à l'admin Django:

    ```bash
    python manage.py createsuperuser
    ```

7. Lancez le serveur de développement:

    ```bash
    python manage.py runserver
    ```

8. Accédez à l'application via `http://localhost:8000`.

## Utilisation

1. Accédez à `http://localhost:8000/upload/` pour télécharger une vidéo.
2. Suivez la progression de la compression via l'interface utilisateur.
3. Consultez la liste des vidéos compressées à `http://localhost:8000/videos/`.

## Structure du Projet

