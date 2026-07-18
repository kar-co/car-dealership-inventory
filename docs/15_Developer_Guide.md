# Developer Guide

Configure `backend/fastapi_backend/.env`, start PostgreSQL, run `alembic upgrade head`, then start Uvicorn. In a second terminal, run `npm install` and `npm run dev` from `frontend`. Run the test and quality commands in `09_Testing.md` before review.

## Dependency reference

The following declared project dependencies are listed with their purpose and primary usage location. Development, production, and testing requirement files all include `base.txt`.

| Dependency | Purpose | Used in |
| --- | --- | --- |
| alembic | Database migrations | `backend/fastapi_backend/alembic/` |
| annotated-types | Pydantic typing support | Pydantic runtime |
| anyio | Async compatibility | FastAPI runtime |
| asgiref | ASGI support | Django runtime |
| bcrypt | Password hashing | `app/core/security.py` |
| black | Python formatter | backend quality checks |
| certifi | Certificate bundle | HTTP dependency support |
| cffi | Native extension interface | bcrypt/cryptography support |
| click | Command-line support | Uvicorn/Alembic tooling |
| colorama | Terminal color support | Windows CLI tooling |
| coverage | Test coverage support | pytest tooling |
| cryptography | Cryptographic primitives | JWT dependency support |
| Django | Administrative framework | `backend/django_backend/` |
| ecdsa | Signing algorithms | python-jose support |
| fastapi | REST API framework | `app/main.py` and routes |
| flake8 | Python linting | backend quality checks |
| greenlet | SQLAlchemy concurrency | SQLAlchemy runtime |
| h11 | HTTP protocol | Uvicorn/HTTPX runtime |
| httpcore | HTTP transport | HTTPX runtime |
| httptools | HTTP parsing | Uvicorn runtime |
| httpx | HTTP tests/client | FastAPI tests |
| idna | International domains | HTTP support |
| iniconfig | Test configuration | pytest tooling |
| isort | Import sorting | backend quality checks |
| Mako | Migration templates | Alembic runtime |
| MarkupSafe | Safe markup | Django/Mako support |
| mccabe | Complexity checks | flake8 runtime |
| mypy_extensions | Typing support | Black runtime |
| packaging | Version parsing | Python tooling |
| passlib | Password utility dependency | retained requirements |
| pathspec | File patterns | Black runtime |
| platformdirs | Platform paths | Python tooling |
| pluggy | Plugin framework | pytest runtime |
| psycopg | PostgreSQL driver | SQLAlchemy engine |
| psycopg-binary | Binary PostgreSQL driver | local database support |
| pyasn1 | ASN.1 support | python-jose support |
| pycodestyle | Style checks | flake8 runtime |
| pycparser | C parser | cffi support |
| pydantic | API validation | `app/schemas/` |
| pydantic-settings | Environment settings | `app/core/config.py` |
| pydantic_core | Validation engine | Pydantic runtime |
| pyflakes | Static checks | flake8 runtime |
| Pygments | Terminal formatting | pytest tooling |
| pytest | Test framework | `app/tests/` |
| pytest-cov | Coverage plugin | pytest tooling |
| python-dotenv | `.env` parsing | settings runtime |
| python-jose | JWT handling | `app/core/security.py` |
| python-multipart | Form support | FastAPI runtime |
| pytokens | Token handling | Black runtime |
| PyYAML | YAML support | tooling dependency |
| rsa | RSA support | python-jose support |
| setuptools | Packaging | environment tooling |
| six | Compatibility | dependency support |
| SQLAlchemy | ORM and queries | `app/models/`, `app/db/` |
| sqlparse | SQL parsing | Django runtime |
| starlette | ASGI base | FastAPI runtime |
| typing-inspection | Type introspection | Pydantic runtime |
| typing_extensions | Extended types | FastAPI/Pydantic |
| tzdata | Time-zone data | datetime support |
| uvicorn | ASGI server | backend run command |
| watchfiles | Development reload | Uvicorn reload |
| websockets | WebSocket support | Uvicorn runtime |
| wheel | Package distribution | environment tooling |
| React | Component UI | `frontend/src/` |
| React DOM | Browser rendering | `frontend/src/main.jsx` |
| Vite | Dev server/build | `frontend/vite.config.js` |
| @vitejs/plugin-react | React transform | `frontend/vite.config.js` |
| Tailwind CSS | Utility CSS | `frontend/src/index.css` |
| PostCSS | CSS processing | `frontend/postcss.config.js` |
| Autoprefixer | CSS prefixes | `frontend/postcss.config.js` |
