# AURA Django Backend

A small Django REST backend for the static AURA storefront.

## Setup on Windows PowerShell

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/`.

## API routes

- `GET /api/products/` - product catalog; supports `?category=women` and `?search=trench`
- `POST /api/auth/register/` - create a session-authenticated account
- `POST /api/auth/login/` - log in with username and password
- `POST /api/auth/logout/` - log out
- `GET /api/auth/me/` - current authenticated user
- `GET /api/orders/` - current user's orders
- `POST /api/orders/create/` - create an order with `items` and `shipping_address`
- `POST /api/auth/google/` - reserved for verified Google sign-in; dormant by default

## Google sign-in

Google login is intentionally disabled in `aura_backend/settings.py`:

```python
GOOGLE_LOGIN_ENABLED = False
```

Before enabling it, add a real OAuth client ID and implement server-side token verification with Google's official library. Do not trust an ID token decoded only in browser JavaScript. Use HTTPS and configure the frontend origin in Google Cloud Console.
