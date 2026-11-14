---
theme: default
title: ECM - Fall 26 / WEB 101
info: |
  Trois jours : Flask, SSR, tests utiles, API persistante, FastAPI, Canvas et projet avec classement persistant.
layout: cover
colorSchema: light
aspectRatio: 16/9
fonts:
  sans: Arial
  mono: Menlo
  local: Arial,Menlo
drawings:
  persist: false
---

<div class="eyebrow">Centrale Méditerranée · Novembre 2026</div>

# Web 101

Backend et applications web

<!--
Ouverture de la première matinée backend après les trois jours de frontend.
Environ trois heures avec les pauses de synchronisation, à adapter au diagnostic du groupe.
Chaque outil apparaît au moment où il devient utile ; le code complet est disponible aux checkpoints.
-->

---

# whoami

<div class="speaker-intro">
<div>

<h2>Adrien Brunet</h2>

Co-founder & CTO chez **may**

[may.app](https://may.app)

Promo sortante **2013**

</div>
<div class="speaker-links">

### Contact

[adrien@may-sante.com](mailto:adrien@may-sante.com)

[brunet.adrien@gmail.com](mailto:brunet.adrien@gmail.com)

### Code et parcours

GitHub : [adrienbrunet](https://github.com/adrienbrunet) / [adrien-may](https://github.com/adrien-may)

LinkedIn : [adrienbrunet](https://www.linkedin.com/in/adrienbrunet)

</div>
</div>

<!--
2 min. Présenter son parcours depuis la promo 2013, son rôle chez may et le lien entre le cours et la construction d'une application au quotidien.
Source des informations biographiques : slide 2 du support de l'enseignant, https://docs.google.com/presentation/d/18zrTpdve2sIDFO0LlsQsUEsND7sDr9xka69duHYLBsY/edit.
-->

---

# Et vous ?

**Tour de table**

Votre prénom et une envie pour votre stage ou la suite de l'école.

### Après trois jours de frontend

- Qu'avez-vous appris ou réussi à construire ?
- Qu'avez-vous aimé ? Moins aimé ou trouvé difficile ?
- Qu'aimeriez-vous comprendre côté backend ?

<!--
Prévoir 10 à 15 min selon la taille du groupe, en partageant le temps de l'introduction et du diagnostic. Noter les acquis, les difficultés et les attentes pour ajuster les premières pauses de code. Une réponse concrète suffit, sans chercher le vocabulaire parfait.
Adapté de la slide 3 du support de l'enseignant, https://docs.google.com/presentation/d/18zrTpdve2sIDFO0LlsQsUEsND7sDr9xka69duHYLBsY/edit.
-->

---

# Le fil conducteur des trois jours

**Jour 1 · Comprendre** : construire Flask, produire du HTML puis du JSON, tester et conserver les données.

**Jour 2 · Relier** : transférer la todo vers FastAPI, puis construire un jeu et son classement avec ce même backend.

**Jour 3 · Terminer** : choisir une organisation, découvrir d’autres responsabilités du backend, puis vérifier et expliquer son projet.

À chaque étape : **un besoin, un test, du code, un checkpoint de reprise**.

<!--
3 min. Présenter le trajet complet avant le premier outil. Les étudiants connaissent déjà React : nous allons construire ce qui répond à ses requests, puis réutiliser ce trajet pour une autre interface. Le jeu n'est pas une rupture de sujet : son résultat a besoin des mêmes mécanismes HTTP, validation, persistance et tests. Indiquer où se situent les deux évaluations.
-->

---
src: ./chapters/01-flask.md
---

---
src: ./chapters/02-todo.md
---

---
src: ./chapters/02b-flask-structure.md
---

---
src: ./chapters/02c-openapi.md
---

---
src: ./chapters/03-day-two.md
---

---
src: ./chapters/03-fastapi.md
---

---
src: ./chapters/03c-todo-to-game.md
---

---
src: ./chapters/04-canvas.md
---

---
src: ./chapters/05-game-project.md
---

---
src: ./chapters/05b-day-two-close.md
---

---
src: ./chapters/06-architecture.md
---

---
src: ./chapters/06b-backend-capabilities.md
---

---
src: ./chapters/07-delivery.md
---
