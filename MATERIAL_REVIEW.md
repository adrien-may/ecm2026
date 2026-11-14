# Review of the existing ECM materials

Reviewed 13 November 2026. Source inspection and planning only; runtime behaviour has not been verified.

## Scope and evidence

Read the full text of the 66-page PDF at `/Users/adrienbrunet/Downloads/WEB - ECM 11_2026.pdf` and visually reviewed all pages as rendered contact sheets. Google Slides was provided as the editable source; the live deck was not inspected or changed.

Inspected the five public repository landing pages and selected raw source files. For `ecm2025`, inspected `first_app`, `first_crud` and `front_ready` files. The PDF names additional checkpoints; their full contents were not audited. Full GitHub branch enumeration was blocked by automatic approval review. Accessible public raw source pages provided a narrower, read-only review route. No repository tests were run.

Context7 CLI could not run under the shell permission policy. Framework-specific claims below were checked against official documentation through the web tool.

## Slide changes, mapped to the PDF

| Existing pages | Recommendation |
| --- | --- |
| 1–3 | Keep introduction and discussion. Update the cover to reflect backend, games and architecture. Use the introductions as a quick experience diagnostic. |
| 4–6 | Rewrite the three-day programme and prerequisite checklist. Reconcile the prior-course instructor/content references and the Python version mismatch. |
| 7–10 | Keep backend motivation, HTTP, JSON and rendering comparison. Use the same todo example in HTML and JSON. Clarify that SSR is current and can coexist with browser-side rendering. |
| 11 | Keep the discussion/video as an optional prompt if it serves the rendering comparison; do not let it replace the concrete example. |
| 12–16 | Keep Flask, setup and request routing. Make setup reproducible, and use a real route response as the first meaningful test. |
| 17–18 | Keep decorators and route tests. Show the equivalence between decorator syntax and registering/wrapping a function without turning this into a general decorator course. |
| 19 | Replace obsolete `FLASK_ENV` instructions with a tested current development command. Clearly distinguish development server and production hosting. |
| 20–21 | Keep the routing diagram. Condense duplicate explanation; move full `url_map` output to a live demonstration if useful. |
| 22–26 | Keep request/response basics and enough context explanation to understand the code. Remove `before_first_request`, correct the teardown callback signature, and avoid a catalogue of hooks. |
| 27–30 | Keep Jinja, SSR and the weak/useful test discussion. Use one small template. Preserve slide 30's critical question and add a deliberate regression demonstration. |
| 31–35 | Keep pytest fixtures and dependency injection as teaching priorities. Replace 100%-coverage-as-default with discussion of what coverage does and does not establish. Correct pseudocode on slide 33, including the JavaScript-style comment. |
| 36 | Retain template_rendered capture after fixtures, as requested. Compare its template/context guarantee with independent HTML assertions during the same regression. |
| 37–38 | Keep the checkpoint discussion. Reduce the CSS framework catalogue to an optional resource, since students already completed frontend teaching. |
| 39–40 | Keep JSON API introduction and manual request tools. Connect them to the todo contract and to automated tests. |
| 41–44 | Keep persistence and ORM explanation. Use current docs, an explicit database path and a rehearsed schema workflow. Show a simple underlying table/query concept. |
| 45–46 | Replace factory and session machinery with a small temporary-database fixture. Keep the lesson on repeatable, independent tests. |
| 47–48 | Keep a brief discussion of response shape, then replace database destruction and migration deletion advice with safe test isolation. |
| 49–50 | Keep the distinction between stored models, JSON representations and input validation. Reduce extension setup where it obscures the concept. |
| 51–52 | Split dense CRUD listings into small behaviour/test/implementation steps. Cover invalid input, 404s, partial updates and transaction failure handling. |
| 53–54 | Keep API docs and CORS, but teach what an origin is and why CORS is not authentication. Connect to the existing frontend immediately. |
| 55–58 | Replace the repeat React build and Storybook installation with integration/debugging of the frontend students already have. Keep Storybook as optional reference. |
| 59 | Existing illustration/interlude: keep only if it has a clear teaching purpose. |
| 60 | Move deployment to an optional demonstration. The slide uses `build`, while the inspected Vite repo deploys `dist`. GitHub Pages hosts the static frontend, not the Python/Nest backend. |
| 61–62 | Replace the old day-2 evaluation brief/interlude with two explicit assessments, a minimum reference result and a rubric. |
| 63–66 | Keep careers, outcomes and feedback. Make outcomes observable and add the new architecture discussion before the conclusion. |

Visual observations: the branding and diagrams are reusable. Code-heavy pages 41, 46, 51 and 52 are particularly dense at presentation size. Page 23's final paragraph reaches the footer area. Preserve the existing identity while moving full code into linked checkpoints and showing a smaller excerpt per slide.

## Repository findings

### `ecm2025`

The checkpoint approach is worth preserving. The default branch only exposes a minimal README, so the new default branch needs a clear course map.

Priority corrections:

- **Development data at risk:** `front_ready/create_app()` selects `data.sqlite`, the test fixture uses that same factory, and fixture teardown calls `drop_all()`. Supply test configuration before initialising the database. [Application](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/app.py), [fixtures](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/conftest.py).
- **Failure handling:** CRUD catches broad exceptions and returns 400 without explicitly rolling back failed commits in those handlers. Narrow expected failures, roll back where needed, and preserve unexpected errors for diagnosis. [Views](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/tasks/views.py).
- **Contract clarity:** list is an array, create uses `title`, PUT changes title, PATCH changes `done`. Document this before porting. Do not silently change the shape expected by students' clients. [Views](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/tasks/views.py).
- **Unnecessary domain constraint:** task titles are unique. Decide whether the course actually wants that rule. [Model](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/tasks/models.py).
- **Environment mismatch:** the final branch requires Python 3.12+, while slide 5 says 3.10+. The development tooling list is broad for a beginner workshop. [Dependencies](https://raw.githubusercontent.com/adrien-may/ecm2025/front_ready/pyproject.toml).

### `react-todo`

Keep this as a reference integration client, not another mandatory frontend rebuild. The API location is hardcoded. Most read/update/delete operations do not check `response.ok`; a failed deletion can still remove the item locally. Make the base URL configurable and preserve visible state on failed mutations. [Hooks](https://raw.githubusercontent.com/adrien-may/react-todo/develop/src/hooks.js).

The README contains a placeholder clone URL. The project already uses Vite and deploys `dist`, unlike slide 60. Verify the existing UI dependencies against their actual component usage during the implementation phase. [README](https://github.com/adrien-may/react-todo), [package configuration](https://raw.githubusercontent.com/adrien-may/react-todo/develop/package.json).

### `scores_fastapi`

This is the clearer starting point for a brief score API explanation: two endpoints and SQLite. Put score constraints on the input schema, bound query limits, add isolated tests and document CORS when connecting a separately served frontend. Use the current lifespan pattern when updating startup code. [Source](https://raw.githubusercontent.com/adrien-may/scores_fastapi/main/main.py).

This API is not a drop-in backend for the inspected game: it returns only score data and lacks the game's `/scores/top/10` endpoint and player/level contract. Choose and document one matching pair.

### `scores_api_ecm25`

Useful as an extension/reference for students who want more: async persistence, player scores and aggregate statistics. It is too much scaffolding to reproduce during the core Flask-to-FastAPI transfer exercise.

Source issues to verify and fix before reuse:

- The startup query executes outside the `try` intended to explain a missing schema, so that query failure bypasses the custom message.
- `db.py` reads the database environment variable during import, before `main.py` calls `load_dotenv()`; values supplied only through `.env` can be missed.
- POST does not explicitly set 201, and the list limit is unbounded.
- The README's PostgreSQL example names the asyncpg driver, while the dependency list supplies psycopg and not asyncpg.

[Application](https://raw.githubusercontent.com/adrien-may/scores_api_ecm25/main/src/main.py), [database setup](https://raw.githubusercontent.com/adrien-may/scores_api_ecm25/main/src/db.py), [dependencies](https://raw.githubusercontent.com/adrien-may/scores_api_ecm25/main/pyproject.toml), [README](https://github.com/adrien-may/scores_api_ecm25).

Do not infer that the repository has no tests: its tree shows a test directory, but the test suite was not inspected successfully or executed.

### `space-invaders-ecm25`

The existing game already includes the ECM enemy pattern and score integration, making it useful as a reference. The inspected main component is 613 lines; derive a smaller sequence of teaching checkpoints rather than presenting the full file at once.

Before using it as the reference implementation, fix or verify the loop: the animation effect has no cancellation cleanup, and pause/resume leaves the previous timestamp untouched, allowing a large catch-up interval. The loop also clones the full game state into React state on every logic step, despite the README's minimal-rerender claim. Focus input handling so entering a player name does not act like game controls.

[Game component](https://raw.githubusercontent.com/adrien-may/space-invaders-ecm25/main/src/ui/SpaceInvaders.tsx), [README](https://github.com/adrien-may/space-invaders-ecm25).

These are source-level findings, not measured performance results or reproduced runtime failures.

## Documentation checks

- Flask removed `FLASK_ENV` and `before_first_request` in 2.3. [Official change history](https://flask.palletsprojects.com/en/stable/changes/).
- Flask documents pytest fixtures and its test client without requiring template-signal capture. [Testing documentation](https://flask.palletsprojects.com/en/stable/testing/).
- FastAPI uses request models for parsing, validation and API documentation. [Request bodies](https://fastapi.tiangolo.com/tutorial/body/).
- FastAPI provides request dependency injection. [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).
- The current FastAPI lifecycle documentation teaches the lifespan parameter. [Lifespan](https://fastapi.tiangolo.com/advanced/events/).
- NestJS providers support injected services. TypeScript types alone are insufficient for request validation; the documented validation workflow uses DTO classes and a validation pipe. [Providers](https://docs.nestjs.com/providers), [validation](https://docs.nestjs.com/techniques/validation).
- Canvas animation is built around repeated drawing and animation scheduling. [MDN animation tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations).
- On the review date, Node 26 and Node 24 are both listed as LTS. Slide 5's Node 26 designation is not itself an error. [Official release table](https://nodejs.org/en/about/previous-releases).

## Next review boundary

Before creating final teaching branches, inspect the complete repository trees and tests, compare this year's frontend contract with the reference, then run fresh-install and browser integration checks. The instructor has selected Slidev for future iteration: validate a short SSR/testing prototype before migrating the course, using the original deck as reference. No runtime or live-deck verification is claimed here.

## Local reference follow-up

The instructor cloned the four missing repositories under `_reference/`. Their branches can now be enumerated locally. `ecm2025` contains `correct_api`, `develop`, `first_api`, `first_app`, `first_crud`, `first_db`, `first_templates`, `first_view`, `front_ready` and `wrong_api`. Both score repositories expose `main`; Space Invaders exposes `main` and three dependency-update branches. A separate local `react-todo` clone exists at `/Users/adrienbrunet/projects/react-todo`.

The earlier branch-list access blocker is resolved for these local snapshots. This does not imply a complete runtime audit of the old examples. The new 2026 lesson and its verification status are documented in `COURSE_PLAN.md`.

## Extension du jour 1 · Marshmallow et Blueprint

Les pages 49–54 du PDF du Google Slides original introduisent Marshmallow / SQLAlchemyAutoSchema, puis Flask-smorest, MethodView, les decorators `arguments` et `response`, la registration du Blueprint et la description OpenAPI. La nouvelle séquence reprend la séparation parse / validation / serialization, puis l’organisation du CRUD. Les champs Marshmallow sont déclarés explicitement pour que les règles restent visibles ; le Blueprint natif Flask permet d’apprendre la registration avec les decorators HTTP déjà connus. Une nouvelle étape installe Flask-smorest, présente arguments et response, puis ouvre la specification OpenAPI dans Swagger UI. AutoSchema reste une piste de recherche. Les pages 36 et 47 sont également reprises : fixture de capture du template et serialization manuelle avant la solution outillée.

La séquence conserve les assertions du cours actuel : une valeur invalide ne modifie aucune donnée, les booleans ne sont pas implicitement convertis, une seconde task reste intacte, et la persistance survit à une nouvelle app. Le test SSR comparant un template à lui-même reste présent pour montrer sa portée limitée.
