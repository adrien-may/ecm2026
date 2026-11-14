# Checkpoints du cours

Chaque ZIP contient un projet complet et son lockfile. Les noms de branches ouvrent leur code sur [GitHub](https://github.com/adrien-may/ecm2026). Les branches sont aussi réunies dans le [bundle du cours](slides/public/checkpoints/ecm26-course.bundle). Voir [le guide de reprise](docs/environment.md).

| Branche | Projet complet |
| --- | --- |
| [`flask-00-ready`](https://github.com/adrien-may/ecm2026/tree/flask-00-ready) | [ZIP](slides/public/checkpoints/00-ready.zip) |
| [`flask-01-flask`](https://github.com/adrien-may/ecm2026/tree/flask-01-flask) | [ZIP](slides/public/checkpoints/01-flask.zip) |
| [`flask-02-pytest`](https://github.com/adrien-may/ecm2026/tree/flask-02-pytest) | [ZIP](slides/public/checkpoints/02-pytest.zip) |
| [`flask-03-route`](https://github.com/adrien-may/ecm2026/tree/flask-03-route) | [ZIP](slides/public/checkpoints/03-route.zip) |
| [`flask-04-template`](https://github.com/adrien-may/ecm2026/tree/flask-04-template) | [ZIP](slides/public/checkpoints/04-template.zip) |
| [`flask-05-name`](https://github.com/adrien-may/ecm2026/tree/flask-05-name) | [ZIP](slides/public/checkpoints/05-name.zip) |
| [`flask-06-fixtures`](https://github.com/adrien-may/ecm2026/tree/flask-06-fixtures) | [ZIP](slides/public/checkpoints/06-fixtures.zip) |
| [`flask-07-test-quality`](https://github.com/adrien-may/ecm2026/tree/flask-07-test-quality) | [ZIP](slides/public/checkpoints/07-test-quality.zip) |
| [`flask-08-json`](https://github.com/adrien-may/ecm2026/tree/flask-08-json) | [ZIP](slides/public/checkpoints/08-json.zip) |
| [`flask-09-list`](https://github.com/adrien-may/ecm2026/tree/flask-09-list) | [ZIP](slides/public/checkpoints/09-list.zip) |
| [`flask-10-create`](https://github.com/adrien-may/ecm2026/tree/flask-10-create) | [ZIP](slides/public/checkpoints/10-create.zip) |
| [`flask-11-crud`](https://github.com/adrien-may/ecm2026/tree/flask-11-crud) | [ZIP](slides/public/checkpoints/11-crud.zip) |
| [`flask-12-package`](https://github.com/adrien-may/ecm2026/tree/flask-12-package) | [ZIP](slides/public/checkpoints/12-package.zip) |
| [`flask-13-sqlite`](https://github.com/adrien-may/ecm2026/tree/flask-13-sqlite) | [ZIP](slides/public/checkpoints/13-sqlite.zip) |
| [`flask-14-cors`](https://github.com/adrien-may/ecm2026/tree/flask-14-cors) | [ZIP](slides/public/checkpoints/14-cors.zip) |
| [`flask-15-marshmallow`](https://github.com/adrien-may/ecm2026/tree/flask-15-marshmallow) | [ZIP](slides/public/checkpoints/15-marshmallow.zip) |
| [`flask-16-blueprint`](https://github.com/adrien-may/ecm2026/tree/flask-16-blueprint) | [ZIP](slides/public/checkpoints/16-blueprint.zip) |
| [`flask-17-openapi`](https://github.com/adrien-may/ecm2026/tree/flask-17-openapi) | [ZIP](slides/public/checkpoints/17-openapi.zip) |
| [`fastapi-00-app`](https://github.com/adrien-may/ecm2026/tree/fastapi-00-app) | [ZIP](slides/public/checkpoints/fastapi-00-app.zip) |
| [`fastapi-01-create`](https://github.com/adrien-may/ecm2026/tree/fastapi-01-create) | [ZIP](slides/public/checkpoints/fastapi-01-create.zip) |
| [`fastapi-02-crud`](https://github.com/adrien-may/ecm2026/tree/fastapi-02-crud) | [ZIP](slides/public/checkpoints/fastapi-02-crud.zip) |
| [`fastapi-03-sqlmodel`](https://github.com/adrien-may/ecm2026/tree/fastapi-03-sqlmodel) | [ZIP](slides/public/checkpoints/fastapi-03-sqlmodel.zip) |
| [`canvas-01-draw`](https://github.com/adrien-may/ecm2026/tree/canvas-01-draw) | [ZIP](slides/public/checkpoints/canvas-01-draw.zip) |
| [`canvas-02-animation`](https://github.com/adrien-may/ecm2026/tree/canvas-02-animation) | [ZIP](slides/public/checkpoints/canvas-02-animation.zip) |
| [`canvas-03-input`](https://github.com/adrien-may/ecm2026/tree/canvas-03-input) | [ZIP](slides/public/checkpoints/canvas-03-input.zip) |
| [`canvas-04-game`](https://github.com/adrien-may/ecm2026/tree/canvas-04-game) | [ZIP](slides/public/checkpoints/canvas-04-game.zip) |
| [`nest-00-app`](https://github.com/adrien-may/ecm2026/tree/nest-00-app) | [ZIP](slides/public/checkpoints/nest-00-app.zip) |
| [`nest-01-memory`](https://github.com/adrien-may/ecm2026/tree/nest-01-memory) | [ZIP](slides/public/checkpoints/nest-01-memory.zip) |
| [`nest-02-sqlite`](https://github.com/adrien-may/ecm2026/tree/nest-02-sqlite) | [ZIP](slides/public/checkpoints/nest-02-sqlite.zip) |
| [`todo-client`](https://github.com/adrien-may/ecm2026/tree/todo-client) | [ZIP](slides/public/checkpoints/todo-client.zip) |
| [`game-starter`](https://github.com/adrien-may/ecm2026/tree/game-starter) | [ZIP](slides/public/checkpoints/game-starter.zip) |
| [`game-reference`](https://github.com/adrien-may/ecm2026/tree/game-reference) | [ZIP](slides/public/checkpoints/game-reference.zip) |
| [`canvas-05-three`](https://github.com/adrien-may/ecm2026/tree/canvas-05-three) | [ZIP](slides/public/checkpoints/three-demo.zip) |

Les familles Flask, FastAPI, Canvas et NestJS suivent chacune une progression. Les branches game-starter et game-reference sont deux états explicitement différents du projet. La démo Three.js reste optionnelle.

## Vérifier les archives

```sh
npm run verify:checkpoints
```

Cette commande utilise uv et npm pour installer dans des dossiers temporaires, lancer les tests, vérifier les étapes rouges et cloner le bundle. Aucun checkout du dépôt enseignant ni donnée de développement ne sont remplacés.
