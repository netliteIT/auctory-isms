# Document control procedure (ISMS-as-Code)

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Purpose
Ensure ISMS documentation is controlled, updated, approved and traceable.

## Rules
- All ISMS documents live in this Git repository.
- Changes are made via **Pull Request** with mandatory review.
- Recommended branch protection:
  - PR required
  - at least 1 reviewer
  - status checks (CI) where applicable
- Each document includes a date/version in its header.
- After the annual Management Review, create a **release tag** (e.g. `ISMS-2026-v1.0`).

## Retention
- Git history is the versioning record.
- Repository backup per provider policy (GitHub) + optional periodic export.
