import random
import tkinter as tk
from tkinter import messagebox, ttk

from quiz import Quiz


class QuizDashboard:
    COLORS = {
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
    TOPICS = ["전체", "Python", "JSON", "Git", "GitHub"]

    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.colors = self.COLORS
        self.nav_buttons = {}
        self.active_questions = []
        self.question_index = 0
        self.correct_count = 0
        self.selected_answer = None
        self.answer_checked = False
        self.choice_buttons = []
        self.root.title("Dev Command Quiz")
        self.root.geometry("1120x760")
        self.root.minsize(860, 640)
        self.root.configure(bg=self.colors["background"])
        self._configure_styles()
        self._build_shell()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.show_page("dashboard")

    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabel", background=self.colors["background"], foreground=self.colors["ink"], font=("Segoe UI", 10))
        style.configure("Muted.TLabel", foreground=self.colors["muted"], font=("Segoe UI", 10))
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("TCombobox", padding=7)

    def _build_shell(self):
        shell = tk.Frame(self.root, bg=self.colors["background"])
        shell.pack(fill="both", expand=True)
        sidebar = tk.Frame(shell, bg=self.colors["green_dark"], width=232)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=self.colors["green_dark"])
        brand.pack(fill="x", padx=20, pady=(24, 34))
        tk.Label(brand, text="Q", bg="#4bd2a0", fg=self.colors["green_dark"], width=2,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=(0, 10))
        brand_text = tk.Frame(brand, bg=self.colors["green_dark"])
        brand_text.pack(side="left")
        tk.Label(brand_text, text="DEV COMMAND", bg=self.colors["green_dark"], fg="#ffffff",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="QUIZ LAB  /  01", bg=self.colors["green_dark"], fg="#91b9a7",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(3, 0))
        tk.Label(sidebar, text="WORKSPACE", bg=self.colors["green_dark"], fg="#83a997",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 10))

        navigation = [
            ("dashboard", "⌂", "대시보드"),
            ("play", "▶", "퀴즈 풀기"),
            ("add", "+", "퀴즈 추가"),
            ("list", "≡", "퀴즈 목록"),
            ("scores", "★", "점수 기록"),
        ]
        for page, symbol, label in navigation:
            button = tk.Button(
                sidebar,
                text=f"{symbol}    {label}",
                anchor="w",
                padx=14,
                pady=11,
                borderwidth=0,
                relief="flat",
                bg=self.colors["green_dark"],
                fg="#c1d5ca",
                activeforeground="#ffffff",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                command=lambda selected_page=page: self.show_page(selected_page),
            )
            button.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[page] = button

        tk.Label(sidebar, text="PYTHON 3.10+  ·  STANDARD LIBRARY", bg=self.colors["green_dark"],
                 fg="#83a997", font=("Segoe UI", 7, "bold")).pack(side="bottom", anchor="w", padx=20, pady=18)
        tk.Button(sidebar, text="⏻    종료", anchor="w", padx=14, pady=10,
              borderwidth=0, relief="flat", bg="#21483b", fg="#f3d9d3",
              activebackground="#6b392f", activeforeground="#ffffff",
              font=("Segoe UI", 10, "bold"), cursor="hand2",
              command=self.close).pack(side="bottom", fill="x", padx=12, pady=(2, 8))

        main_area = tk.Frame(shell, bg=self.colors["background"])
        main_area.pack(side="left", fill="both", expand=True)
        topbar = tk.Frame(main_area, bg=self.colors["surface"], height=54,
                          highlightthickness=1, highlightbackground=self.colors["line"])
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="학습 작업실     /     명령어 기초", bg=self.colors["surface"],
                 fg=self.colors["muted"], font=("Segoe UI", 9)).pack(side="left", padx=26)
        tk.Label(topbar, text="●  로컬 모드", bg=self.colors["surface"], fg=self.colors["green"],
                 font=("Segoe UI", 9, "bold")).pack(side="right", padx=25)

        content = tk.Frame(main_area, bg=self.colors["background"])
        content.pack(fill="both", expand=True, padx=34, pady=28)
        self.status_text = tk.StringVar(value=self.game.load_message)
        self.status_label = tk.Label(content, textvariable=self.status_text, bg=self.colors["background"],
                                     fg=self.colors["muted"], font=("Segoe UI", 9), anchor="w")
        self.status_label.pack(side="bottom", fill="x", pady=(12, 0))
        self.page_body = tk.Frame(content, bg=self.colors["background"])
        self.page_body.pack(fill="both", expand=True)

    def _clear_page(self):
        for child in self.page_body.winfo_children():
            child.destroy()

    def _heading(self, eyebrow, title, description):
        heading = tk.Frame(self.page_body, bg=self.colors["background"])
        heading.pack(fill="x", pady=(0, 19))
        tk.Label(heading, text=eyebrow.upper(), bg=self.colors["background"], fg=self.colors["green"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(heading, text=title, bg=self.colors["background"], fg=self.colors["ink"],
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=(5, 3))
        tk.Label(heading, text=description, bg=self.colors["background"], fg=self.colors["muted"],
                 font=("Segoe UI", 10)).pack(anchor="w")

    def _button(self, parent, label, command, primary=False):
        background = self.colors["green"] if primary else self.colors["surface"]
        foreground = "#ffffff" if primary else self.colors["ink"]
        border = self.colors["green"] if primary else self.colors["line"]
        return tk.Button(parent, text=label, command=command, padx=16, pady=10,
                         bg=background, fg=foreground, activebackground=self.colors["green_dark"],
                         activeforeground="#ffffff", relief="flat", borderwidth=1,
                         highlightthickness=1, highlightbackground=border,
                         font=("Segoe UI", 10, "bold"), cursor="hand2")

    def show_page(self, page):
        self._clear_page()
        for page_name, button in self.nav_buttons.items():
            active = page_name == page
            button.configure(
                bg="#285544" if active else self.colors["green_dark"],
                fg="#ffffff" if active else "#c1d5ca",
                activebackground="#285544" if active else self.colors["green_dark"],
            )
        renderers = {
            "dashboard": self.render_dashboard,
            "play": self.render_quiz_setup,
            "add": self.render_add_quiz,
            "list": self.render_quiz_list,
            "scores": self.render_scores,
        }
        renderers[page]()

    def render_dashboard(self):
        self._heading("Learning console", "개발 명령어 퀴즈", "네 가지 도구의 개념과 명령을 문제로 익힙니다.")
        hero = tk.Frame(self.page_body, bg=self.colors["green_dark"], padx=24, pady=22)
        hero.pack(fill="x", pady=(0, 18))
        hero_copy = tk.Frame(hero, bg=self.colors["green_dark"])
        hero_copy.pack(side="left", fill="both", expand=True)
        tk.Label(hero_copy, text="TODAY'S PRACTICE", bg=self.colors["green_dark"], fg="#c9ded4",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(hero_copy, text="네 가지 도구, 하나씩 내 것으로", bg=self.colors["green_dark"], fg="#ffffff",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(8, 5))
        tk.Label(hero_copy, text="Python  ·  JSON  ·  Git  ·  GitHub  /  사지선다형", bg=self.colors["green_dark"],
                 fg="#c9ded4", font=("Segoe UI", 10)).pack(anchor="w")
        self._button(hero, "퀴즈 시작  →", lambda: self.show_page("play"), primary=True).pack(side="right", padx=(15, 0))

        topics = [
            ("01", "Python", "자료형 · 조건 · 반복", self.colors["green"]),
            ("02", "JSON", "읽기 · 쓰기 · 오류 처리", self.colors["coral"]),
            ("03", "Git", "기록 · 브랜치 · 병합", self.colors["teal"]),
            ("04", "GitHub", "원격 저장소 · 협업", self.colors["gold"]),
        ]
        topic_row = tk.Frame(self.page_body, bg=self.colors["background"])
        topic_row.pack(fill="x", pady=(0, 16))
        for column, (number, name, detail, accent) in enumerate(topics):
            card = tk.Frame(topic_row, bg=self.colors["surface"], padx=13, pady=13,
                            highlightthickness=1, highlightbackground=self.colors["line"])
            card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0))
            topic_row.grid_columnconfigure(column, weight=1, uniform="topic")
            tk.Label(card, text=number, bg=self.colors["surface"], fg=accent,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(card, text=name, bg=self.colors["surface"], fg=self.colors["ink"],
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 2))
            tk.Label(card, text=detail, bg=self.colors["surface"], fg=self.colors["muted"],
                     font=("Segoe UI", 8), wraplength=145, justify="left").pack(anchor="w")

        stats = tk.Frame(self.page_body, bg=self.colors["background"])
        stats.pack(fill="x")
        best_text = "기록 없음" if self.game.best_total == 0 else (
            f"{self.game.best_score}점  ·  {self.game.best_correct}/{self.game.best_total}"
        )
        self._stat_card(stats, "최고 점수", best_text, self.colors["green"]).pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        self._stat_card(stats, "문제 은행", f"{len(self.game.quizzes)}개 문제", self.colors["coral"]).pack(
            side="left", fill="x", expand=True, padx=(8, 0)
        )

    def _stat_card(self, parent, label, value, accent):
        card = tk.Frame(parent, bg=self.colors["surface"], padx=16, pady=13,
                        highlightthickness=1, highlightbackground=self.colors["line"])
        tk.Label(card, text=label, bg=self.colors["surface"], fg=self.colors["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(card, text=value, bg=self.colors["surface"], fg=accent,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(4, 0))
        return card

    def render_quiz_setup(self):
        self._heading("Practice", "퀴즈 풀기", "주제를 고르면 문제가 무작위 순서로 출제됩니다.")
        card = tk.Frame(self.page_body, bg=self.colors["surface"], padx=22, pady=22,
                        highlightthickness=1, highlightbackground=self.colors["line"])
        card.pack(fill="x")
        tk.Label(card, text="출제 주제", bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        topic_choice = ttk.Combobox(card, values=self.TOPICS, state="readonly", width=24)
        topic_choice.set("전체")
        topic_choice.pack(anchor="w", pady=(8, 18))
        tk.Label(card, text="문제 수", bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        count_choice = tk.Spinbox(card, from_=1, to=max(1, len(self.game.quizzes)), width=6,
                                  font=("Segoe UI", 10), relief="solid", borderwidth=1)
        count_choice.delete(0, "end")
        count_choice.insert(0, str(min(10, len(self.game.quizzes))))
        count_choice.pack(anchor="w", pady=(8, 18))

        def update_count_limit(event=None):
            topic = topic_choice.get()
            available_count = len([quiz for quiz in self.game.quizzes if topic == "전체" or quiz.topic == topic])
            count_choice.configure(to=max(1, available_count))
            count_choice.delete(0, "end")
            count_choice.insert(0, str(min(10, max(1, available_count))))

        topic_choice.bind("<<ComboboxSelected>>", update_count_limit)

        def begin():
            topic = topic_choice.get()
            available = [quiz for quiz in self.game.quizzes if topic == "전체" or quiz.topic == topic]
            if not available:
                messagebox.showinfo("퀴즈 없음", "선택한 주제에 등록된 문제가 없습니다.")
                return
            try:
                count = int(count_choice.get().strip())
            except ValueError:
                messagebox.showwarning("문제 수 확인", "문제 수는 숫자로 입력해 주세요.")
                return
            if not 1 <= count <= len(available):
                messagebox.showwarning("문제 수 확인", f"1부터 {len(available)} 사이로 입력해 주세요.")
                return
            self.active_questions = random.sample(available, count)
            self.question_index = 0
            self.correct_count = 0
            self.render_question()

        self._button(card, "시작하기  →", begin, primary=True).pack(anchor="w")

    def render_question(self):
        self._clear_page()
        quiz = self.active_questions[self.question_index]
        question_total = len(self.active_questions)
        self._heading(f"{quiz.topic}  /  QUESTION {self.question_index + 1:02d}",
                      f"문제 {self.question_index + 1}", "보기 하나를 마우스로 선택한 뒤 정답을 확인하세요.")
        progress = ttk.Progressbar(self.page_body, maximum=question_total, value=self.question_index + 1)
        progress.pack(fill="x", pady=(0, 15))
        question_card = tk.Frame(self.page_body, bg=self.colors["surface"], padx=22, pady=21,
                                 highlightthickness=1, highlightbackground=self.colors["line"])
        question_card.pack(fill="x", pady=(0, 12))
        tk.Label(question_card, text=quiz.question, bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 14, "bold"), justify="left", wraplength=740).pack(anchor="w")

        self.selected_answer = None
        self.answer_checked = False
        self.choice_buttons = []
        for answer_number, choice in enumerate(quiz.choices, start=1):
            button = tk.Button(
                self.page_body,
                text=f"{answer_number}     {choice}",
                anchor="w",
                padx=16,
                pady=12,
                bg=self.colors["surface"],
                fg=self.colors["ink"],
                activebackground=self.colors["green_light"],
                activeforeground=self.colors["ink"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.colors["line"],
                font=("Segoe UI", 10),
                cursor="hand2",
                command=lambda selected=answer_number: self.select_answer(selected),
            )
            button.pack(fill="x", pady=4)
            self.choice_buttons.append(button)

        self.feedback = tk.Label(self.page_body, text="", bg=self.colors["background"],
                                 fg=self.colors["muted"], font=("Segoe UI", 10, "bold"), anchor="w")
        self.feedback.pack(fill="x", pady=(8, 4))
        actions = tk.Frame(self.page_body, bg=self.colors["background"])
        actions.pack(fill="x", pady=(4, 0))
        self._button(actions, "대시보드", lambda: self.show_page("dashboard")).pack(side="left")
        self.answer_button = self._button(actions, "정답 확인", self.check_answer, primary=True)
        self.answer_button.pack(side="right")

    def select_answer(self, answer_number):
        if self.answer_checked:
            return
        self.selected_answer = answer_number
        for index, button in enumerate(self.choice_buttons, start=1):
            selected = index == answer_number
            button.configure(
                bg=self.colors["green_light"] if selected else self.colors["surface"],
                highlightbackground=self.colors["green"] if selected else self.colors["line"],
                font=("Segoe UI", 10, "bold" if selected else "normal"),
            )

    def check_answer(self):
        if self.answer_checked:
            self.question_index += 1
            if self.question_index >= len(self.active_questions):
                self.finish_quiz()
            else:
                self.render_question()
            return
        if self.selected_answer is None:
            messagebox.showinfo("보기 선택", "먼저 보기 하나를 선택해 주세요.")
            return

        quiz = self.active_questions[self.question_index]
        self.answer_checked = True
        for button in self.choice_buttons:
            button.configure(state="disabled")
        if quiz.is_correct(self.selected_answer):
            self.correct_count += 1
            self.feedback.configure(text="정답입니다.", fg=self.colors["green"])
        else:
            correct_choice = quiz.choices[quiz.answer - 1]
            self.feedback.configure(text=f"정답: {quiz.answer}. {correct_choice}", fg=self.colors["coral"])
        next_label = "결과 보기" if self.question_index + 1 == len(self.active_questions) else "다음 문제  →"
        self.answer_button.configure(text=next_label)

    def finish_quiz(self):
        is_new_best, save_message = self.game.record_game(self.correct_count, len(self.active_questions))
        self._clear_page()
        score = round(self.correct_count / len(self.active_questions) * 100)
        self._heading("Practice complete", "퀴즈 결과", "이번 학습 기록이 저장되었습니다.")
        card = tk.Frame(self.page_body, bg=self.colors["surface"], padx=28, pady=28,
                        highlightthickness=1, highlightbackground=self.colors["line"])
        card.pack(fill="x")
        tk.Label(card, text=f"{self.correct_count} / {len(self.active_questions)}", bg=self.colors["surface"],
                 fg=self.colors["green"], font=("Segoe UI", 32, "bold")).pack(anchor="w")
        tk.Label(card, text=f"정답률 {score}%", bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(7, 2))
        if not save_message.startswith("저장했습니다"):
            result_message = save_message
        else:
            result_message = "새로운 최고 점수입니다." if is_new_best else "기록을 저장했습니다."
        tk.Label(card, text=result_message, bg=self.colors["surface"], fg=self.colors["muted"],
                 font=("Segoe UI", 10), wraplength=740, justify="left").pack(anchor="w", pady=(2, 17))
        self._button(card, "대시보드로", lambda: self.show_page("dashboard"), primary=True).pack(anchor="w")

    def render_add_quiz(self):
        self._heading("Question bank", "퀴즈 추가", "문제와 보기 네 개를 입력하고 정답을 선택하세요.")
        form = tk.Frame(self.page_body, bg=self.colors["surface"], padx=20, pady=18,
                        highlightthickness=1, highlightbackground=self.colors["line"])
        form.pack(fill="both", expand=True)
        tk.Label(form, text="주제", bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        topic = ttk.Combobox(form, values=self.TOPICS[1:], state="readonly", width=22)
        topic.set("Python")
        topic.pack(anchor="w", pady=(5, 12))
        tk.Label(form, text="문제", bg=self.colors["surface"], fg=self.colors["ink"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        question_entry = tk.Entry(form, font=("Segoe UI", 10), relief="solid", borderwidth=1)
        question_entry.pack(fill="x", pady=(5, 12), ipady=7)

        choice_entries = []
        answer_value = tk.IntVar(value=1)
        for answer_number in range(1, 5):
            row = tk.Frame(form, bg=self.colors["surface"])
            row.pack(fill="x", pady=3)
            tk.Radiobutton(row, text=f"{answer_number}", variable=answer_value, value=answer_number,
                           bg=self.colors["surface"], fg=self.colors["ink"], selectcolor=self.colors["green_light"],
                           activebackground=self.colors["surface"], font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
            entry = tk.Entry(row, font=("Segoe UI", 10), relief="solid", borderwidth=1)
            entry.pack(side="left", fill="x", expand=True, ipady=5)
            choice_entries.append(entry)

        def save_question():
            question = question_entry.get().strip()
            choices = [entry.get().strip() for entry in choice_entries]
            if not question or not all(choices):
                messagebox.showwarning("입력 확인", "문제와 보기 네 개를 모두 입력해 주세요.")
                return
            try:
                quiz = Quiz(question, choices, answer_value.get(), topic.get())
            except ValueError as error:
                messagebox.showwarning("입력 확인", str(error))
                return
            saved, message = self.game.add_quiz(quiz)
            if not saved:
                messagebox.showerror("저장 오류", message)
                return
            self.status_text.set(message)
            self.show_page("list")

        self._button(form, "퀴즈 저장", save_question, primary=True).pack(anchor="w", pady=(14, 0))

    def render_quiz_list(self):
        self._heading("Question bank", "퀴즈 목록", f"저장된 문제 {len(self.game.quizzes)}개")
        if not self.game.quizzes:
            tk.Label(self.page_body, text="등록된 퀴즈가 없습니다.", bg=self.colors["background"],
                     fg=self.colors["muted"], font=("Segoe UI", 11)).pack(anchor="w")
            return

        table_frame = tk.Frame(self.page_body, bg=self.colors["surface"], padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        columns = ("number", "topic", "question", "answer")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("number", text="#")
        tree.heading("topic", text="주제")
        tree.heading("question", text="문제")
        tree.heading("answer", text="정답")
        tree.column("number", width=45, anchor="center", stretch=False)
        tree.column("topic", width=90, anchor="center", stretch=False)
        tree.column("question", width=480)
        tree.column("answer", width=160)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        details = tk.StringVar(value="문제를 선택하면 네 가지 보기가 표시됩니다.")
        tk.Label(self.page_body, textvariable=details, bg=self.colors["background"], fg=self.colors["muted"],
                 font=("Segoe UI", 9), justify="left", anchor="w", wraplength=780).pack(fill="x", pady=(9, 0))

        for number, quiz in enumerate(self.game.quizzes, start=1):
            tree.insert("", "end", iid=str(number - 1), values=(number, quiz.topic, quiz.question,
                                                                 quiz.choices[quiz.answer - 1]))

        def show_details(event=None):
            selection = tree.selection()
            if not selection:
                return
            quiz = self.game.quizzes[int(selection[0])]
            choices = "   ·   ".join(f"{index}. {choice}" for index, choice in enumerate(quiz.choices, start=1))
            details.set(choices)
        tree.bind("<<TreeviewSelect>>", show_details)

    def render_scores(self):
        self._heading("Progress", "점수 기록", "최고 점수와 최근 퀴즈 기록을 확인합니다.")
        best_text = "아직 퀴즈 기록이 없습니다." if self.game.best_total == 0 else (
            f"{self.game.best_score}점  ·  정답 {self.game.best_correct}/{self.game.best_total}"
        )
        self._stat_card(self.page_body, "BEST SCORE", best_text, self.colors["green"]).pack(fill="x", pady=(0, 15))
        if not self.game.history:
            tk.Label(self.page_body, text="플레이 기록이 여기에 표시됩니다.", bg=self.colors["background"],
                     fg=self.colors["muted"], font=("Segoe UI", 10)).pack(anchor="w")
            return

        history_frame = tk.Frame(self.page_body, bg=self.colors["surface"], padx=10, pady=10)
        history_frame.pack(fill="both", expand=True)
        columns = ("played_at", "result", "score")
        tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        tree.heading("played_at", text="날짜")
        tree.heading("result", text="정답 수")
        tree.heading("score", text="점수")
        tree.column("played_at", width=240)
        tree.column("result", width=120, anchor="center")
        tree.column("score", width=120, anchor="center")
        tree.pack(fill="both", expand=True)
        for entry in reversed(self.game.history):
            tree.insert("", "end", values=(entry.get("played_at", ""),
                                             f"{entry.get('correct', 0)}/{entry.get('total', 0)}",
                                             f"{entry.get('score', 0)}점"))

    def close(self):
        should_close = messagebox.askyesno(
            "프로그램 종료",
            "저장된 퀴즈와 점수를 유지하고 종료할까요?\n저장하지 않은 새 문제 입력은 사라집니다.",
        )
        if not should_close:
            return
        saved, message = self.game.save_data()
        if not saved:
            messagebox.showerror("저장 오류", message)
        self.root.destroy()


def launch_dashboard(game):
    root = tk.Tk()
    QuizDashboard(root, game)
    root.mainloop()
