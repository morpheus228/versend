from config import Config
from repositories.orm import Base, get_orm


def make_migrations():
    orm = get_orm()
    Base.metadata.drop_all(orm)
    # Base.metadata.create_all(orm)
    print("✅ Миграции для БД сделаны.")


if __name__ == "__main__":
    Config.set()
    make_migrations()