from .database import make_engine
from .models import Base


def main():
    engine = make_engine()
    try:
        Base.metadata.create_all(engine)
        print("Database ready")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
