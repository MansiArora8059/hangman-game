import os
import sys
from sqlalchemy import create_engine, text

# Handle path for PyInstaller bundled files
if getattr(sys, "frozen", False):
    # PyInstaller extracts bundled data to _MEIPASS
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, "hangman.db")

# SQLite connection configuration
engine = create_engine(
    f"sqlite:///{db_path}",
    connect_args={"check_same_thread": False}
)


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