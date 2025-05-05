import os

# Use different database URLs based on environment
is_docker = os.getenv("DOCKER_ENV") == "true"
db_host = "db" if is_docker else "localhost"
test_db_url = f"postgresql+psycopg://postgres:{os.getenv('DATABASE_PASSWORD')}@{db_host}:5432/test_db"
# Add a production database URL with the correct dialect
prod_db_url = f"postgresql+psycopg://postgres:{os.getenv('DATABASE_PASSWORD')}@{db_host}:5432/licitacao_hub"