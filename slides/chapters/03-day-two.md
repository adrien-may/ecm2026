# Jour 2 · Du clic au score sauvegardé

Ce soir, nous voulons **jouer, enregistrer un score et relire le classement**.

Le trajet reste celui du jour 1 :

**Interface → request → validation → SQLite → response.**

D’abord avec la todo connue, puis avec une partie de jeu.

Nous gardons **FastAPI + SQLAlchemy** jusqu’à la fin du projet commun.

<!--
10 min avec la slide suivante. Montrer game-reference avant les installations : jouer, sauvegarder, recharger. Le projet donne une destination à toute la journée. Le support optionnel reste fermé pendant le parcours commun.
-->

---

# Trois étapes, trois résultats observables

| Étape | Pourquoi ? | Nous sommes prêts quand… |
| --- | --- | --- |
| Todo avec FastAPI | Transférer le contrat connu | Le même client React fonctionne |
| Jeu avec Canvas | Produire un résultat à conserver | Une partie finit avec un score |
| Classement avec FastAPI | Relier interface et persistance | Le score revient après redémarrage |

SQLModel, 3D et NestJS sont disponibles dans le **support d’approfondissements**, à ouvrir séparément.

<!--
Les options sont des parcours complets conservés pour prolonger le cours. Elles ne sont ni des étapes requises ni du contenu à intercaler avant que le trajet commun fonctionne. Protéger le temps d’intégration et de réalisation.
-->
