import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
print("DB_USER loaded:", bool(os.getenv("DB_USER")))
print("DB_PASSWORD loaded:", bool(os.getenv("DB_PASSWORD")))

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "hangman_db")
)

engine = create_engine(connection_url)


def get_high_score(player_name="Player"):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COALESCE(MAX(high_score), 0)
                FROM hangman_scores
                WHERE player_name = :player_name
            """),
            {"player_name": player_name}
        )

        return result.scalar()


def save_high_score(score, player_name="Player"):
    with engine.begin() as connection:

        current_score = connection.execute(
            text("""
                SELECT MAX(high_score)
                FROM hangman_scores
                WHERE player_name = :player_name
            """),
            {"player_name": player_name}
        ).scalar()

        if current_score is None:
            connection.execute(
                text("""
                    INSERT INTO hangman_scores
                    (player_name, high_score)
                    VALUES (:player_name, :score)
                """),
                {"player_name": player_name, "score": score}
            )

        elif score > current_score:
            connection.execute(
                text("""
                    UPDATE hangman_scores
                    SET high_score = :score,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE player_name = :player_name
                """),
                {"player_name": player_name, "score": score}
            )


def get_random_word(level):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT word
                FROM hangman_words
                WHERE level = :level
                ORDER BY RANDOM()
                LIMIT 1
            """),
            {"level": level}
        )

        return result.scalar()


if __name__ == "__main__":
    print("Testing database connection...")

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_schema()")
        )
        print("Database:", result.fetchone())

    print("Testing High Score...")
    print("Current High Score:", get_high_score())

    save_high_score(10)

    print("Updated High Score:", get_high_score())

