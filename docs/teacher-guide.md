# Conduite des trois jours

Les slides sont le fil conducteur d'une séance de code, pas un texte à lire d'une traite. Les presenter notes indiquent les pauses, les questions et les fichiers complets à ouvrir. Les durées visent 375 minutes utiles par jour, avec 45 minutes de marge et pauses courtes hors déjeuner.

Avant chaque bloc de code, faire repérer l'action visible dans la slide : créer un dossier, créer un fichier, modifier un fichier existant, déplacer ou ouvrir un fichier fourni. Montrer le path dans l'explorateur et laisser le groupe s'y placer. Présenter d'abord le comportement à construire et sa raison, puis proposer le nom de la fonction. Lors d'un passage à un starter fourni, annoncer le nouveau dossier de travail et les fichiers déjà présents.

## Jour 1

Consacrer la matinée à construire Flask progressivement. Installer Flask, puis pytest, et distinguer chaque decorator. Préserver le SSR et l'expérience du test comparant le même template : il vérifie une cohérence, mais ne détecte pas certaines régressions du besoin. Faire prédire avant de casser le prénom.

L'après-midi relie JSON au client connu : CRUD en mémoire, refactor isolé vers le package `todo`, puis ORM, persistance et React. La séquence SQLite montre les blocs complets : modèle, configuration, commande, cinq routes, fixtures et test de redémarrage. Faire observer le test rouge avant le refactor ; utiliser le ZIP pour comparaison ou reprise. Vérifier l'emplacement du marker en demandant aux étudiants de le désigner dans leur propre arbre.

Finir le jour 1 par deux refactors : `flask-15-marshmallow` puis `flask-16-blueprint`. Les 33 tests du checkpoint CORS ne changent pas. Distinguer le parse JSON de `load()` (deserialize et validate), de `dump()` (serialize, sans validation de sortie), puis de l’écriture SQLAlchemy. Présenter `@pre_load` avant `@validates_schema`. `fields.Boolean` peut convertir des valeurs que notre contrat refuse : le hook strict est donc nécessaire.

Le Blueprint natif regroupe le CRUD dans `todo/tasks.py` et la factory l’enregistre avec `app.register_blueprint()`. Déclarer un Blueprint ne suffit pas pour rendre ses routes accessibles. `schemas.py` et `tasks.py` sont deux nouveaux fichiers au même niveau que `models.py`, sans nouveaux dossiers ni nouveaux markers. Poursuivre avec `flask-17-openapi` : installer Flask-smorest, introduire `@response`, puis `@arguments`, et ouvrir `/openapi/swagger`. Les 33 tests précédents restent verts ; deux tests documentent le nouveau besoin. `SQLAlchemyAutoSchema` reste seulement une piste de recherche.

Les 375 minutes visées dans COURSE_PLAN.md préservent la matinée Flask/SSR/pytest. Les blocs CRUD, React et bilan ont été resserrés pour les deux refactors ; le rythme réel reste à ajuster au groupe. Ne pas présenter le nombre de slides comme une mesure de durée.

## Jour 2

Ouvrir par la démonstration du jeu de référence et la carte des trois étapes : todo FastAPI, jeu Canvas, score persistant. Le backend reste FastAPI avec SQLAlchemy pendant toute la journée.

Le bloc de 105 minutes inclut la découverte de FastAPI et l’exercice todo. Prévoir ensuite 15 minutes de débrief et reprise au checkpoint fastapi-02-crud (25 tests). Montrer ce qui se transpose de POST/GET tasks à POST/GET scores.

Canvas occupe 90 minutes, montage React compris. Avant de passer au projet, faire observer une fin de partie et son score. Garder le dossier game-starter extrait à cette étape.

Après Canvas, consacrer cinq minutes aux deux slides 3D (212–213). Préparer la démo avant la séance, mettre le jeu en pause et déplacer le slider Point de vue. Les deux captures montrent le même instant. Éviter les paramètres de caméra et le code de rendu : l’objectif est de voir une autre représentation du jeu. Revenir explicitement à game-starter/ pour le score.

Consacrer 35 minutes à l’intégration guidée : repérer backend/ et frontend/, lancer les deux terminaux, écrire le test POST puis GET, constater 405, ajouter la route, puis construire le formulaire et les états de sauvegarde. La référence complète a 11 tests backend et 14 frontend ; le seul test ajouté au starter en donne 2 côté backend.

Protéger 100 minutes de réalisation personnelle puis 15 minutes de revue. Limiter le projet à une mécanique et une ressource stockée.

SQLModel et NestJS sont dans slides/options.md, ouverts avec npm run slides:options -- --port 3032. Ils sont indépendants, hors du budget commun. Le refactor SQLModel (30 minutes) conserve model_validate et sqlmodel_update ; NestJS remplace le backend connu (60 minutes). Ne pas les intercaler avant que l’intégration fonctionne.

## Jour 3

Prévoir 50 minutes d’architecture sur le même score : modules, layers, ports/adapters, clean architecture, services, events et CQRS. Expliquer le sens des dépendances, pas une recette de dossiers. Notre starter n’est pas présenté comme une implémentation hexa ou clean.

Après les architectures, prévoir 30 minutes de découverte : authentication/authorization et sessions, jobs/cron, webhooks, cache, puis MCP. Garder le jeu comme cas commun. Les slides décrivent des évolutions possibles, sans nouvelle installation ni fonctionnalité obligatoire. Voir docs/backend-capabilities.md.

Puis 145 minutes de réalisation et 30 de vérification croisée des README. Une plage collective de démonstration et discussion reste prévue dans le planning, sans durée individuelle imposée. La présentation finale ne contient plus de grille chiffrée ; les modalités institutionnelles seront annoncées séparément. La slide qui explique un test utile est placée juste avant pour préparer le passage. Terminer le cours par « Relier, tester, expliquer » : cinq minutes de synthèse sur les acquis, en revenant du frontend au backend. La plage collective de présentation est de 115 minutes dans ce planning, sans quota individuel.

## Checkpoints

Après chaque slide de synchronisation, faire lancer la commande annoncée et regarder le résultat. Les étudiants comparent l'arbre, les imports et les fichiers ; ceux qui reprennent extraient un ZIP dans un nouveau dossier. Le professeur ouvre le même checkpoint que le groupe. Tous les états nommés sont distribués avec code complet et lockfile.

Le bundle contient plusieurs familles de projets ; ne pas passer de Flask à NestJS sans expliquer le nouveau dossier. Un ZIP par projet convient aux personnes moins à l'aise avec Git.

## Arbitrages retenus pour terminer les supports

FastAPI est le parcours commun. Les approfondissements sont séparés. Le gel de livraison précède les démonstrations ; l’enseignant précisera ses modalités avant diffusion. Le brief final conserve les comportements attendus sans barème chiffré ni durée de passage.

La version actuelle du client historique inspecté utilise GET/POST/PATCH/DELETE, pas PUT. Vérifier ce point avec l'enseignant des trois jours frontend avant la séance. Le client de référence du kit permet une répétition indépendante.

Si le temps manque : montrer les captures de la courte ouverture 3D, réduire les effets et menus du jeu, puis limiter le catalogue d’architecture. Garder les tests utiles, le SSR, les checkpoints, la persistance, l'intégration et l'explication individuelle.

La fixture `captured_templates` revient après les fixtures, avec connect/yield/finally/disconnect expliqués. Faire prédire les trois observations après suppression du prénom dans le template : comparaison verte, signal vert, assertions de prénom rouges. Pour la serialization, exécuter d’abord la concaténation volontairement cassée dans un shell, puis json.dumps, avant le schema. Le passage true/True appartient au parse JSON.

La version intégralement saisie du jour 1 représente désormais 425 minutes hors pauses. Voir COURSE_PLAN.md pour la variante 375 minutes avec certains déplacements de code lus et repris depuis un checkpoint. Ne pas masquer les nouveaux fichiers ni accélérer silencieusement les explications de l’introduction.

Les captures Canvas et 3D sont dans le parcours commun. La démo 3D conserve les mêmes règles, sans changement de backend ni de fichier à recopier. SQLModel et NestJS constituent les approfondissements.
