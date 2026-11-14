# Évaluation 1 · Remplacer le backend todo

Travail individuel, pendant le bloc FastAPI du jour 2. Point de départ : `fastapi-01-create`, également disponible dans `lessons/03-fastapi-starter`. Le stockage, les schemas de création, GET collection et POST sont fournis. **30 minutes de réalisation, puis 5 minutes de retour** dans la séquence guidée ; le professeur peut prolonger avec le budget de reprise.

## À livrer

- GET `/tasks/{id}`, PATCH partiel et DELETE conformes au contrat du cours.
- Un test d'un parcours réussi, un test de body invalide sans modification, un test d'ID absent.
- Le client React connecté au backend sur le port 8000, avec quatre actions vérifiées.
- Un README court : commandes, résultat des tests, choix expliqué et limite connue.

Commencer par `uv run pytest tests/exercise_contract.py -q`. Ce test fourni doit échouer avant les routes et passer après. Ajouter vos propres cas. Vous pouvez consulter les slides, la documentation et votre code Flask. Les assistants de programmation sont autorisés ; vous restez responsable de comprendre et vérifier chaque changement.

## Barème sur 20

| Critère | Points | Preuve attendue |
| --- | ---: | --- |
| Contrat et CRUD | 6 | Bon ID, status codes, champs conservés, DELETE vide |
| Validation et erreurs | 4 | Entrée invalide refusée sans écriture, ID absent |
| Tests utiles et isolés | 5 | Assertion indépendante du code produit ; database temporaire |
| Client et reproductibilité | 3 | URL configurable, démarrage documenté, interaction complète |
| Explication | 2 | Justifier un test et la différence entre annotation et validation |

Un test qui ne vérifie que `200` reçoit moins de crédit qu'un test qui détecte une modification du mauvais ID. Une sophistication de framework n'apporte pas de points supplémentaires. Un résultat incomplet peut obtenir les points correspondant aux comportements démontrés et expliqués.

Questions possibles : pourquoi `exclude_unset=True` ? Pourquoi un test a-t-il besoin d'une autre database ? Pourquoi `"false"` et `false` ne sont-ils pas équivalents ? Qu'est-ce qui reste identique après le remplacement de Flask ?

À la fin, conserver son état de travail avant de consulter `fastapi-02-crud`. La pondération de cette note avec le projet final suit le règlement communiqué par l'enseignant ; aucun pourcentage non confirmé n'est annoncé ici.
