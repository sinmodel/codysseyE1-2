import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game import QuizGame
from quiz import DEFAULT_QUIZZES


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


class ExplanationTests(unittest.TestCase):
    def test_all_default_quizzes_have_explanations(self):
        missing = [quiz.question for quiz in DEFAULT_QUIZZES if not quiz.explanation.strip()]
        self.assertEqual(missing, [])

    def test_migration_fills_missing_explanations_without_overwriting_existing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_path = Path(temporary_directory) / "state.json"
            first_quiz, second_quiz = DEFAULT_QUIZZES[:2]
            state = {
                "quizzes": [
                    {**first_quiz.to_dict(), "explanation": ""},
                    {**second_quiz.to_dict(), "explanation": "사용자가 작성한 설명"},
                ],
                "best_score": 90,
                "best_correct": 9,
                "best_total": 10,
                "history": [],
                "quiz_bank_version": 2,
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")

            game = QuizGame(state_path=state_path)
            explanations = {quiz.question: quiz.explanation for quiz in game.quizzes}
            updated_state = json.loads(state_path.read_text(encoding="utf-8"))

            self.assertEqual(explanations[first_quiz.question], first_quiz.explanation)
            self.assertEqual(explanations[second_quiz.question], "사용자가 작성한 설명")
            self.assertEqual(game.best_score, 90)
            self.assertEqual(updated_state["quiz_bank_version"], 3)


if __name__ == "__main__":
    unittest.main()
