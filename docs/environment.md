# Préparer et dépanner le poste

Versions réellement utilisées pour construire le kit : **Python 3.12.9**, **uv 0.6.3**, **Node 26.10.0**. Les lockfiles fixent les packages. Utiliser la version Node répétée en classe, même si plusieurs projets acceptent des versions plus anciennes. Aucun compte cloud n'est nécessaire.

Avant le cours : vérifier `git --version`, `uv --version`, `node --version`, `npm --version`, puis `uv python install 3.12`. Télécharger le bundle et les ZIPs pendant que le réseau fonctionne. Installer les dépendances d'un checkpoint de chaque écosystème avant la séance si le réseau de l'école est incertain. Les ZIPs contiennent le code et les lockfiles, **pas les caches de packages** ; un premier install hors ligne n'est pas garanti.

## Python

Après extraction d'un checkpoint, se placer dans le dossier où se trouve `pyproject.toml`, puis `uv sync --locked` et `uv run pytest -q`. Le premier checkpoint sans tests demande seulement `uv run python --version`.

Pour un nouveau projet : `uv init --bare --python 3.12`, puis `uv python pin 3.12`. Ne pas mélanger `pip` global, un ancien virtualenv et `uv run`. Les packages arrivent avec `uv add`, les outils de test avec `uv add --dev`.

| Symptôme | Vérifier |
| --- | --- |
| `No module named todo` | Être au niveau de `pyproject.toml`, avec `todo/__init__.py` juste dessous |
| `attempted relative import` | Utiliser `python -m todo.init_db`, pas le fichier directement |
| pytest collecte zéro test | Fichiers `tests/test_*.py`, fonctions `test_*`, bon dossier |
| Import de test incohérent | `tests/__init__.py` directement à côté de `conftest.py` |
| `no such table` | Exécuter la commande `init-db` du README du checkpoint |
| Changement de colonne absent | `create_all()` n'est pas une migration |

Les markers sont nommés `__init__.py` : deux underscores avant et après `init`, puis `.py`. Ni `__init__py`, ni `_init_.py`, ni `.py.txt`. Un dossier d'images, de templates, `instance/` ou `frontend/` ne reçoit pas ce fichier. Nous utilisons des packages Python classiques ; les namespace packages sans marker sont hors parcours.

## Ports et URLs

| Application | Port |
| --- | ---: |
| Slides | 3030 |
| Todo React | 5173 |
| Canvas / 3D | 5174 / 5176 |
| Jeu React | 5175 |
| Flask todo | 5001 |
| FastAPI todo | 8000 |
| Scores Python / NestJS | 8001 / 8002 |

Le port 5001 évite le conflit fréquent de 5000 avec AirPlay sur macOS. Un port déjà pris : retrouver le terminal de ce projet et arrêter avec Ctrl-C ; ne pas tuer un processus inconnu. Les serveurs Vite utilisent `--strictPort` pour éviter un changement silencieux qui casserait CORS.

## Frontend et CORS

`npm ci` puis `npm run dev`. Les variables `VITE_*` sont lues au démarrage de Vite. Copier `.env.example` en `.env.local` est une méthode commune aux systèmes. Sous PowerShell, `$env:VITE_API_URL="http://localhost:8000"` remplace le préfixe de commande utilisé sous macOS/Linux.

`localhost` et `127.0.0.1` ne sont pas la même origin. Comparer URL, port, method, headers et body dans Network. CORS est appliqué par le navigateur ; curl ne le vérifie pas. `fetch` doit vérifier `response.ok`, et ne pas parser un body vide de `204`.

## Reprendre sans perdre son travail

Extraire le ZIP du checkpoint dans **un nouveau dossier** est la solution la plus directe. Depuis le dépôt public :

```sh
git clone -b flask-00-ready https://github.com/adrien-may/ecm2026.git mon-backend
cd mon-backend
git branch -r
git worktree add ../reprise origin/flask-13-sqlite
```

Hors ligne, télécharger `ecm26-course.bundle` à l’avance et remplacer l’URL du clone par ce fichier. Aucun compte GitHub n’est nécessaire pour lire le dépôt public. La branche `main` contient les supports, `flask-00-ready` le premier projet.

Les branches correspondent à des projets indépendants ou à des étapes, pas toutes au même dossier de travail. Lire le README après un changement de branche. Conserver les modifications locales avant toute reprise ; aucun `reset --hard` n'est nécessaire.
