# Au-delà du CRUD · Repères enseignant

Les slides 239–252 prolongent les architectures avec les besoins possibles du même jeu. Compter 30 minutes, discussion comprise. Aucun nouveau package, fichier applicatif ou service n’est demandé. Le server MCP, le webhook et les jobs décrits sont des exemples de conception.

| Slides | Besoin | Distinction à faire entendre |
| --- | --- | --- |
| 240–241 | Reconnaître une personne et contrôler ses actions | Authentication ≠ authorization ; le champ player du body ne prouve pas une identité |
| 242–244 | Calculer un rapport en dehors d’une request | Acceptation ≠ réussite ; cron choisit le moment, le worker exécute |
| 245 | Recevoir un event d’un service | Webhook ≠ polling ; il reste une request HTTP |
| 246–247 | Éviter de recalculer le même classement | Cache ≠ source de vérité ; TTL ≠ cohérence immédiate |
| 248–251 | Permettre à un assistant de lire le classement | MCP expose des capacités ; le backend conserve ses règles et ses permissions |
| 252 | Choisir une évolution et sa preuve | Nommer le besoin avant de choisir un outil |

## Authentication et session

La suppression d’un score personnel est hypothétique : le projet actuel n’a pas cette route ni de comptes. Une personne connectée n’a pas pour autant le droit de modifier les données des autres.

La session illustrée est conservée côté serveur ; le cookie ne contient qu’un identifiant opaque. D’autres architectures utilisent des cookies signés ou des tokens, mais ce survol n’en fait pas une recette de login. Mentionner un provider OpenID Connect si la question du SSO vient du groupe. Ne pas assimiler JWT à un contenu chiffré, OAuth à un mécanisme de login complet, ou CORS à un contrôle des permissions.

Sources : [OWASP Authorization Cheat Sheet](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authorization_Cheat_Sheet.md), [Session Management Cheat Sheet](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Session_Management_Cheat_Sheet.md). Principes consultés via Context7 le 14 novembre 2026.

## Jobs, cron, webhooks et cache

Un job durable demande une prise en charge persistante, un état observable et une stratégie de reprise. La déclaration async def ne fournit pas ces garanties. Cron peut lancer directement une commande ou déclencher une queue ; une queue n’est pas imposée pour tout travail périodique.

L’expression cron du support comporte cinq champs. Son exemple à 02:00 suppose explicitement une timezone UTC. Discuter du cas où la machine est éteinte ou où un run précédent est encore actif : ne pas promettre un rattrapage automatique commun à tous les schedulers.

Le rapport quotidien illustre une opération idempotente : deux exécutions pour une même date ne créent pas deux rapports. Une contrainte unique et une transaction protègent mieux qu’un simple test d’existence avant écriture.

Un webhook inverse l’initiative par rapport au polling : le service externe envoie un POST quand l’event survient. Dans le cas proposé, vérifier la signature et le body, accepter durablement l’event avant de répondre 2xx, puis confier le traitement au worker. Les retries et doublons imposent une stratégie par event ID. Les règles de signature, de replay et d’ordre dépendent du provider ; sa documentation est la référence pour une implémentation. Il n’y a aucun nouveau endpoint à lancer dans ce kit et aucun développement sur RPC.

Le cache-aside du Top 10 permet de parler de hit/miss et de Time To Live sans introduire Redis. Le POST confirmé peut invalider l’entrée. Cette séquence pédagogique ne résout pas toutes les races entre lecteurs et writers : demander quelle fraîcheur est acceptable. Pour les données privées, la clé et les contrôles d’accès doivent tenir compte de l’utilisateur et des changements de droits.

## MCP

**Model Context Protocol** standardise les échanges entre une application IA et des servers exposant des tools, resources ou prompts. Le host héberge un client MCP ; un modèle peut proposer un appel et le host en contrôle l’exécution.

Le tool proposé, get_leaderboard, lit notre GET /scores/. Il n’existe pas déjà dans le starter. Les méthodes tools/list et tools/call expliquent découverte et invocation ; le tableau n’est pas une reproduction complète des messages du protocole. Il n’y a pas de nouvelle démo ou de server MCP à lancer dans le kit.

MCP peut utiliser stdio localement ou Streamable HTTP à distance. Un tool peut exécuter du code et avoir des effets : les droits, la validation des entrées, le consentement et la confiance accordée aux résultats restent des sujets explicites. Une annotation read-only n’est pas une permission. Le contenu d’un pseudo retourné par l’API ne devient pas une instruction pour le host.

Sources vérifiées contre la specification **2026-07-28** :

- [Overview et principes de contrôle](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/2026-07-28/docs/specification/2026-07-28/index.mdx)
- [Tools et security considerations](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/2026-07-28/docs/specification/2026-07-28/server/tools.mdx)
- [Transport stdio](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/2026-07-28/docs/specification/2026-07-28/basic/transports/stdio.mdx)
- [Transport Streamable HTTP](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/2026-07-28/docs/specification/2026-07-28/basic/transports/streamable-http.mdx)

## Revenir à une vraie conclusion

La slide 255 prépare une explication de test avant la présentation du projet. Elle ne conclut plus le cours.

La slide 257, « Relier, tester, expliquer », revient sur le trajet interface → backend → données, les preuves apportées par les tests, et les choix que chaque étudiant peut expliquer. Elle clôt les acquis sans annoncer un nouvel outil ni un nouvel exercice.
