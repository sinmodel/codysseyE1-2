import json
from datetime import datetime
from pathlib import Path

from quiz import DEFAULT_QUIZZES, Quiz


QUIZ_BANK_VERSION = 1


class QuizGame:
    def __init__(self, state_path=None):
        self.state_path = Path(state_path) if state_path else Path(__file__).with_name("state.json")
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0
        self.history = []
        self.quiz_bank_version = QUIZ_BANK_VERSION
        self.load_message = ""
        self.load_data()

    def load_data(self):
        if not self.state_path.exists():
            self.load_message = "처음 실행입니다. 기본 퀴즈를 준비했습니다."
            self.save_data()
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as state_file:
                data = json.load(state_file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터의 최상위 값은 객체여야 합니다.")

            stored_quizzes = data.get("quizzes", [])
            if not isinstance(stored_quizzes, list):
                raise ValueError("quizzes 항목은 목록이어야 합니다.")

            loaded_quizzes = [Quiz.from_dict(item) for item in stored_quizzes]
            stored_bank_version = self._valid_nonnegative_integer(data.get("quiz_bank_version", 0))
            added_defaults = []
            if stored_bank_version < QUIZ_BANK_VERSION:
                saved_questions = {quiz.question for quiz in loaded_quizzes}
                added_defaults = [
                    quiz for quiz in DEFAULT_QUIZZES if quiz.question not in saved_questions
                ]
                loaded_quizzes.extend(added_defaults)

            self.quizzes = loaded_quizzes
            self.best_score = self._valid_nonnegative_integer(data.get("best_score", 0))
            self.best_correct = self._valid_nonnegative_integer(data.get("best_correct", 0))
            self.best_total = self._valid_nonnegative_integer(data.get("best_total", 0))
            self.quiz_bank_version = QUIZ_BANK_VERSION
            stored_history = data.get("history", [])
            if not isinstance(stored_history, list):
                raise ValueError("history 항목은 목록이어야 합니다.")
            self.history = stored_history
            if added_defaults:
                self.load_message = f"저장된 문제를 보존하고 새 기본 문제 {len(added_defaults)}개를 추가했습니다."
                self.save_data()
            else:
                self.load_message = f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다."
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
            self.best_correct = 0
            self.best_total = 0
            self.history = []
            self.load_message = f"저장 파일을 읽지 못해 기본 데이터로 시작합니다: {error}"

    @staticmethod
    def _valid_nonnegative_integer(value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("점수 데이터는 0 이상의 정수여야 합니다.")
        return value

    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "history": self.history,
            "quiz_bank_version": self.quiz_bank_version,
        }
        temporary_path = self.state_path.with_suffix(".json.tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as state_file:
                json.dump(data, state_file, ensure_ascii=False, indent=2)
                state_file.write("\n")
            temporary_path.replace(self.state_path)
            return True, "저장했습니다."
        except (OSError, TypeError, ValueError) as error:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            return False, f"파일을 저장하지 못했습니다: {error}"

    def add_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            raise TypeError("퀴즈는 Quiz 객체여야 합니다.")
        self.quizzes.append(quiz)
        return self.save_data()

    def record_game(self, correct, total):
        if total <= 0:
            return False, "출제할 퀴즈가 없습니다."

        score = round(correct / total * 100)
        self.history.append(
            {
                "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "correct": correct,
                "total": total,
                "score": score,
            }
        )

        is_new_best = score > self.best_score or self.best_total == 0
        if is_new_best:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total

        saved, message = self.save_data()
        return is_new_best, message if saved else message
