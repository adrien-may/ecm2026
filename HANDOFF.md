# Reprise du cours ECM 2026

Mis à jour le 17 novembre 2026. Le parcours principal comporte **259 slides**, complétées par **30 slides optionnelles**. Les 33 checkpoints sont conservés. Dépôt public : https://github.com/adrien-may/ecm2026. Les PDF de 259 et 30 pages sont vérifiés : 289 titres et 43 liens de téléchargement GitHub couvrant les 33 checkpoints. Le kit contient ces exports et les sources actualisées. La 3D revient dans le parcours commun en deux slides ; voir docs/verification.md.

## Dernières corrections locales

Le déplacement de la slide GitHub a été annulé à la demande de l’enseignant. Elle reste en slide 8, uv en 10 et la création du projet en 11. Le clone utilise ecm26-flask-ssr-reprise/ pour rester cohérent avec le projet ecm26-flask-ssr/ tout en gardant un dossier distinct. Cette correction locale n’a pas été publiée : le dernier push a échoué car Git n’a pas pu obtenir les credentials GitHub. La release publique reste fall-2026-r4.

La transition « Notre backend fonctionne · Quelle suite ? » a été supprimée. La slide 110 ouvre directement l’expérience de serialization manuelle. Le bilan reste à la fin du jour 1. Le PDF et le kit locaux suivent cette séquence.

## Repères de relecture

- **3** : tour de table sans durée individuelle.
- **10–12** : installer uv selon son OS, contrôler les fichiers du projet, puis vérifier l’import de Flask.
- **42–48** : template_rendered, fixture de capture, cleanup et garanties distinctes des tests.
- **91 et 93** : session SQLAlchemy, select, scalars et all avant le GET.
- **110–164** : serialization manuelle, Marshmallow, Blueprint, Flask-smorest et OpenAPI.
- **165–166** : destination du jour 2 et ses trois résultats observables.
- **167–186** : todo FastAPI avec SQLAlchemy, puis reprise à 25 tests.
- **187–211** : passage de la todo au jeu, Canvas et montage React.
- **212–213** : ouverture 3D de cinq minutes, captures du même instant et démo avec slider de caméra.
- **214–227** : projet et intégration du classement, avec fichiers précis, test rouge puis POST, formulaire et point de synchronisation.
- **233–236** : hexagonal architecture, ports/adapters, dependency inversion et clean architecture.
- **239** : CQRS = Command Query Responsibility Segregation.
- **241–254** : au-delà du CRUD : authentication/authorization, session, jobs/cron, webhooks, cache et MCP. Exemples de conception, pas de fonctionnalités ajoutées aux starters.
- **257–259** : préparer une explication de test, présenter son projet, puis conclure sur « Relier, tester, expliquer ». La discussion sur les tests n’est plus la dernière slide. Aucune grille chiffrée ni durée individuelle.

Jour 1 : 1–164. Jour 2 : 165–227. Jour 3 : 228–259. Le cours reste sur http://localhost:3030. L’onglet présentateur n’a pas été déplacé.

## Les options sont un support séparé

Lancer npm run slides:options -- --port 3032. Dans slides/options.md : orientation (1), SQLModel (2–15), NestJS (16–30).

Le parcours commun conserve FastAPI + SQLAlchemy jusqu’au jeu. SQLModel propose model_validate et sqlmodel_update ; NestJS remplace un backend de scores déjà compris. Aucun de ces ateliers ne doit interrompre l’intégration commune.

## Projets et reprise

CHECKPOINTS.md indexe les 33 branches et ZIPs, sur GitHub. Les sources du cours sont sur main ; les autres branches contiennent les projets. Les PDF et le kit sont distribués dans la release fall-2026-r4 : https://github.com/adrien-may/ecm2026/releases/tag/fall-2026-r4. La slide 8 et docs/environment.md expliquent le clone GitHub et la reprise par branche. Les projets sont dans lessons/, projects/ et workshops/. Les README de game-starter, fastapi-03-sqlmodel et nest-02-sqlite ont été synchronisés avec la séparation des parcours ; leur code est inchangé.

Attention : lessons/03-fastapi-todo contient le résultat optionnel SQLModel. Pour suivre le parcours commun, extraire fastapi-02-crud. Les deux versions ont 25 tests.

Introduction Flask : 8 tests ; todo Flask : 35 ; client React : 4 ; Canvas/Three.js : 10 chacun ; NestJS final : 4 ; jeu de référence : 11 backend et 14 frontend.

Le nouveau test montré dans le projet échoue bien sur 405 avant le POST (1 passed, 1 failed), puis passe avec la route affichée (2 passed). Le starter distribué reste volontairement incomplet. Les markers __init__.py et les opérations de fichiers restent visibles.

## Temps et limites

Jour 2 : 375 minutes, dont 35 d’intégration guidée et 100 de réalisation personnelle. Les cinq minutes de 3D sont incluses ; la revue finale passe de 20 à 15 minutes. SQLModel (30 minutes) et NestJS (60) sont hors de ce parcours. Jour 3 : 50 minutes d’architecture puis 30 de découverte backend. Les 145 minutes de réalisation sont préservées ; 115 minutes de présentations collectives et 5 de conclusion complètent le planning, sans durée individuelle imposée.

Le jour 1 intégralement saisi représente toujours 425 minutes hors pauses. COURSE_PLAN.md décrit une variante 375 minutes avec reprise de certains changements SQLite et Blueprint depuis les checkpoints. Ce point n’est pas masqué par le nombre de slides.

L’enseignant précisera les modalités institutionnelles et la remise avant diffusion. Aucun blocage technique connu.

## Vérifier et distribuer

npm run slides:build et npm run slides:build:options produisent les deux sites statiques. npm run slides:export produit les deux PDF et vérifie pages et liens de téléchargement. python3 scripts/package_course.py assemble le kit avec les PDF, les sources et les checkpoints.

Revue de la réorganisation : output/flow-review/. Nouveau chapitre et conclusion : output/backend-topics-review/. Les vérifications complètes précédentes des projets restent dans docs/verification.md. Seule la démo Three.js change : slider de caméra et controls visibles à côté du jeu. Les règles et les tests du jeu sont conservés.

_reference/ et le Google Slides original restent inchangés. Les refs étudiants sont séparées du checkout enseignant. Les supports et les 33 branches de checkpoints sont publiés avec les archives actualisées. Les anciennes instructions de bundle ont été remplacées par la reprise GitHub.

Publication : les liens de téléchargement utilisent GitHub, y compris dans les PDF. Les databases de développement dans instance/ et _reference/ sont exclus du dépôt et du kit.

GitHub est le point d’entrée Git du cours. Aucun lien .bundle dans les supports courants ; le kit ne contient plus ce format. Les ZIPs restent disponibles en secours.
