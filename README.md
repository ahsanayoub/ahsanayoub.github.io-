# Talent Acquisition Platform Monorepo Baseline

This repository contains a baseline full-stack setup for a recruitment platform:

- `frontend/`: Next.js 14 (App Router, TypeScript, Tailwind CSS, shadcn/ui conventions)
- `backend/`: FastAPI with a clean architecture-inspired module layout
- `docker-compose.yml`: local orchestration for frontend, backend, and PostgreSQL

## Project structure

```text
.
├── frontend/
│   ├── app/
│   │   ├── login/page.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── requisitions/page.tsx
│   │   └── candidates/page.tsx
│   ├── components/
│   ├── hooks/
│   └── lib/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── routers/
│   │   └── repositories/
│   └── alembic/
├── docker-compose.yml
└── .env.example
```

## Coding conventions and module boundaries

### Backend (FastAPI)

- **`routers/`**: transport layer only (HTTP concerns, request/response mapping, dependency wiring).
- **`services/`**: use-case/business logic. Services should not import FastAPI primitives.
- **`repositories/`**: data-access abstraction over SQLAlchemy.
- **`models/`**: SQLAlchemy ORM entities.
- **`schemas/`**: Pydantic request/response/data-transfer objects.
- **`core/`**: cross-cutting concerns (settings, security, DB session).

Rules:
1. `routers -> services -> repositories -> models`
2. `schemas` can be shared between routers/services, but ORM models should not leak to API responses.
3. Keep side effects (DB/network) out of routers whenever possible.

### Frontend (Next.js)

- Route files live in `app/**/page.tsx`.
- Reusable visual pieces belong in `components/`.
- Shared utilities and API clients belong in `lib/`.
- Client-side auth/navigation helpers belong in `hooks/`.

Rules:
1. Page-level data orchestration stays in route segments; reusable view logic moves to `components/`.
2. API calls go through `lib/api.ts` for consistency.
3. Keep UI primitives in `components/ui/` (shadcn-style approach).

## Local development

1. Copy env defaults:
   ```bash
   cp .env.example .env
   ```
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Open:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

## Notes

- This is a baseline scaffold intended for extension.
- Add domain-specific models, migrations, and auth flows before production use.
