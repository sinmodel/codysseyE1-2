from console_ui import run_console
from game import QuizGame


def main():
    game = QuizGame()
    print(game.load_message)
    run_console(game)


if __name__ == "__main__":
    main()
