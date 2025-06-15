# BuildMart Online

BuildMart Online is a full-stack e-commerce platform powered by Django and React.

## Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

## Local Setup
1. Clone the repository
2. Create and activate a virtual environment
3. Install backend dependencies:
   ```bash
   pip install -r buildmart-online/backend/requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd buildmart-online/frontend
   npm install
   ```
5. Configure environment variables in `.env`
6. Apply migrations and run the development servers:
   ```bash
   python buildmart-online/backend/manage.py migrate
   python buildmart-online/backend/manage.py runserver
   npm run dev
   ```
   The frontend dev server will be available at `http://localhost:3000/` and the
   backend will respond at `http://127.0.0.1:8000/` with a small JSON
   confirmation.
7. Alternatively, start everything with Docker:
   ```bash
   docker-compose up --build
   ```

For more details see the `docs/` directory.

## API Endpoints

The catalog app exposes basic read-only endpoints under `/api/catalog/`:

- `/categories/` list of product categories
- `/categories/<id>/` single category details
- `/brands/` list of brands
- `/brands/<id>/` single brand details
- `/products/` list of products
- `/products/<id>/` single product details

## Admin Features

The Django admin panel is configured with several advanced options:

- Category management uses **django-mptt** for a tree view with drag & drop
- Products include inline editing for images, variants and specifications
- Orders show order items inline and include an action to mark them as sent

## Adding a Django App
Create a new folder under `buildmart-online/backend/` and add it to `INSTALLED_APPS` in `buildmart/settings/base.py`.

## Adding a React Page
Create a component under `frontend/src/pages` or `frontend/src/components` and register a route inside `src/pages/App.tsx` or your router configuration.

## Running Tests
- Backend: `pytest` inside `buildmart-online/backend`
- Frontend: `npm run test` inside `buildmart-online/frontend`

## Product Data Storage

Product images and specification files can be stored inside the `database/` directory
at the project root:

```
newsasan/
  database/
    images/   # place JPG/PNG files here
    specs/    # CSV or JSON specification files
```

Commit your assets to Git if you want them version controlled. Empty `.gitkeep`
files are provided so the folders exist by default.

## Loading Brand Categories

After applying migrations you can create the four main brand categories using the
included management command:

```bash
python buildmart-online/backend/manage.py create_brand_categories
```

This will ensure the following categories exist:
1. لوله واتصالات پنج لایه نیوپایپ
2. لوله و اتصالات تک لایه آذین
3. لوله و اتصالات فاضلابی مولتی پایپ
4. محصولات پلی اتیلن آبیاری دینا پلیمر

## Importing Products from JSON

Sample product data can be stored in `database/space/got.json`. After
creating your categories run the following command to load these products
into the database:

```bash
python buildmart-online/backend/manage.py import_products_json
```

The command accepts an optional path to the JSON file and a category ID to
assign the imported products.

