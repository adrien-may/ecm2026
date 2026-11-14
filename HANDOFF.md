# Reprise du cours ECM 2026

Mis à jour le 14 novembre 2026. Le parcours principal comporte **257 slides**, complétées par **34 slides optionnelles**. Les 33 checkpoints sont conservés. Dépôt public : https://github.com/adrien-may/ecm2026. Les PDF de 257 et 34 pages sont vérifiés : 291 titres et 44 liens GitHub couvrant les 33 checkpoints. Le kit contient ces exports et les sources actualisées. Le contenu du support optionnel reste inchangé ; voir docs/verification.md.

## Repères de relecture

- **3** : tour de table sans durée individuelle.
- **41–47** : template_rendered, fixture de capture, cleanup et garanties distinctes des tests.
- **90 et 92** : session SQLAlchemy, select, scalars et all avant le GET.
- **110–164** : serialization manuelle, Marshmallow, Blueprint, Flask-smorest et OpenAPI.
- **165–166** : destination du jour 2 et ses trois résultats observables.
- **167–186** : todo FastAPI avec SQLAlchemy, puis reprise à 25 tests.
- **187–211** : passage de la todo au jeu, Canvas et montage React.
- **212–225** : projet et intégration du classement, avec fichiers précis, test rouge puis POST, formulaire et point de synchronisation.
- **231–234** : hexagonal architecture, ports/adapters, dependency inversion et clean architecture.
- **237** : CQRS = Command Query Responsibility Segregation.
- **239–252** : au-delà du CRUD : authentication/authorization, session, jobs/cron, webhooks, cache et MCP. Exemples de conception, pas de fonctionnalités ajoutées aux starters.
- **255–257** : préparer une explication de test, présenter son projet, puis conclure sur « Relier, tester, expliquer ». La discussion sur les tests n’est plus la dernière slide. Aucune grille chiffrée ni durée individuelle.

Jour 1 : 1–164. Jour 2 : 165–225. Jour 3 : 226–257. Le cours reste sur http://localhost:3030. L’onglet présentateur n’a pas été déplacé.

## Les options sont un support séparé

Lancer npm run slides:options -- --port 3032. Dans slides/options.md : orientation (1), SQLModel (2–15), rendu 3D/2.5D (16–19), NestJS (20–34).

Le parcours commun conserve FastAPI + SQLAlchemy jusqu’au jeu. SQLModel propose model_validate et sqlmodel_update ; le rendu 3D compare deux caméras avec la même simulation 2D ; NestJS remplace un backend de scores déjà compris. Aucun de ces ateliers ne doit interrompre l’intégration commune.

## Projets et reprise

CHECKPOINTS.md indexe les 33 branches et ZIPs, avec le bundle Git. Les sources du cours sont sur main ; les autres branches contiennent les projets. Les PDF et le kit sont distribués dans la release fall-2026 : https://github.com/adrien-may/ecm2026/releases/tag/fall-2026. La slide 8 et docs/environment.md expliquent le clone public et la reprise hors ligne. Les projets sont dans lessons/, projects/ et workshops/. Les README de game-starter, fastapi-03-sqlmodel et nest-02-sqlite ont été synchronisés avec la séparation des parcours ; leur code est inchangé.

Attention : lessons/03-fastapi-todo contient le résultat optionnel SQLModel. Pour suivre le parcours commun, extraire fastapi-02-crud. Les deux versions ont 25 tests.

Introduction Flask : 8 tests ; todo Flask : 35 ; client React : 4 ; Canvas/Three.js : 10 chacun ; NestJS final : 4 ; jeu de référence : 11 backend et 14 frontend.

Le nouveau test montré dans le projet échoue bien sur 405 avant le POST (1 passed, 1 failed), puis passe avec la route affichée (2 passed). Le starter distribué reste volontairement incomplet. Les markers __init__.py et les opérations de fichiers restent visibles.

## Temps et limites

Jour 2 : 375 minutes, dont 35 d’intégration guidée et 100 de réalisation personnelle. SQLModel (30 minutes), 3D (10–15) et NestJS (60) sont hors de ce parcours. Jour 3 : 50 minutes d’architecture puis 30 de découverte backend. Les 145 minutes de réalisation sont préservées ; 115 minutes de présentations collectives et 5 de conclusion complètent le planning, sans durée individuelle imposée.

Le jour 1 intégralement saisi représente toujours 425 minutes hors pauses. COURSE_PLAN.md décrit une variante 375 minutes avec reprise de certains changements SQLite et Blueprint depuis les checkpoints. Ce point n’est pas masqué par le nombre de slides.

L’enseignant précisera les modalités institutionnelles et la remise avant diffusion. Aucun blocage technique connu.

## Vérifier et distribuer

npm run slides:build et npm run slides:build:options produisent les deux sites statiques. npm run slides:export produit les deux PDF et vérifie pages et liens de téléchargement. python3 scripts/package_course.py assemble le kit avec les PDF, les sources et les checkpoints.

Revue de la réorganisation : output/flow-review/. Nouveau chapitre et conclusion : output/backend-topics-review/. Les vérifications complètes précédentes des projets restent dans docs/verification.md. Aucun code de projet n’a changé lors de cette réorganisation.

_reference/ et le Google Slides original restent inchangés. Les refs étudiants sont séparées du checkout enseignant ; HEAD et staging sont conservés. Aucun push ni publication distante.

Publication : les liens de téléchargement utilisent GitHub, y compris dans les PDF. Les databases de développement dans instance/ et _reference/ sont exclus du dépôt et du kit.
