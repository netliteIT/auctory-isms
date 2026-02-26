# Change management procedure

> Version: 2026-02-26  
> Owner: Andrea Gagliardi

## Purpose
Ensure production changes are authorized, tested and traceable.

## Rules
- Every production change requires:
  - ticket/issue or change record
  - PR with review
  - test evidence (staging) where applicable
- Deploy: preferably automated (CI/CD) with release logs.
- Rollback: define per-component strategy (document in service runbooks).
