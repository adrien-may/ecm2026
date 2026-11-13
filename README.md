# Jour 2 · NestJS en une heure guidée

Objectif : suivre une request validée depuis un controller jusqu'à un service puis un stockage fourni. Le jeu et le contrat `/scores/` sont déjà connus. Nous ne découvrons pas en même temps un nouveau jeu, un nouveau langage et un nouvel ORM.

## Lancer le résultat

Node **26.10.0** est la version utilisée pour la répétition du cours. Node 24 est accepté par le projet, mais le kit doit être répété avec la version distribuée à la classe.

```sh
npm ci
npm test
npm run dev
```

Attendu : **4 tests HTTP passent**. Ouvrir `http://127.0.0.1:8002/scores/`. Brancher le jeu React avec `VITE_API_URL=http://127.0.0.1:8002` et redémarrer Vite. `npm run build` puis `npm start` lance le JavaScript compilé.

## Progression de 60 minutes

| Durée | Branche / objectif | Résultat |
| --- | --- | --- |
| 10 min | `nest-00-app`, lire TypeScript, controller, module | `/health`, 1 test |
| 10 min | `@Controller`, puis `@Get`, service injecté | Expliquer GET `/scores/` |
| 15 min | `@Post`, `@Body`, DTO, une contrainte à la fois | Rejeter un score invalide |
| 10 min | `nest-01-memory`, test de round trip | 3 tests ; redémarrage perd les scores |
| 10 min | `nest-02-sqlite`, stockage fourni | 4 tests ; redémarrage conserve les scores |
| 5 min | Modifier un test puis le comportement, connecter React | Expliquer une régression détectée |

Le premier checkpoint n'installe pas `class-validator` ni `class-transformer`. Les ajouter quand le DTO devient nécessaire : `npm install class-validator@0.14.3 class-transformer@0.5.1`.

## Lire dans cet ordre

1. `src/main.ts` lance l'application sur un port. `app.ts` relie les classes dans `@Module`.
2. `score.controller.ts` déclare le path avec `@Controller('scores')`, puis GET et POST. `@Body()` demande le body.
3. `score.dto.ts` exprime les contraintes avec des decorators exécutés par `ValidationPipe`. `points: number` seul ne valide pas le JSON à l'exécution. `@IsInt`, `@Min(0)`, `@Max(90)` sont trois règles différentes.
4. `score.service.ts` est fourni à Nest par `@Injectable`. Le constructeur reçoit son stockage ; le controller ne le construit pas avec `new`.
5. `score.store.ts` utilise le SQLite intégré à Node. Les paramètres `?` séparent le SQL des données. Un INSERT seul est validé automatiquement par SQLite ; une opération composée demanderait une transaction explicite.

Le stockage et la configuration TypeScript sont fournis. La ligne `DATABASE_PATH` rend le fichier remplaçable pour les tests. Le fichier de développement est `instance/nest-scores.sqlite`. Les tests lancent une application sur un port libre et une database temporaire, puis ferment l'application.

Il n'y a **aucun `__init__.py`** dans ce projet TypeScript. Un module NestJS regroupe des composants ; ce n'est ni un package Python ni un microservice automatiquement.

Le contrat et les limites de confiance sont les mêmes que pour `projects/game-reference`. La validation renvoie `400`. Le serveur accepte un score déclaré, sans vérifier une partie. Le service est volontairement petit : cette couche a un coût et ne devient utile que si des règles doivent y vivre.
