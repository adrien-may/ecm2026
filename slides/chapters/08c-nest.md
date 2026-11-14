# Option NestJS · Le même contrat en TypeScript

Nous gardons `POST /scores/` et `GET /scores/`.

TypeScript ajoute des annotations à JavaScript.

NestJS organise controller, service et module.

Prérequis : le trajet du jeu fonctionne déjà avec FastAPI.

Le stockage est fourni. Nous remplaçons seulement le backend.

<!--
Option séparée du parcours commun. Partir de game-reference ou du projet complété, pas du starter sans POST. 3 min. Ne pas installer un générateur global ni proposer tout un catalogue de framework. Ouvrir nest-00-app téléchargé pour un setup vérifiable.
-->

---

# 00 · Lancer le petit projet fourni

**Extraire <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-00-app.zip" download>nest-00-app (.zip)</a> dans un nouveau dossier**, puis ouvrir le terminal dans ce dossier.

```sh
npm ci
npm test
npm run dev
```

Ouvrir `http://127.0.0.1:8002/health`.

Le setup contient NestJS, TypeScript et la configuration des decorators.

Aucun `__init__.py` : ce projet est en TypeScript.

<!--
4 min. Node26.10.0 est le runtime répété. npm run build compile en JavaScript dans dist. Le code TypeScript est dans src ; node ne lit pas ces decorators NestJS sans la compilation prévue.
-->

---

# 00 · Deux decorators, deux rôles

**Ouvrir le fichier fourni** `src/app.ts` : repérer `HealthController`.

```typescript
@Controller('health')
class HealthController {
  @Get()
  health() { return {status: 'ok'}; }
}
```

`@Controller` définit le path commun de la classe.

`@Get` expose cette méthode pour une request GET.

<!--
4 min. Imports depuis @nestjs/common. Faire reconstruire l’URL /health avec le groupe. Comparer @app.get de Flask et cette décomposition sans prétendre que tous les decorators font la même chose.
-->

---

# 00 · Le module déclare les composants

**Dans le même fichier** `src/app.ts`, lire `AppModule`, sous le controller.

```typescript
@Module({controllers: [HealthController]})
class AppModule {}
```

`NestFactory.create(AppModule)` construit l’application.

Un module NestJS n’est pas automatiquement un microservice.

Nous lançons toujours **un seul backend**.

<!--
3 min. Lire app.ts et main.ts du premier checkpoint. Ne pas expliquer toute la dependency injection avant d’avoir un service à fournir.
-->

---

# nest-00-app · Checkpoint

```sh
npm test
```

**1 test passe ; GET /health renvoie le JSON attendu.**

Branche `nest-00-app` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-00-app.zip" download>Projet complet (.zip)</a>

Comparer les fichiers et le résultat avant de poursuivre.

<!--
Faire une pause de synchronisation. Le ZIP contient le projet entier. Extraire dans un nouveau dossier si nécessaire ; conserver le travail personnel.
-->

---

# 01 · Ouvrir les fichiers du backend de scores

**Extraire <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-01-memory.zip" download>nest-01-memory (.zip)</a> dans un nouveau dossier**. Les nouveaux fichiers sont déjà fournis :

```text
src/
├── app.ts              ← module et construction de l'app
├── main.ts             ← démarrage du serveur
├── score.controller.ts ← routes HTTP
├── score.service.ts    ← service
├── score.dto.ts        ← validation du body
└── score.store.ts      ← stockage en mémoire
```

Ouvrir ces fichiers existants ; les slides suivantes indiquent lequel lire ou modifier.

---

# 01 · Un service fourni au controller

**Ouvrir** `src/score.service.ts` : lire la classe `ScoresService`.

```typescript
@Injectable()
export class ScoresService {
  constructor(private readonly store: ScoreStore) {}
  list() { return this.store.list(); }
}
```

Nest construit le service et lui fournit son stockage.

Le controller reçoit à son tour `ScoresService` dans son constructeur.

<!--
4 min. Lire private readonly comme un attribut du constructeur TypeScript. Montrer le tableau providers du module. Ce petit service est mince ; reconnaître son coût, et son intérêt lorsque les règles du domaine grandissent.
-->

---

# 01 · POST reçoit un body

**Ouvrir** `src/score.controller.ts` : lire `create()` dans `ScoresController`.

```typescript
@Post()
create(@Body() data: CreateScoreDto) {
  return this.scores.create(data);
}
```

`@Post` expose la méthode. `@Body` choisit l’entrée de la méthode.

`CreateScoreDto` doit être une classe disponible à l’exécution.

Le POST renvoie `201` par défaut dans NestJS.

<!--
4 min. Imports Body et Post depuis @nestjs/common. Faire écrire le test round trip avant d’ajouter cette méthode. TypeScript number seul ne vérifie pas le JSON reçu.
-->

---

# 01 · Installer les outils de validation

Ces packages sont déclarés dans le `package.json` fourni. Commande d’ajout :

```sh
npm install class-validator@0.14.3 class-transformer@0.5.1
```

**Modifier** `src/score.dto.ts` : tester les règles de `points` une par une.

```typescript
@IsInt()
@Min(0)
@Max(90)
points!: number;
```

Tester successivement `1.5`, `-1`, puis `91`.

<!--
5 min. Le point d’exclamation est une déclaration d’initialisation TypeScript, pas une validation. Chaque decorator a sa règle. Le fichier complet valide et nettoie aussi player ; lire IsString, Length et Transform après ce besoin, sans tous les réciter au départ.
-->

---

# 01 · Le pipe exécute les contraintes

**Ouvrir** `src/app.ts` : lire la configuration dans `createApplication()`, avant son `return`.

```typescript
app.useGlobalPipes(new ValidationPipe({
  transform: true,
  whitelist: true,
  forbidNonWhitelisted: true,
}));
```

Le DTO devient une instance validée ; les champs inconnus sont refusés.

Une entrée invalide renvoie `400` et ne crée aucun score.

<!--
4 min. Importer ValidationPipe depuis @nestjs/common. transform ne signifie pas activer une conversion implicite de toutes les strings en numbers. Vérifier que "60" est refusé dans les tests du cours. Relier à la frontière Pydantic étudiée le matin.
-->

---

# nest-01-memory · Checkpoint

```sh
npm test
```

**3 tests passent ; les scores disparaissent au redémarrage.**

Branche `nest-01-memory` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-01-memory.zip" download>Projet complet (.zip)</a>

Comparer les fichiers et le résultat avant de poursuivre.

<!--
Faire une pause de synchronisation. Le ZIP contient le projet entier. Extraire dans un nouveau dossier si nécessaire ; conserver le travail personnel.
-->

---

# 02 · Ajouter le stockage fourni

**Extraire <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-02-sqlite.zip" download>nest-02-sqlite (.zip)</a> à part. Ouvrir le fichier fourni `src/score.store.ts`** et comparer avec la version mémoire. Extrait :

```typescript
database.prepare(
  'INSERT INTO score (player, points, created_at) VALUES (?, ?, ?)'
).run(player, points, new Date().toISOString());
```

Le SQLite intégré à Node évite d’apprendre un nouvel ORM ici.

Les `?` lient les données séparément du SQL.

<!--
5 min. Ouvrir la classe complète. Le path est injecté pour remplacer le fichier en test ; on ferme la connexion à l’arrêt du module. Une instruction SQLite est atomique et autocommit ici ; plusieurs écritures liées demanderaient une transaction explicite. Le SQL n’est pas construit en concaténant le pseudo.
-->

---

# 02 · Tester ce que la mémoire ne pouvait pas faire

**Ouvrir le fichier fourni** `tests/scores.test.cjs` : lire le test de persistance.

Créer un score, fermer l’application, la recréer sur le même fichier.

Relire le classement et retrouver le score.

Les autres tests continuent d’utiliser **un fichier temporaire neuf**.

Une assertion sur `service.create()` seule ne prouve pas ce trajet HTTP et database.

<!--
5 min. Lire tests/scores.test.cjs. Les tests utilisent le runner Node déjà rencontré avec Canvas, et un port libre. Rien n’est écrit dans instance/nest-scores.sqlite pendant ces tests.
-->

---

# nest-02-sqlite · Checkpoint

```sh
npm test
npm run dev
```

**4 tests passent ; le classement survit au redémarrage.**

Branche `nest-02-sqlite` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/nest-02-sqlite.zip" download>Projet complet (.zip)</a>

Comparer les fichiers et le résultat avant de poursuivre.

<!--
Faire une pause de synchronisation. Le ZIP contient le projet entier. Extraire dans un nouveau dossier si nécessaire ; conserver le travail personnel.
-->

---

# 02 · Brancher le même jeu

**Créer le fichier** `game-starter/frontend/.env.local`, à côté de `package.json`, puis écrire :

```text
VITE_API_URL=http://127.0.0.1:8002
```

Si `.env.local` existe déjà, modifier cette ligne. Redémarrer Vite depuis `frontend/`.

Même interface, autre backend, **autre fichier de données**.

Modifier ensuite une règle et son test pour expliquer votre changement.

<!--
5 min. CORS autorise les origins5175. La référence Python reste sur8001. Pour l’exercice de modification, changer le nombre de scores affichés puis son attente de test, ou ajouter une vraie donnée avec sa validation ; ne pas attribuer des points pour un changement purement cosmétique.
-->
