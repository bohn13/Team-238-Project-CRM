# Seed data CSV contract

Put fake data CSV files in this directory. The seed command is idempotent and
does not delete existing records.

## users.csv

Required columns:

- `email`
- `first_name`
- `last_name`

Optional columns:

- `password` - defaults to `SEED_DEFAULT_PASSWORD` or `SeedPassword123!`
- `role` - one of `superadmin`, `admin`, `doctor`, `manager`, `patient`, `user`
- `phone_number`
- `is_active` - one of `true`, `false`, `yes`, `no`, `1`, `0`

## doctors.csv

Required columns:

- `email`
- `first_name`
- `last_name`
- `specialization`

Optional columns:

- `password`
- `phone_number`
- `is_active`
- `years_experience`
- `employment_type` - one of `full_time`, `part_time`
- `avatar_url`

Rows in `doctors.csv` create or reuse a seed user with role `doctor`, then create
the related doctor profile.

This directory includes small `users.csv` and `doctors.csv` examples with 10 rows
each. Replace them with larger fake datasets when needed.

## Docker Compose

Run migrations only:

```bash
docker compose run --rm migration
```

Run migrations and seed CSV data:

```bash
SEED_DATABASE=1 docker compose run --rm migration
```
