# Migrations

1. Set env: `export LN_SERVER_DEPLOY=1` (it tells `lnhub_rest` that the server-side admin connection string is available)
2. Modify the schema by rewriting the ORMs (add a column, rename a column, add constraints, drop constraints, add an ORM, etc.)
3. Auto-generate the migration script: `lnhub migrate generate`
4. Thoroughly test the migration script: `pytest tests/test_migrations.py` (is also run on CI)
5. Merge to main and make a release commit, bumping the version number

Deploy migration to production database: `lnhub migrate deploy` while setting `export LNHUB_PROD_PG_PASSWORD=***`
