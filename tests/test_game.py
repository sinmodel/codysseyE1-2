import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game import QuizGame


class TopicSelectionTests(unittest.TestCase):
    def test_play_quiz_samples_only_the_selected_topic(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            game = QuizGame(state_path=Path(temporary_directory) / "state.json")
            topics = list(dict.fromkeys(quiz.topic for quiz in game.quizzes))
            git_topic_number = topics.index("Git") + 1
            sampled_populations = []

            def sample(population, question_count):
                sampled_populations.append((population, question_count))
                return [population[0]]

            with (
                patch(
                    "builtins.input",
                    side_effect=[str(git_topic_number), "1", "1"],
                ),
                patch("game.random.sample", side_effect=sample),
                patch.object(game, "record_game", return_value=(False, "저장했습니다.")),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                game.play_quiz()

            self.assertEqual(len(sampled_populations), 1)
            population, question_count = sampled_populations[0]
            self.assertTrue(population)
            self.assertTrue(all(quiz.topic == "Git" for quiz in population))
            self.assertEqual(question_count, 1)


if __name__ == "__main__":
    unittest.main()
