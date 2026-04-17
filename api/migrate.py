"""
Migreringsscript — køres én gang efter deploy på Render.com Shell.

Hvad det gør:
  1. Sletter alle eksisterende todos (mangler user_id kolonne)
  2. Dropper todos tabellen
  3. Genskaber todos tabellen med user_id kolonne (ForeignKey til users)

Kør med:
  python -m api.migrate
"""

from api.database import engine, Base
from api.models_db import TodoDB        # registrerer TodoDB med Base
from api.models_db_auth import UserDB   # registrerer UserDB med Base (skal eksistere)


def run():
    print("Starter migration...")

    with engine.connect() as conn:
        print("  Dropper todos tabellen hvis den eksisterer...")
        conn.execute(TodoDB.__table__.delete())
        conn.commit()

    print("  Dropper og genskaber todos tabellen...")
    TodoDB.__table__.drop(bind=engine, checkfirst=True)
    TodoDB.__table__.create(bind=engine)

    print("Migration fuldfoert. todos tabellen er genskabt med user_id kolonne.")


if __name__ == "__main__":
    run()
