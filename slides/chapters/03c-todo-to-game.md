# De la todo au jeu · Un trajet connu

| Ce que nous savons faire | Ce que le jeu va demander |
| --- | --- |
| POST une task avec un title | POST un score avec player et points |
| GET la liste des tasks | GET le classement |
| Valider puis conserver dans SQLite | Valider puis conserver dans SQLite |

**Maintenant : construire le jeu qui produit ces points.**

Canvas dessine et anime la partie ; React affichera le classement. FastAPI reste notre backend.

<!--
La todo est notre exercice de transfert, le jeu notre application du même trajet. Nous n’allons pas convertir une task en score ni ajouter le jeu au package todo : le starter du jeu sera un projet voisin, annoncé explicitement au montage React.
-->
