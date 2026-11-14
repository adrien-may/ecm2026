# ECM 2026 · Trois jours de backend et web

**257 slides de cours et 34 slides d’approfondissement**, une progression de code guidée, **33 checkpoints complets**, deux évaluations et des projets exécutables. Les explications sont en français ; les termes techniques restent en anglais. `_reference/` est conservé sans modification.

## Ouvrir le cours

```sh
git clone https://github.com/adrien-may/ecm2026.git
cd ecm2026
npm ci
npm run slides -- --port 3030
```

Présentation : [localhost:3030](http://localhost:3030). Les notes du présentateur expliquent les pauses de code, les questions et les transitions. Le [PDF du cours](https://github.com/adrien-may/ecm2026/releases/download/fall-2026/ecm26-three-days.pdf) fournit une version hors ligne ; les démos restent des applications séparées.

```sh
npm run slides:build
npm run slides:build:options
npm run slides:export
```

Les liens de téléchargement des slides et des PDF pointent vers le dépôt public GitHub. Hors ligne, ouvrir `CHECKPOINTS.md` et les ZIPs du kit téléchargé à l’avance.

Pour les ateliers optionnels : **npm run slides:options -- --port 3032**. Le [PDF des approfondissements](https://github.com/adrien-may/ecm2026/releases/download/fall-2026/ecm26-options.pdf) conserve SQLModel, le rendu 3D et NestJS. L’export produit les deux PDF ; leurs liens couvrent les 33 checkpoints.

Le build optionnel est dans slides/dist-options/. Le build principal est dans `slides/dist/`. Le PDF est exporté dans `output/ecm26-three-days.pdf`. L’export slide par slide prend quelques minutes et vérifie que les pages ont fini de charger.

## Le parcours

| Jour | Slides | Fil conducteur | Code |
| --- | --- | --- | --- |
| 1 | 1–164 | Flask installé progressivement, SSR, pytest, decorators, tests utiles, CRUD, SQLite, React, Marshmallow, Blueprint, OpenAPI | [Introduction](lessons/01-flask-ssr/README.md), [todo Flask](lessons/02-flask-todo/README.md), [React](projects/todo-client/README.md) |
| 2 | 165–225 | Todo FastAPI → jeu Canvas → classement avec le même backend | [FastAPI avec SQLAlchemy](slides/public/checkpoints/fastapi-02-crud.zip), [Canvas](workshops/canvas/README.md) |
| 3 | 226–257 | Architecture, authentication, jobs/cron, webhooks, cache, MCP, projet et synthèse | [Starter](projects/game-starter/README.md), [référence](projects/game-reference/README.md), [brief final](assessments/02-game.md) |

Le jour 2 commence par la cible du projet, puis suit trois résultats observables. FastAPI + SQLAlchemy reste le backend commun jusqu’au classement. Les options [SQLModel](lessons/03-fastapi-todo/README.md), [Three.js](workshops/three-demo/README.md) et [NestJS](lessons/04-nest-scores/README.md) sont dans un support séparé ; elles n’interrompent plus l’intégration.

Après les architectures, les slides 239–252 présentent d’autres responsabilités du backend à partir du même classement. Ce survol ne rajoute pas de fonctionnalités au projet. Les [repères du chapitre](docs/backend-capabilities.md) précisent les distinctions et les sources. Le cours se termine par une synthèse des acquis ; la discussion sur les tests prépare la présentation.

Les outils sont introduits au moment du besoin. Les tests passent de la construction de l'app au comportement HTTP, puis aux entrées invalides, à la persistance et aux règles du jeu. Le cours conserve la comparaison entre le test qui utilise le même template et celui qui exprime le besoin du visiteur.

## Reprendre exactement le même code

[Catalogue des 33 checkpoints](CHECKPOINTS.md) · [Bundle Git](slides/public/checkpoints/ecm26-course.bundle) · [Kit complet](https://github.com/adrien-may/ecm2026/releases/download/fall-2026/ecm26-course-kit.zip)

```sh
git clone -b flask-00-ready https://github.com/adrien-may/ecm2026.git mon-backend
cd mon-backend
git branch -r
```

La branche `main` contient les supports. Les 33 autres branches contiennent les projets à chaque étape. Hors ligne, remplacer l’URL du clone par le fichier `ecm26-course.bundle` téléchargé à l’avance.

Chaque slide de synchronisation lie un ZIP complet et indique une branche et le résultat attendu. Pour reprendre sans écraser son travail, extraire dans un nouveau dossier ou utiliser un worktree depuis une branche `origin/...`. Le [guide d'environnement](docs/environment.md) donne les commandes et les cas de panne courants.

Les emplacements de `__init__.py` sont montrés explicitement : d'abord `tests/__init__.py`, ensuite `todo/__init__.py`, puis `backend/scores/__init__.py`. Les slides distinguent package classique, convention de tests et dossiers qui n'ont pas de marker.

## Préparer la séance et évaluer

- [Guide enseignant](docs/teacher-guide.md) et [timing détaillé](COURSE_PLAN.md).
- [Contrat todo](contracts/todo.md) à conserver entre Flask et FastAPI.
- [Évaluation todo](assessments/01-todo.md), starter [FastAPI](lessons/03-fastapi-starter/README.md).
- [Projet final et présentation](assessments/02-game.md), [starter](projects/game-starter/README.md), [référence complète](projects/game-reference/README.md).
- [État de livraison et reprise](HANDOFF.md), [vérifications](docs/verification.md).

Le parcours commun utilise FastAPI ; NestJS reste une option séparée. La présentation finale demande de montrer le trajet, un test et un choix expliqué, sans grille chiffrée ni durée individuelle. Les modalités institutionnelles et l’heure de remise seront annoncées par l’enseignant.

## Vérification technique

Versions répétées : Python 3.12.9, uv 0.6.3, Node 26.10.0. Les projets possèdent leurs lockfiles et leurs propres commandes de test. `npm run verify:checkpoints` vérifie les archives dans des dossiers temporaires, les étapes rouges, la régression du template et la récupération depuis le bundle.

Le projet final accepte des scores déclarés par le client. Sa validation n'est pas un mécanisme anti-cheat ; cette limite fait partie de la leçon. Aucun service distant ni déploiement public n'est requis.
