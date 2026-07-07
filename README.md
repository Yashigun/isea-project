# Vimsy

Vimsy is a full-stack e-commerce application with a Next.js storefront and a FastAPI backend. It includes customer authentication, product browsing, cart and wishlist flows, checkout-related data models, reviews, and an admin area for catalog, orders, and security visibility.

## Stack

- Frontend: Next.js 16, TypeScript, Tailwind CSS 4
- Backend: FastAPI, SQLAlchemy async, Alembic
- Database: PostgreSQL 16
- Media: Cloudinary for product image uploads
- Auth: JWT access/refresh tokens with cookie support

## Features

- Customer signup, login, logout, session refresh, and password change
- Product catalog with categories, collections, and product detail pages
- Cart and wishlist APIs and frontend flows
- Customer profile pages for account, addresses, and phone numbers
- Product reviews
- Admin pages for products, categories, orders, and security monitoring
- Security-related persistence for login attempts, blocked IPs, audit logs, request logs, and customer sessions

## Repository Layout

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/           # FastAPI route modules
|   |   |-- core/          # settings, auth dependencies, exceptions
|   |   |-- db/            # async SQLAlchemy engine/session
|   |   |-- middlewares/   # request and security event logging
|   |   |-- models/        # store + security models
|   |   |-- repositories/  # data access layer
|   |   |-- schemas/       # request/response schemas
|   |   |-- services/      # business logic
|   |   `-- validators/    # validation helpers
|   |-- alembic/
|   `-- tests/
|-- frontend/
|   |-- src/app/           # Next.js app router pages
|   |-- src/components/    # UI, auth, admin, product, profile components
|   |-- src/hooks/         # frontend data hooks
|   |-- src/lib/           # axios client, auth helpers
|   |-- src/services/      # API wrappers
|   `-- public/
`-- docker-compose.yml     # local PostgreSQL service
```

## Local Development

### 1. Start PostgreSQL

The included Compose file provisions PostgreSQL only.

```bash
docker compose up -d
```

This uses values from the root `.env` file:

```env
POSTGRES_USER=<db user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
```

### 2. Configure the backend

The backend loads settings from `backend/.env` or the current working directory `.env`, depending on how you run it. At minimum, the code expects values for:

```env
APP_NAME=Personal <store name>
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=<db connection string>

JWT_ACCESS_SECRET_KEY=change-me
JWT_REFRESH_SECRET_KEY=change-me-too
JWT_ALGORITHM=HS256
JWT_ISSUER=personal-store
JWT_AUDIENCE=personal-store-users
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

COOKIE_SECURE=false  #change it is true for deployment
COOKIE_HTTPONLY=true
COOKIE_SAMESITE=lax

ALLOWED_ORIGINS=http://localhost:3000    #NextJS default port
LOG_LEVEL=INFO

MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCK_MINUTES=15
PASSWORD_MIN_LENGTH=8
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

REDIS_URL=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_UPLOAD_PRESET=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
```

Install Python dependencies in your preferred environment, then run the API server from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with:

- `GET /` for a basic status message
- `GET /health` for a health check
- `GET /docs` for Swagger UI

### 3. Run database migrations

From `backend/`:

```bash
alembic upgrade head
```

### 4. Start the frontend

From `frontend/`:

```bash
npm install
npm run dev
```

The frontend runs at `http://localhost:3000`.

By default, frontend requests are routed to:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1
```

## Notable API Areas

- `/api/v1/auth`
- `/api/v1/products`
- `/api/v1/categories`
- `/api/v1/cart`
- `/api/v1/orders`
- `/api/v1/addresses`
- `/api/v1/phones`
- `/api/v1/wishlist`
- `/api/v1/reviews`
- `/api/v1/admin`


