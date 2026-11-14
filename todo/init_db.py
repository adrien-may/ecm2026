from .database import make_engine
from sqlmodel import SQLModel


def main():
    engine = make_engine()
    try:
        SQLModel.metadata.create_all(engine)
        print("Database ready")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
