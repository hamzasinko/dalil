## Description

<!-- What does this PR do? Why is it needed? -->

## Type of change

- [ ] `feat` — new feature
- [ ] `fix` — bug fix
- [ ] `docs` — documentation only
- [ ] `refactor` — code change without behavior change
- [ ] `test` — tests only
- [ ] `chore` — maintenance (CI, packaging, tooling)

## Related issue

<!-- Use "Closes #123" so the issue is closed automatically. -->

Closes #

## How to test

```bash
python -m pytest tests/ -k <relevant-test>
```

<!-- Steps, snippets, or screenshots to reproduce / validate the change. -->

## Checklist

- [ ] Tests added for nominal **and** edge cases
- [ ] Coverage stays >= 90% (`python -m pytest`)
- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `mypy --strict src tests` passes
- [ ] Documentation and `CHANGELOG.md` updated
- [ ] Branch created from `dev` and PR targets `dev`
