import os
import sys
import unicodedata


PANEL_CONTENT_WIDTH = 54


def display_width(text):
    return sum(
        2 if unicodedata.east_asian_width(character) in {"F", "W"} else 1
        for character in text
    )


def panel_row(left_text="", right_text=""):
    gap = PANEL_CONTENT_WIDTH - display_width(left_text) - display_width(right_text)
    return f"│ {left_text}{' ' * max(1, gap)}{right_text} │"


def colorize(text, color_code):
    if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
        return text
    return f"\033[{color_code}m{text}\033[0m"


def read_number(prompt, minimum, maximum):
    while True:
        raw_value = input(prompt).strip()

        if not raw_value:
            print("입력이 비어 있습니다. 다시 입력해 주세요.")
            continue

        try:
            number = int(raw_value)
        except ValueError:
            print("숫자로 입력해 주세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")


def show_menu():
    line = "─" * (PANEL_CONTENT_WIDTH + 2)
    print()
    print(colorize(f"┌{line}┐", "38;5;42"))
    print(colorize(panel_row("DEV COMMAND QUIZ", "v0.1"), "1;38;5;42"))
    print(panel_row("Python  /  JSON  /  Git  /  GitHub"))
    print(colorize(f"├{line}┤", "38;5;42"))
    print(panel_row())
    print(panel_row("01   퀴즈 풀기", "개념과 명령어 익히기"))
    print(panel_row("02   퀴즈 추가", "나만의 문제 등록"))
    print(panel_row("03   퀴즈 목록", "등록된 문제 살펴보기"))
    print(panel_row("04   최고 점수", "나의 기록 확인"))
    print(panel_row())
    print(colorize(f"├{line}┤", "38;5;42"))
    print(panel_row("05   종료"))
    print(colorize(f"└{line}┘", "38;5;42"))


def run_console():
    try:
        while True:
            show_menu()
            choice = read_number("선택: ", 1, 5)

            if choice == 5:
                print("게임을 종료합니다.")
                break

            feature_names = {
                1: "퀴즈 풀기",
                2: "퀴즈 추가",
                3: "퀴즈 목록",
                4: "최고 점수",
            }
            print(f"{feature_names[choice]} 기능을 다음 개발 단계에서 연결합니다.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 안전하게 종료합니다.")


def launch_gui():
    import tkinter as tk
    from tkinter import ttk

    colors = {
        "background": "#f2f5f0",
        "surface": "#ffffff",
        "ink": "#1c2b25",
        "muted": "#68776f",
        "green": "#176a4b",
        "green_dark": "#143a30",
        "green_light": "#e3f2e9",
        "line": "#dce4dc",
        "coral": "#c64d38",
        "gold": "#c28a24",
        "teal": "#287b83",
    }

    root = tk.Tk()
    root.title("Dev Command Quiz")
    root.geometry("1040x700")
    root.minsize(820, 600)
    root.configure(bg=colors["background"])

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background=colors["background"])
    style.configure("Card.TFrame", background=colors["surface"])
    style.configure("TLabel", background=colors["background"], foreground=colors["ink"], font=("Segoe UI", 10))
    style.configure("Muted.TLabel", foreground=colors["muted"], font=("Segoe UI", 10))
    style.configure("Eyebrow.TLabel", foreground=colors["green"], font=("Segoe UI", 9, "bold"))
    style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
    style.configure("CardTitle.TLabel", background=colors["surface"], font=("Segoe UI", 12, "bold"))
    style.configure("CardNote.TLabel", background=colors["surface"], foreground=colors["muted"], font=("Segoe UI", 9))
    style.configure("Hero.TLabel", background=colors["green_dark"], foreground="#ffffff", font=("Segoe UI", 21, "bold"))
    style.configure("HeroNote.TLabel", background=colors["green_dark"], foreground="#c9ded4", font=("Segoe UI", 10))
    style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 11))
    style.map("Primary.TButton", background=[("!disabled", colors["green"]), ("active", "#10573d")], foreground=[("!disabled", "#ffffff")])

    shell = tk.Frame(root, bg=colors["background"])
    shell.pack(fill="both", expand=True)

    sidebar = tk.Frame(shell, bg=colors["green_dark"], width=224)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    brand = tk.Frame(sidebar, bg=colors["green_dark"])
    brand.pack(fill="x", padx=20, pady=(24, 34))
    tk.Label(brand, text="Q", bg="#4bd2a0", fg=colors["green_dark"], width=2, height=1,
             font=("Segoe UI", 18, "bold")).pack(side="left", padx=(0, 10))
    brand_text = tk.Frame(brand, bg=colors["green_dark"])
    brand_text.pack(side="left")
    tk.Label(brand_text, text="DEV COMMAND", bg=colors["green_dark"], fg="#ffffff",
             font=("Segoe UI", 11, "bold")).pack(anchor="w")
    tk.Label(brand_text, text="QUIZ LAB  /  01", bg=colors["green_dark"], fg="#91b9a7",
             font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(3, 0))

    tk.Label(sidebar, text="WORKSPACE", bg=colors["green_dark"], fg="#83a997",
             font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 10))

    nav_items = [
        ("⌂", "대시보드", "학습 현황과 퀴즈 주제를 확인합니다."),
        ("▶", "퀴즈 풀기", "Python, JSON, Git, GitHub 문제를 풀어 봅니다."),
        ("+", "퀴즈 추가", "새로운 사지선다형 문제를 등록합니다."),
        ("≡", "퀴즈 목록", "등록된 문제와 보기를 살펴봅니다."),
        ("★", "점수 기록", "최고 점수와 학습 기록을 확인합니다."),
    ]
    nav_buttons = []
    page_note = tk.StringVar(value=nav_items[0][2])

    def select_nav(index):
        for button_index, button in enumerate(nav_buttons):
            active = button_index == index
            button.configure(
                bg="#285544" if active else colors["green_dark"],
                fg="#ffffff" if active else "#c1d5ca",
                activebackground="#285544",
            )
        page_note.set(nav_items[index][2])

    for index, (symbol, label, _) in enumerate(nav_items):
        button = tk.Button(
            sidebar,
            text=f"{symbol}    {label}",
            anchor="w",
            padx=14,
            pady=11,
            borderwidth=0,
            relief="flat",
            bg=colors["green_dark"],
            fg="#c1d5ca",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=lambda selected=index: select_nav(selected),
        )
        button.pack(fill="x", padx=12, pady=2)
        nav_buttons.append(button)

    tk.Label(sidebar, text="PYTHON 3.10+  ·  STANDARD LIBRARY", bg=colors["green_dark"],
             fg="#83a997", font=("Segoe UI", 7, "bold")).pack(side="bottom", anchor="w", padx=20, pady=18)
    select_nav(0)

    main_area = tk.Frame(shell, bg=colors["background"])
    main_area.pack(side="left", fill="both", expand=True)

    topbar = tk.Frame(main_area, bg=colors["surface"], height=54,
                      highlightthickness=1, highlightbackground=colors["line"])
    topbar.pack(fill="x")
    topbar.pack_propagate(False)
    tk.Label(topbar, text="학습 작업실     /     명령어 기초", bg=colors["surface"],
             fg=colors["muted"], font=("Segoe UI", 9)).pack(side="left", padx=26)
    tk.Label(topbar, text="●  로컬 모드", bg=colors["surface"], fg=colors["green"],
             font=("Segoe UI", 9, "bold")).pack(side="right", padx=25)

    content = tk.Frame(main_area, bg=colors["background"])
    content.pack(fill="both", expand=True, padx=34, pady=28)

    heading = ttk.Frame(content)
    heading.pack(fill="x", pady=(0, 19))
    ttk.Label(heading, text="LEARNING CONSOLE", style="Eyebrow.TLabel").pack(anchor="w")
    ttk.Label(heading, text="개발 명령어 퀴즈", style="Title.TLabel").pack(anchor="w", pady=(5, 3))
    ttk.Label(heading, textvariable=page_note, style="Muted.TLabel").pack(anchor="w")

    hero = tk.Frame(content, bg=colors["green_dark"], padx=26, pady=22)
    hero.pack(fill="x", pady=(0, 18))
    hero_text = tk.Frame(hero, bg=colors["green_dark"])
    hero_text.pack(side="left", fill="both", expand=True)
    ttk.Label(hero_text, text="TODAY'S PRACTICE", style="HeroNote.TLabel").pack(anchor="w")
    ttk.Label(hero_text, text="네 가지 도구, 하나씩 내 것으로", style="Hero.TLabel").pack(anchor="w", pady=(8, 5))
    ttk.Label(hero_text, text="Python · JSON · Git · GitHub  /  사지선다형", style="HeroNote.TLabel").pack(anchor="w")
    status_text = tk.StringVar(value="퀴즈 기능을 연결하는 중입니다.")

    def show_coming_soon():
        status_text.set("선택한 기능은 다음 구현 단계에서 연결합니다.")

    ttk.Button(hero, text="퀴즈 시작  →", style="Primary.TButton", command=show_coming_soon).pack(side="right", padx=(16, 0))

    overview = tk.Frame(content, bg=colors["background"])
    overview.pack(fill="x", pady=(0, 15))
    topics = [
        ("01", "Python", "자료형 · 조건 · 반복", colors["green"]),
        ("02", "JSON", "읽기 · 쓰기 · 오류 처리", colors["coral"]),
        ("03", "Git", "기록 · 브랜치 · 병합", colors["teal"]),
        ("04", "GitHub", "원격 저장소 · 협업", colors["gold"]),
    ]
    for column, (number, name, detail, accent) in enumerate(topics):
        card = tk.Frame(overview, bg=colors["surface"], padx=13, pady=13,
                        highlightthickness=1, highlightbackground=colors["line"])
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 7, 0))
        overview.grid_columnconfigure(column, weight=1, uniform="topic")
        tk.Label(card, text=number, bg=colors["surface"], fg=accent,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(card, text=name, style="CardTitle.TLabel").pack(anchor="w", pady=(5, 2))
        ttk.Label(card, text=detail, style="CardNote.TLabel", wraplength=160).pack(anchor="w")

    score_row = tk.Frame(content, bg=colors["background"])
    score_row.pack(fill="x")
    score_card = tk.Frame(score_row, bg=colors["surface"], padx=16, pady=13,
                          highlightthickness=1, highlightbackground=colors["line"])
    score_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
    tk.Label(score_card, text="최고 점수", bg=colors["surface"], fg=colors["muted"],
             font=("Segoe UI", 9)).pack(anchor="w")
    tk.Label(score_card, text="아직 기록 없음", bg=colors["surface"], fg=colors["ink"],
             font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(4, 0))
    progress_card = tk.Frame(score_row, bg=colors["surface"], padx=16, pady=13,
                             highlightthickness=1, highlightbackground=colors["line"])
    progress_card.pack(side="left", fill="x", expand=True, padx=(8, 0))
    tk.Label(progress_card, text="문제 은행", bg=colors["surface"], fg=colors["muted"],
             font=("Segoe UI", 9)).pack(anchor="w")
    tk.Label(progress_card, text="4개 학습 분야", bg=colors["surface"], fg=colors["ink"],
             font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(4, 0))

    tk.Label(content, textvariable=status_text, bg=colors["background"], fg=colors["muted"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(13, 0))
    root.mainloop()


def main():
    import argparse
    from game import QuizGame

    parser = argparse.ArgumentParser(description="Python, JSON, Git, GitHub 명령어 퀴즈")
    parser.add_argument("--cli", action="store_true", help="콘솔 메뉴로 실행")
    arguments = parser.parse_args()
    game = QuizGame()

    if arguments.cli:
        from console_ui import run_console

        run_console(game)
        return

    try:
        from desktop_ui import launch_dashboard

        launch_dashboard(game)
    except ModuleNotFoundError as error:
        if error.name != "tkinter":
            raise
        print("Tkinter를 사용할 수 없어 콘솔 모드로 시작합니다.")
        from console_ui import run_console

        run_console(game)


if __name__ == "__main__":
    main()