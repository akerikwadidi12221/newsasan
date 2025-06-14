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
7. Alternatively, start everything with Docker:
   ```bash
   docker-compose up --build
   ```

For more details see the `docs/` directory.

## Adding a Django App
Create a new folder under `buildmart-online/backend/` and add it to `INSTALLED_APPS` in `buildmart/settings/base.py`.

## Adding a React Page
Create a component under `frontend/src/pages` or `frontend/src/components` and register a route inside `src/pages/App.tsx` or your router configuration.

## Running Tests
- Backend: `pytest` inside `buildmart-online/backend`
- Frontend: `npm run test` inside `buildmart-online/frontend`
