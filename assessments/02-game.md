# Projet final · Un petit jeu relié à un backend

Travail individuel. Construire un trajet complet pendant les jours 2 et 3 avant d’élargir le périmètre. Partir de `game-starter`, du Canvas guidé ou d'un projet aussi petit. La référence « Six cibles » indique la finition attendue.

## Socle attendu

1. Une interaction jouable, un objectif compréhensible, une fin et un restart.
2. Une ressource utile enregistrée par le backend : score, partie, niveau ou progression.
3. Une écriture et une lecture visibles dans l'interface, avec chargement, succès et erreur.
4. Une persistance vérifiée après redémarrage du backend.
5. Une validation côté backend, des erreurs cohérentes et des tests utiles avec des données isolées.
6. Une modification personnelle limitée du starter, que vous pouvez expliquer.

Backend du parcours commun : **FastAPI + SQLAlchemy**. Le support d’approfondissements propose NestJS comme remplacement optionnel une fois le trajet complet terminé. Ne pas multiplier les frameworks. Les comptes, le cache, les jobs, les webhooks, un server MCP, le multiplayer, la 3D et le déploiement public ne sont pas nécessaires. Les nouveaux sujets du jour 3 servent à discuter des besoins possibles.

Commencer par un seul trajet : fin de partie → POST → database → GET → classement. Éviter les menus, assets ou effets tant que ce trajet ne fonctionne pas.

## Livrables

- Sources et lockfiles, sans `.venv/`, `node_modules/`, secrets ou database personnelle.
- README avec versions, commandes, URL, controls, tests et une limite connue.
- Un schéma du trajet complet et une décision d'architecture justifiée.
- Trois preuves de test au minimum : succès observable, entrée invalide, persistance ou règle métier importante.
- Une démonstration du trajet complet, avec un test, un choix expliqué et une limite.

Ouvrir le jeu, les fichiers utiles et le test choisi avant son passage. Montrer ce qui fonctionne et expliquer ce qui reste incomplet. Aucune durée individuelle ni grille chiffrée n’est fixée dans ce support.

Les assistants sont autorisés. Indiquer brièvement ce qu’ils ont aidé à produire et comment vous l’avez vérifié. La compréhension et les preuves portent sur votre code.

## Livraison prévue

Le parcours de référence prévoit un gel des sources avant les démonstrations du jour 3. Garder une archive ou un commit identifiable. L'enseignant communiquera l'heure exacte et les règles institutionnelles avant le début de l'évaluation.

Si une livraison après le cours est retenue, le passage du jour 3 devient formatif : montrer l'état réel, les limites et un plan de fin. Une date et une modalité de démonstration finale doivent alors être communiquées à toute la classe avant de noter. Les modalités sont annoncées avant l’évaluation.

Questions possibles : le serveur peut-il croire votre score ? Quel test attrape une vraie panne ? Que se passe-t-il si le backend s'arrête ? Où serait `__init__.py` si vous ajoutiez un sous-package Python ? Pourquoi votre application n'a-t-elle pas besoin de microservices ?
