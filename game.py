import json
import random
import unicodedata
from datetime import datetime
from pathlib import Path

from quiz import DEFAULT_QUIZZES, Quiz


QUIZ_BANK_VERSION = 3
PANEL_WIDTH = 40


def display_width(text):
    return sum(
        2 if unicodedata.east_asian_width(character) in {"F", "W"} else 1
        for character in text
    )


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
            saved, message = self.save_data()
            if not saved:
                self.load_message += f" 초기 데이터 저장에 실패했습니다: {message}"
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
            updated_explanations = 0
            if stored_bank_version < QUIZ_BANK_VERSION:
                default_quizzes_by_question = {
                    quiz.question: quiz for quiz in DEFAULT_QUIZZES
                }
                for quiz in loaded_quizzes:
                    default_quiz = default_quizzes_by_question.get(quiz.question)
                    if default_quiz and not quiz.explanation and default_quiz.explanation:
                        quiz.explanation = default_quiz.explanation
                        updated_explanations += 1

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
            if stored_bank_version < QUIZ_BANK_VERSION:
                if added_defaults and updated_explanations:
                    self.load_message = (
                        f"저장된 문제를 보존하고 새 기본 문제 {len(added_defaults)}개를 추가했으며, "
                        f"{updated_explanations}개의 설명을 보완했습니다."
                    )
                elif added_defaults:
                    self.load_message = f"저장된 문제를 보존하고 새 기본 문제 {len(added_defaults)}개를 추가했습니다."
                elif updated_explanations:
                    self.load_message = f"저장된 퀴즈 {len(self.quizzes)}개 중 설명 {updated_explanations}개를 보완했습니다."
                else:
                    self.load_message = f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다."
                saved, message = self.save_data()
                if not saved:
                    self.load_message += f" 업데이트 저장에 실패했습니다: {message}"
            else:
                self.load_message = f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다."
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
            self.best_correct = 0
            self.best_total = 0
            self.history = []
            self.load_message = f"저장 파일을 읽지 못해 기본 데이터로 시작합니다: {error}"
            saved, message = self.save_data()
            if saved:
                self.load_message += " 기본 데이터로 복구했습니다."
            else:
                self.load_message += f" 기본 데이터 저장에 실패했습니다: {message}"

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

    @staticmethod
    def _read_required(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("입력이 비어 있습니다. 다시 입력해 주세요.")

    @staticmethod
    def _read_number(prompt, minimum, maximum):
        while True:
            value = input(prompt).strip()
            if not value:
                print("입력이 비어 있습니다. 다시 입력해 주세요.")
                continue
            try:
                number = int(value)
            except ValueError:
                print("숫자로 입력해 주세요.")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"{minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")

    def show_menu(self):
        separator = "=" * PANEL_WIDTH
        title = "기초 명령어 퀴즈 게임"
        title_padding = (PANEL_WIDTH - display_width(title)) // 2
        print()
        print(separator)
        print(" " * title_padding + title)
        print(separator)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print(separator)

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        topics = list(dict.fromkeys(quiz.topic for quiz in self.quizzes))
        print("\n주제를 선택해 주세요.")
        for topic_number, topic in enumerate(topics, start=1):
            print(f"{topic_number}. {topic}")
        selected_topic_number = self._read_number("주제 번호: ", 1, len(topics))
        selected_topic = topics[selected_topic_number - 1]
        topic_quizzes = [quiz for quiz in self.quizzes if quiz.topic == selected_topic]

        maximum = len(topic_quizzes)
        question_count = self._read_number(f"몇 문제를 풀까요? (1-{maximum}): ", 1, maximum)
        selected_quizzes = random.sample(topic_quizzes, question_count)
        correct_count = 0

        for question_number, quiz in enumerate(selected_quizzes, start=1):
            print(f"\n[{question_number}/{question_count}] {quiz.topic}")
            print(quiz.question)
            for choice_number, choice in enumerate(quiz.choices, start=1):
                print(f"  {choice_number}. {choice}")

            while True:
                response = input("정답 번호(예: 4번) 또는 보기 문구: ").strip()
                if quiz.get_answer_number(response) is not None:
                    break
                print("보기의 번호(1-4, 예: 4번)나 보기 문구를 입력해 주세요.")

            if quiz.is_correct(response):
                correct_count += 1
                print("정답입니다.")
                if quiz.explanation:
                    print(f"해설: {quiz.explanation}")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"아쉬워요. 정답은 {quiz.answer}. {correct_choice}입니다.")
                if quiz.explanation:
                    print(f"해설: {quiz.explanation}")

        is_new_best, save_message = self.record_game(correct_count, question_count)
        score = round(correct_count / question_count * 100)
        print(f"\n결과: {question_count}문제 중 {correct_count}문제 정답 ({score}점)")
        if is_new_best:
            print("새로운 최고 점수입니다.")
        print(save_message)

    def add_quiz(self):
        question = self._read_required("문제: ")
        choices = [self._read_required(f"선택지 {number}: ") for number in range(1, 5)]
        print("안내: 주제는 Python, JSON, Git, GitHub 중에서 입력해 주세요.")
        print("중복 문제 확인과 기존 문제 수정은 지원하지 않습니다.")
        topic = self._read_required("주제 (Python/JSON/Git/GitHub): ")
        explanation = self._read_required("해설: ")
        draft = Quiz(question, choices, 1, topic, explanation)

        while True:
            response = input("정답 번호(예: 4번) 또는 보기 문구: ").strip()
            answer = draft.get_answer_number(response)
            if answer is not None:
                break
            print("보기의 번호(1-4, 예: 4번)나 보기 문구를 입력해 주세요.")

        saved, message = self.save_quiz(Quiz(question, choices, answer, topic, explanation))
        print("퀴즈를 추가했습니다." if saved else message)

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈: {len(self.quizzes)}개")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. [{quiz.topic}] {quiz.question}")

    def show_score(self):
        if self.best_total == 0:
            print("아직 퀴즈 기록이 없습니다.")
            return
        print(f"최고 점수: {self.best_score}점 (정답 {self.best_correct}/{self.best_total})")

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()
        quiz_number = self._read_number("삭제할 퀴즈 번호: ", 1, len(self.quizzes))
        quiz = self.quizzes[quiz_number - 1]

        while True:
            confirmation = input(
                f"'{quiz.question}'을(를) 삭제할까요? (y/n): "
            ).strip().casefold()
            if confirmation in ("y", "yes", "예"):
                break
            if confirmation in ("n", "no", "아니요", "아니오", "취소"):
                print("삭제를 취소했습니다.")
                return
            print("삭제하려면 y 또는 예, 취소하려면 n 또는 아니요를 입력해 주세요.")

        deleted_quiz = self.quizzes.pop(quiz_number - 1)
        saved, message = self.save_data()
        if not saved:
            self.quizzes.insert(quiz_number - 1, deleted_quiz)
            print(message)
            return
        print("퀴즈를 삭제했습니다.")

    def save_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            raise TypeError("퀴즈는 Quiz 객체여야 합니다.")
        self.quizzes.append(quiz)
        return self.save_data()

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self._read_number("선택: ", 1, 6)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.delete_quiz()
                else:
                    saved, message = self.save_data()
                    print(message if not saved else "게임을 종료합니다.")
                    return
        except (KeyboardInterrupt, EOFError):
            _, message = self.save_data()
            print(f"\n입력이 중단되어 안전하게 종료합니다. {message}")

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
