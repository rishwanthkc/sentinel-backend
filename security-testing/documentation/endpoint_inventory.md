# Sentinel Backend Endpoint Inventory

Generated from source inspection of `app/main.py` and route modules.

## Public Endpoints

- `GET /` — Public — Health check / welcome message.
- `GET /health` — Public — Application health status.
- `POST /auth/register` — Public — User registration.
- `POST /auth/login` — Public — User login by email.

## Emergency Endpoints

- `POST /emergency/trigger` — Public — Trigger an emergency event. No auth enforced in source.
- `GET /emergency/history/{email}` — Public — Retrieve emergency history for the specified email. No auth enforcement observed.
- `POST /emergency/resolve/{emergency_id}` — Public — Resolve an emergency by its numeric ID. No auth enforcement observed.
- `GET /emergency/active` — Public — List active emergencies. No auth enforcement observed.

## Emergency Contacts Endpoints

- `POST /contacts/add` — Public — Add a contact to a user email. No auth enforcement observed.
- `GET /contacts/{user_email}` — Public — Retrieve emergency contacts for a user email. No auth enforcement observed.

## Report Endpoints

- `POST /reports/submit` — Public — Submit a report. No auth enforcement observed.
- `GET /reports/all` — Public — Retrieve all reports. No auth enforcement observed.

## Dashboard Endpoints

- `GET /dashboard/stats` — Public — Dashboard statistics. No auth enforcement observed.
- `GET /dashboard/reports` — Public — Retrieve all reports for dashboard. No auth enforcement observed.
- `GET /dashboard/emergencies` — Public — Retrieve all emergencies. No auth enforcement observed.
- `GET /dashboard/users` — Public — Retrieve all users. No auth enforcement observed.
- `GET /dashboard/analytics` — Public — Analytics summary. No auth enforcement observed.
- `GET /dashboard/hotspots` — Public — Hotspot risk summary. No auth enforcement observed.
- `POST /dashboard/resolve/{id}` — Public — Resolve emergency from dashboard. No auth enforcement observed.

## Safety Routing Endpoints

- `GET /safety/risk-points` — Public — Return risk points from crime dataset and reports. No auth enforcement observed.
- `GET /safety/route` — Public — Compute safe route via Google Directions. No auth enforcement observed.

## Notes

- No JWT or bearer authentication hooks are present in inspected routes.
- No role-based restrictions are enforced in the current backend route source.
- There are raw SQL queries and updates in several endpoints, including `trigger_emergency`, `resolve_emergency`, `dashboard_reports`, `dashboard_emergencies`, `dashboard_users`, `get_hotspots`, and `resolve_emergency`.
- The application uses environment variables for DB credentials. The local `.env` file contains a password that should be treated as sensitive.
