# Contributing

Thanks for helping make MicroLab more accurate and more useful.

## Report a wrong number

The most valuable contribution is a correction. Open an issue with:
- the board or part and the field that's wrong,
- the correct value,
- a link to the datasheet or manufacturer page.

## Report a bug

Include the board, the circuit (or a screenshot) and the sketch. The console message is very helpful.

## Change the code

1. Fork and branch from `main`.
2. Make your change in `index.html`. Guides for common changes: [docs/contributing-parts.md](docs/contributing-parts.md) and [docs/languages.md](docs/languages.md).
3. Run the tests:
   ```bash
   cd tests && npm install && pip install -r requirements.txt && python -m playwright install chromium
   python -m pytest -q
   ```
4. Open a pull request describing what changed and how you checked it. CI runs the same tests.

## Ground rules

- Be honest in the simulation: if something isn't modelled, say so instead of faking it.
- Keep messages plain and actionable: say what's wrong and how to fix it.
- Mark uncertain specs as uncertain.
