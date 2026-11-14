# Vérifications du kit · 14 novembre 2026

Runtime : Python 3.12.9, uv 0.6.3, Node 26.10.0. Vérifications sur les projets extraits, les sources de l’enseignant et le navigateur.

## Publication GitHub · état actuel

Le dépôt public est https://github.com/adrien-may/ecm2026. La branche main contient les supports ; les 33 branches de checkpoints conservent leurs commits. Les PDF et le kit sont distribués dans la release fall-2026. Aucun code applicatif ni historique de checkpoint n’a été réécrit pour cette publication.

Les deux builds passent. La commande GitHub de la slide 8 a été vérifiée dans le navigateur, réexportée et inspectée dans le PDF final. Les 291 titres sont toujours présents, aucun caractère ne sort des pages, et les 44 liens de téléchargement utilisent GitHub et couvrent les 33 checkpoints. Résultats : output/github-publication/pdf-audit.json. Le normaliseur accepte une seconde exécution sur les URLs publiques ; un lien volontairement supprimé dans une copie provoque un refus avant toute modification des deux PDF.

Les instructions distinguent le clone public et le bundle hors ligne. Les fichiers instance/, .env.local et l’ancien bundle Flask sont exclus du dépôt. _reference/ reste inchangé et exclu de la distribution. Les suites applicatives n’ont pas été relancées : le code des projets est identique aux checkpoints déjà vérifiés.

## Backend au-delà du CRUD et conclusion · avant publication GitHub

Le cours principal contient **257 slides**, complétées par **34 slides optionnelles**. Le chapitre 239–252 introduit authentication, authorization, session, jobs, cron, webhook, cache et MCP. Ces exemples de design n’ajoutent aucune fonctionnalité obligatoire aux projets. La discussion sur un test utile précède maintenant la présentation (255) ; « Relier, tester, expliquer » conclut le cours (257).

Les 20 slides modifiées (4 et 239–257) ont été contrôlées dans le navigateur, puis rendues depuis le PDF final et inspectées sur trois planches. Aucun débordement de code ni contenu sous le footer. Deux titres trop longs ont été raccourcis et revérifiés. Captures et mesures : output/backend-topics-review/ ; rendus PDF : output/backend-topics-review/pdf/. L’onglet présentateur sur 3030 n’a pas été déplacé.

Le build principal passe. Les pages modifiées ont été exportées puis assemblées avec les pages inchangées de l’export précédent. Les **291 titres** des deux PDF correspondent aux sources ; aucun caractère ne sort des pages. Les **36 liens** du PDF principal et les **8 liens** du support optionnel couvrent les **33 checkpoints**, sur le port 3030. Résultat : output/backend-topics-review/pdf-audit.json. Le kit est assemblé avec ces exports et les guides actualisés.

Les concepts MCP et les appels tools/list et tools/call ont été confrontés à la specification 2026-07-28 ; les notions de session et d’authorization aux recommandations OWASP. Sources et limites pédagogiques : docs/backend-capabilities.md. Aucun code applicatif ni checkpoint n’a changé lors de cet ajout : les suites des projets n’ont pas été relancées. _reference/ reste inchangé.

## Réorganisation du parcours et présentation finale · état précédent (242 slides)

Le cours principal contient 242 slides ; le support optionnel en contient 34. Les 78 slides des jours 2 et 3, les deux slides d’orientation modifiées et les 34 slides optionnelles ont été contrôlées dans le navigateur : aucun débordement de code, image manquante ou contenu sous le footer. Mesures et captures : output/flow-review/.

Les nouvelles étapes du projet ont été reconstruites depuis les blocs Python des slides dans une copie du starter : 1 passed / 1 failed sur 405, puis 2 passed après l’ajout exact du POST. Aucune modification du code des projets n’était nécessaire ; seuls trois README de checkpoints ont changé. Leurs refs, ZIPs et bundle ont été régénérés.

Les builds des deux supports passent. Les deux PDF contiennent 242 et 34 pages : les 276 titres ont été comparés aux sources, aucun caractère ne sort des pages, et 44 liens couvrent les 33 checkpoints. Les 78 pages des jours 2 et 3 et les 34 pages optionnelles ont été rendues et leurs dix planches inspectées. Résultats : output/flow-review/pdf-audit.json et output/flow-review/pdf/. Le contrôle d’export a également refusé un PDF optionnel privé de son lien SQLModel, avant de remplacer le PDF principal. Le kit est assemblé avec ces deux exports et les archives actualisées.

## Projets et checkpoints

| Projet final | Résultat |
| --- | --- |
| Introduction Flask | 8 tests |
| Todo Flask avec Flask-smorest | 35 tests |
| Todo FastAPI avec SQLModel | 25 tests |
| Starter FastAPI | 14 tests ; exercice volontairement rouge |
| Client todo React | 4 tests et build |
| Canvas complet et Three.js | 10 tests et build chacun |
| Scores NestJS | 4 tests HTTP et build TypeScript |
| Jeu de référence | 11 tests backend, 14 frontend et build |
| Starter du jeu | 1 test backend, 14 frontend et build |

La dernière vérification complète, avant la réorganisation des parcours, passe avec **33 checkpoints** via npm run verify:checkpoints. Les installations sont faites en dossiers temporaires ; le bundle expose les branches et la reprise par worktree conserve le travail initial.

La régression du template donne **1 passed** pour la comparaison, **1 passed** pour le signal et **2 failed** pour les prénoms. La fixture et le test affichés correspondent au code distribué. Le projet enseignant Flask d’introduction correspond au checkpoint 08.

Les parcours reconstruits depuis les extraits vérifient :

- POST Flask : 9 tests verts, nouveau test rouge, puis 10, 18 et 20 verts ; correspondance des helpers et de la route avec le checkpoint 10.
- SQLite : test de redémarrage rouge, 31 tests HTTP verts, puis 32 avec persistence.
- Marshmallow et Blueprint : mêmes 33 tests verts après CORS ; AST des fichiers reconstruits identiques aux checkpoints 13, 15 et 16.
- Flask-smorest : deux tests de documentation rouges avant le nouveau endpoint, puis 35 verts ; correspondance avec le checkpoint 17.
- SQLModel : 25 tests avant et après, mêmes assertions, fichiers reconstruits identiques au checkpoint 03. Une database créée avec SQLAlchemy est lue et modifiée avec SQLModel sans reconstruire sa table.

## Navigateur et visuels

La version précédente de **262 slides** a été contrôlée : aucun code ne déborde horizontalement, aucune image manquante et aucun contenu sous le début du footer. Mesures et captures : output/pedagogy-review/. Deux slides SQLModel trop denses ont été corrigées puis revérifiées. Les visuels modifiés ont été rechargés avec de nouveaux noms pour éviter le cache d’images de Slidev en développement.

Swagger UI du checkpoint Flask 17 affiche les cinq opérations. Le POST exécuté avec {"title":"Lire la documentation"} renvoie 201 avec les champs attendus. La capture OpenAPI provient de cette API locale.

Les quatre captures Canvas montrent dessin, animation, déplacement jusqu’au bord et tirs. L’exercice Three.js a été exécuté dans une copie isolée : la perspective change le rendu, et les dix tests restent verts. Les deux captures de caméra illustrent cette comparaison.

Les vérifications antérieures du client React (Flask puis FastAPI), du trajet jeu/score (FastAPI puis NestJS), des erreurs réseau et de la reprise du jeu restent documentées par output/full-browser-review/. Le contrat et les tests correspondants sont conservés. L’onglet du présentateur n’a pas été déplacé.

## PDF et distribution

L’export utilise --per-slide, car l’export global avait produit des pages vides ou « Loading slide… ». scripts/fix_pdf_links.py refuse ces états. Depuis la publication GitHub, il normalise les liens de téléchargement vers le dépôt public ; les comptes rendus ci-dessous décrivent les anciens exports locaux.

Le précédent export, conservé dans le compte rendu historique, contenait **262 pages**, les **262 titres attendus** et **43 liens de téléchargement** couvrant les **33 checkpoints**, sur le port 3030. Aucun caractère ne sort de la page. Toutes les pages ont été rendues et les sept planches inspectées. Deux titres 3D, le nombre de tests du checkpoint POST et le lien OpenAPI ont été réexportés séparément, intégrés et contrôlés à nouveau. Résultats : output/pedagogy-pdf-review/audit.json. Le contrôle d’export refuse désormais un PDF auquel manque un lien de checkpoint ; il a été vérifié sur le PDF incomplet puis sur sa correction. Ce résultat appartient à la vérification précédente.

Le kit contient sources, guides, briefs, contrats, lockfiles, archives, bundle et PDF. Il exclut node_modules, .venv, databases de développement et _reference/.

## Limites

Une deprecation warning AnyIO/Starlette peut accompagner les tests FastAPI sans les faire échouer. Les premiers téléchargements de packages et de Swagger UI nécessitent Internet ou un cache préparé. La specification OpenAPI est locale. Le score du jeu reste déclaré par le client ; il ne prouve pas une partie réelle.

Le jour 1 complet prend 425 minutes hors pauses ; la variante 375 minutes est explicitée dans COURSE_PLAN.md. La démo 3D enseigne le rendu et sa séparation des règles, pas les collisions en 3D.
