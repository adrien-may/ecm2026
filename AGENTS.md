# Course authoring

- Write explanations in French, but keep technical terms in English. In particular: headers, body, request, response, status code, decorator, factory, fixture, template, package, checkpoint and server-side rendering. Never translate headers as « en-têtes » or body as « corps ».
- Leave `_reference/` unchanged.
- Use course names for branches, steps and artifacts. Never use an agent or product name as a prefix; Flask checkpoint branches use `flask-00-ready`, `flask-01-flask`, etc.
- Introduce tools when students need them. Keep the slide sequence, runnable code, checkpoint branches, downloadable archives and expected test results consistent.
- Whenever a Python package is introduced, show its exact directory tree and the precise location of its `__init__.py`. Distinguish required package markers from optional test-package conventions and ordinary folders such as templates.
- Put every file operation in the main slide content at normal body size, never only in the top-right label. Distinguish creating a directory, creating a file, editing an existing file, moving a file, and opening a provided file. Give the exact path and insertion point. Introduce helpers before their first call and explicitly announce when a supplied checkpoint replaces the current working project.
- Introduce the behavior students need to build and explain why it is useful before suggesting a helper name. Function names chosen for this course must not sound like pre-existing framework features or assumed requirements.
- For the guided Flask lesson, show every new or replaced code block directly in the slides. Checkpoint archives support comparison and recovery; they must not hide required implementation steps.
