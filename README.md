# Multi-tenant Organization Service (FastAPI + MongoDB)

Backend service that manages organizations and admin users in a simple multi-tenant style. The master database keeps global metadata (organizations and users). Each organization gets its own MongoDB collection (`org_<slug>`). JWT-based admin auth protects destructive actions.

## Tech Stack
- FastAPI, Uvicorn
- MongoDB via Motor (async)
- JWT (PyJWT), password hashing (Passlib/bcrypt)

## Running Locally
1. Ensure Python 3.10+ and MongoDB are available.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env template and adjust values:
   ```bash
   copy env.example .env   # Windows
   # or: cp env.example .env
   ```
4. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Swagger UI: http://localhost:8000/docs

## API Overview
- `POST /org/create` – create organization + admin + dynamic collection
- `GET /org/get` – fetch organization metadata by name
- `PUT /org/update` – update org/admin; optional rename creates new collection and copies data
- `DELETE /org/delete` – delete organization (requires admin JWT)
- `POST /admin/login` – admin login, returns JWT with `admin_id` and `org_name`

## High-level Flow
```
graph TD
  Client -->|create/get/update/delete/login| FastAPI
  FastAPI -->|metadata| MasterDB[(Mongo master)]
  FastAPI -->|per-org data| OrgCollections[(org_<slug> collections)]
  MasterDB -->|stores| Organizations & Users
```

## Notes & Assumptions
- Collections are created in the same Mongo database for simplicity; connection info is stored to support separation later.
- Organization rename (`new_organization_name`) will create `org_<new>` collection, copy documents from the old collection, then drop the old one.
- Passwords are stored hashed (bcrypt). JWT expiration is configurable.
- Master DB collections used: `organizations`, `users`, and dynamic `org_<slug>`.

## Future Improvements
- Add per-collection indexes and schema validation.
- Move per-tenant data to isolated databases/cluster-level separation.
- Introduce refresh tokens and role-based permissions beyond admin.
- Add unit/integration tests and CI.

