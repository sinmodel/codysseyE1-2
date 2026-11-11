import random

from quiz import Quiz


def read_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("입력이 비어 있습니다. 다시 입력해 주세요.")


def read_number(prompt, minimum, maximum):
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


def play_quiz(game):
    if not game.quizzes:
        print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    maximum = len(game.quizzes)
    question_count = read_number(f"몇 문제를 풀까요? (1-{maximum}): ", 1, maximum)
    selected_quizzes = random.sample(game.quizzes, question_count)
    correct_count = 0

    for question_number, quiz in enumerate(selected_quizzes, start=1):
        print(f"\n[{question_number}/{question_count}] {quiz.topic}")
        print(quiz.question)
        for choice_number, choice in enumerate(quiz.choices, start=1):
            print(f"  {choice_number}. {choice}")

        while True:
            response = input("정답 번호 또는 보기 문구: ").strip()
            if quiz.get_answer_number(response) is not None:
                break
            print("보기의 번호(1-4)나 보기 문구를 입력해 주세요.")

        if quiz.is_correct(response):
            correct_count += 1
            print("정답입니다.")
        else:
            correct_choice = quiz.choices[quiz.answer - 1]
            print(f"아쉬워요. 정답은 {quiz.answer}. {correct_choice}입니다.")

    is_new_best, save_message = game.record_game(correct_count, question_count)
    score = round(correct_count / question_count * 100)
    print(f"\n결과: {question_count}문제 중 {correct_count}문제 정답 ({score}점)")
    if is_new_best:
        print("새로운 최고 점수입니다.")
    print(save_message)


def add_quiz(game):
    question = read_required("문제: ")
    choices = [read_required(f"선택지 {number}: ") for number in range(1, 5)]
    print("안내: 주제는 Python, JSON, Git, GitHub 중에서 입력해 주세요.")
    print("중복 문제 확인과 기존 문제 수정·삭제는 지원하지 않습니다.")
    topic = read_required("주제 (Python/JSON/Git/GitHub): ")
    draft = Quiz(question, choices, 1, topic)

    while True:
        response = input("정답 번호 또는 보기 문구: ").strip()
        answer = draft.get_answer_number(response)
        if answer is not None:
            break
        print("보기의 번호(1-4)나 보기 문구를 입력해 주세요.")

    saved, message = game.add_quiz(Quiz(question, choices, answer, topic))
    print("퀴즈를 추가했습니다." if saved else message)


def show_quizzes(game):
    if not game.quizzes:
        print("등록된 퀴즈가 없습니다.")
        return
    print(f"\n등록된 퀴즈: {len(game.quizzes)}개")
    for index, quiz in enumerate(game.quizzes, start=1):
        print(f"{index}. [{quiz.topic}] {quiz.question}")


def show_score(game):
    if game.best_total == 0:
        print("아직 퀴즈 기록이 없습니다.")
        return
    print(f"최고 점수: {game.best_score}점 (정답 {game.best_correct}/{game.best_total})")


def run_console(game):
    try:
        while True:
            print("\nPython · JSON · Git 퀴즈")
            print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 퀴즈 목록  4. 점수 확인  5. 종료")
            choice = read_number("선택: ", 1, 5)
            if choice == 1:
                play_quiz(game)
            elif choice == 2:
                add_quiz(game)
            elif choice == 3:
                show_quizzes(game)
            elif choice == 4:
                show_score(game)
            else:
                saved, message = game.save_data()
                print(message if not saved else "게임을 종료합니다.")
                return
    except (KeyboardInterrupt, EOFError):
        _, message = game.save_data()
        print(f"\n입력이 중단되어 안전하게 종료합니다. {message}")
