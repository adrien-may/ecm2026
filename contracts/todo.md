# Le contrat HTTP de la todo API

Ce contrat suit les appels du client React du cours précédent. Flask et FastAPI doivent satisfaire les mêmes besoins. Le dossier `projects/todo-client` fournit un client de référence indépendant des anciens outils de build.

| Request | Succès |
| --- | --- |
| `GET /tasks/` | `200`, array, ordre croissant des IDs |
| `POST /tasks/` avec `{"title":"Lire"}` | `201`, nouvelle task |
| `GET /tasks/{id}` | `200`, une task |
| `PATCH /tasks/{id}` avec `title` et/ou `done` | `200`, task modifiée |
| `DELETE /tasks/{id}` | `204`, body vide |

Une task contient exactement `id` (integer généré par le backend), `title` (string), `done` (boolean) et `creation_date` (string ISO 8601, UTC). Exemple :

```json
{"id":1,"title":"Lire","done":false,"creation_date":"2026-11-14T10:00:00+00:00"}
```

- `title` est nettoyé avec `strip()`, puis doit contenir de 1 à 255 caractères. Les titres identiques sont permis.
- À la création, seul `title` est accepté. Le backend choisit les autres valeurs ; `done` vaut `false`.
- PATCH accepte un objet non vide contenant seulement `title` et/ou `done`. Un champ omis ne change pas. `null`, `0` et `"false"` ne sont pas des booleans.
- Une request invalide ne modifie aucune task. Validation : `400` sous Flask, `422` sous FastAPI ; un mauvais Content-Type peut produire `415`. Les erreurs sont du JSON, mais leur structure dépend du framework.
- Un ID absent donne `404`. Utiliser un ID existant pour tester la validation d'un PATCH : l'ordre validation/recherche peut différer entre frameworks.
- La collection finit par `/`, une ressource individuelle n'en a pas. Utiliser ces URL canoniques : ne pas dépendre des redirects.
- PUT n'est pas utilisé par le client inspecté. Un remplacement complet et un PATCH partiel ont des sémantiques différentes.
- La version du cours ne fournit ni comptes, ni pagination. Chaque backend possède son propre fichier SQLite ; changer de backend peut afficher une liste vide.

Les tests doivent vérifier les données observables, pas reproduire la fonction qui les fabrique. Une response `200` ne prouve ni la persistance, ni la bonne modification de la task demandée.
