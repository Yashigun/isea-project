<div align="center">

# Vimsy
  <img src="frontend/public/images/hero.png" alt="Storefront Screenshot" width="800">
</div>

### Vimsy is a full-stack security aware e-commerce application with a Next.js storefront and a FastAPI backend. It includes customer authentication, product browsing, cart and wishlist flows, checkout-related data models, reviews, and an admin area for catalog, orders, and security visibility.

---

## Features

### E-Commerce Functionality

* Customer account management with signup, login, logout, access-token refresh, and secure password changes
* Product catalog with category and collection organization, product listings, and detailed product pages
* Persistent shopping cart with product quantity management and customer-specific cart data
* Customer wishlist for saving and managing products
* Customer profile dashboard with account information, saved addresses, and phone number management
* Product review system for authenticated customers
* Order management and order tracking workflows

### Administration

* Administrative dashboard for managing store operations
* Product creation, modification, deletion, and image management
* Category and collection management
* Customer order management and order status updates
* Security monitoring interface for reviewing application activity and security-related data

### Authentication and Application Security

* Secure customer authentication and session management
* Short-lived access tokens with refresh-token-based session renewal
* Server-side customer session tracking and session revocation
* Secure password hashing and password change workflows
* Role-based authorization for protected administrative functionality
* API input validation and protected customer-specific resources

### Security Monitoring and Digital Forensics

* HTTP request logging with request metadata, response status, and performance information
* Authentication attempt tracking for successful and failed login activity
* Customer session monitoring and activity tracking
* Blocked IP persistence and management
* Audit logging infrastructure for recording security-sensitive and business-critical actions
* Security event persistence for detected suspicious activity
* Request correlation and security telemetry designed to support incident investigation and forensic analysis

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS 4 (HTTPS) |
| **Backend** | FastAPI, SQLAlchemy async, Alembic |
| **Database** | PostgreSQL 16 |
| **Media** | Cloudinary |
| **Authbtication** |  Argon2, JWT |

---

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

The backend loads settings from `backend/.env`:

```env
APP_NAME=Personal <store name>
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=<db connection string>

JWT_ACCESS_SECRET_KEY=change-me
JWT_REFRESH_SECRET_KEY=change-me-too
JWT_ALGORITHM=HS256
JWT_ISSUER=
JWT_AUDIENCE=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=

COOKIE_SECURE=false  #change it is true for deployment
COOKIE_HTTPONLY=true
COOKIE_SAMESITE=lax

ALLOWED_ORIGINS=http://localhost:3000    #NextJS default port
LOG_LEVEL=INFO

MAX_LOGIN_ATTEMPTS=
ACCOUNT_LOCK_MINUTES=
PASSWORD_MIN_LENGTH=
RATE_LIMIT_REQUESTS=
RATE_LIMIT_WINDOW_SECONDS=

REDIS_URL=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_UPLOAD_PRESET=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
```

### 3. Start the backend

From `backend/`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`.

### 4. Run database migrations

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


