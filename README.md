# 기초 명령어 퀴즈 게임 1.0

Python, JSON, Git, GitHub의 기초 개념과 명령어를 연습하는 콘솔 퀴즈 게임입니다.
메뉴에서 숫자를 입력해 퀴즈를 풀고, 문제를 추가하거나 점수를 확인할 수 있습니다.

## 실행 방법

Python 3.10 이상에서 이 폴더로 이동한 뒤 실행합니다.

```powershell
py -3 main.py
```

## 기능

- 숫자 메뉴로 주제별 퀴즈 풀기, 문제 추가·삭제, 목록 확인, 최고 점수 확인 및 종료
- 삭제 대상과 확인 절차를 거친 뒤 저장 파일에 반영
- Python, JSON, Git, GitHub 기초 퀴즈 77개
- 정답과 함께 각 퀴즈의 해설 표시
- Python, JSON, Git, GitHub 중 주제를 선택하고 해당 주제의 문제를 무작위로 출제
- 출제할 문제 수 지정
- 잘못된 메뉴, 문제 수, 정답 입력을 안내하고 다시 입력
- 퀴즈와 점수 기록을 JSON 파일에 저장하고 다음 실행 때 불러오기
- 저장 파일이 없거나 손상된 경우 기본 퀴즈로 시작
- Ctrl+C 또는 입력 종료 시 저장을 시도하고 안전하게 종료

## 파일 구조

### 로컬 `version-1.0` 폴더

```text
version-1.0/
├── .git/                 # 로컬 Git 저장소 정보(숨김 폴더)
├── .vscode/
│   └── settings.json
├── __pycache__/          # Python 실행 시 생성되는 캐시
├── tests/
│   ├── __init__.py
│   └── test_game.py
├── .gitignore
├── README.md
├── console_ui.py
├── game.py
├── main.py
├── quiz.py
└── state.json            # 실행 중 생성되는 퀴즈·점수 데이터
```

### GitHub 저장소에 올라가는 구조

```text
version-1.0/
├── tests/
│   ├── __init__.py
│   └── test_game.py
├── .gitignore
├── README.md
├── console_ui.py
├── game.py
├── main.py
└── quiz.py
```

## 코드 구조

이 프로젝트는 최소 두 개의 클래스인 `Quiz`와 `QuizGame`으로 역할을 나눕니다. 퀴즈 하나의 데이터와 정답 판정은 `quiz.py`에서, 전체 게임 진행과 저장 관리는 `game.py`에서 담당합니다.

### `quiz.py` - 퀴즈 데이터와 정답 판정

- `Quiz` 클래스는 문제, 네 가지 선택지, 정답 번호, 주제, 해설을 한 퀴즈의 데이터로 관리합니다.
- 퀴즈를 만들 때 필수 항목이 비어 있지 않은지, 선택지가 네 개인지, 정답 번호가 1~4 범위인지 확인합니다.
- 입력한 정답이 번호·`4번` 형식·선택지 문구 중 하나인지 판별하고, 정답 여부를 확인합니다.
- `to_dict()`와 `from_dict()`로 퀴즈 데이터를 JSON 저장·불러오기에 사용할 수 있는 형태로 변환합니다.
- `DEFAULT_QUIZZES`에는 게임을 처음 시작할 때 제공하는 기본 퀴즈가 정의되어 있습니다.

### `game.py` - 게임 진행과 데이터 저장

- `QuizGame` 클래스는 퀴즈 목록, 최고 점수, 플레이 기록을 관리합니다.
- 메뉴를 표시하고 주제와 문제 수를 입력받아 무작위 퀴즈를 출제하며, 정답 확인과 해설 표시를 진행합니다.
- 퀴즈 추가·목록 확인·삭제와 점수 확인 기능을 처리하고, 잘못된 입력은 다시 입력하도록 안내합니다.
- `state.json`에서 저장 데이터를 불러오고, 퀴즈·최고 점수·플레이 기록을 JSON 형식으로 저장합니다. 저장 파일이 없거나 읽을 수 없을 때는 기본 퀴즈로 시작합니다.

- 메서드는 역할별로 나뉩니다: `_read_required()`·`_read_number()`는 입력 처리, `show_menu()`·`run()`·`play_quiz()`는 메뉴와 게임 진행, `add_quiz()`·`save_quiz()`·`show_quizzes()`·`delete_quiz()`·`show_score()`·`record_game()`은 퀴즈와 점수 관리, `load_data()`·`save_data()`는 파일 읽기와 저장을 담당합니다.

### `main.py`와 `console_ui.py` - 프로그램 실행 연결

- `main.py`의 `main()`은 `QuizGame`을 만들고 시작 안내를 출력한 뒤 `run_console()`을 호출하는 프로그램 진입점입니다.
- `console_ui.py`의 `run_console()`은 전달받은 게임 객체의 `run()`을 호출해 콘솔 실행을 연결합니다.

## 데이터 파일

### `state.json` 파일 위치와 생성

`state.json`은 `version-1.0` 폴더에 별도 파일로 생성됩니다. 게임을 처음 실행할 때 자동으로 만들어집니다. 별도의 `data` 폴더는 없지만, `state.json` 자체가 실제 퀴즈·점수 데이터 파일입니다.

이 파일은 추가한 퀴즈와 최고 점수 및 플레이 기록을 JSON 형식으로 저장하고, 한글이 깨지지 않도록 UTF-8 문자 인코딩을 사용합니다. 사용자 데이터 파일은 `.gitignore`에 의해 Git 저장소에는 포함되지 않습니다.

* 퀴즈 데이터와 최고 점수를 프로젝트 루트의 state.json에 저장하는  
  기능을 구현한다. (UTF-8 인코딩 권장)  
  관련 코드 (`version-1.0/game.py`, `QuizGame.__init__()` / `save_data()`):
  ```python
  self.state_path = Path(state_path) if state_path else Path(__file__).with_name("state.json")

  data = {
      "quizzes": [quiz.to_dict() for quiz in self.quizzes],
      "best_score": self.best_score,
      "best_correct": self.best_correct,
      "best_total": self.best_total,
      "history": self.history,
      "quiz_bank_version": self.quiz_bank_version,
  }
  with temporary_path.open("w", encoding="utf-8") as state_file:
      json.dump(data, state_file, ensure_ascii=False, indent=2)
  ```
* JSON 파일에서 데이터를 불러오는 기능을 구현한다.  
  관련 코드 (`version-1.0/game.py`, `QuizGame.load_data()`):
  ```python
  with self.state_path.open("r", encoding="utf-8") as state_file:
      data = json.load(state_file)
  ```
* 파일이 없는 경우(첫 실행) 기본 퀴즈 데이터를 사용한다.  
  관련 코드 (`version-1.0/game.py`, `QuizGame.__init__()` / `load_data()`):
  ```python
  self.quizzes = list(DEFAULT_QUIZZES)

  if not self.state_path.exists():
      self.load_message = "처음 실행입니다. 기본 퀴즈를 준비했습니다."
      self.save_data()
      return
  ```
* 파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우를 try/except로  
  처리한다.  
  관련 코드 (`version-1.0/game.py`, `QuizGame.load_data()`):
  ```python
  except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
      self.quizzes = list(DEFAULT_QUIZZES)
      self.best_score = 0
      self.history = []
      # 기본 데이터로 복구한 뒤 사용자에게 오류 내용을 안내
  ```
  쓰기 오류도 `save_data()`의 `except (OSError, TypeError, ValueError)`에서 처리한다.
* 최소 스키마 예시(데이터 형태 참고; 키 이름/구조는 일관되게 유지):  
  관련 코드 (`version-1.0/game.py`, `QuizGame.save_data()`):
  ```python
  data = {
      "quizzes": [quiz.to_dict() for quiz in self.quizzes],
      "best_score": self.best_score,
  }
  ```
* quizzes: 퀴즈 목록  
  관련 코드 (`version-1.0/quiz.py`, `Quiz.to_dict()`):
  ```python
  return {
      "question": self.question,
      "choices": self.choices,
      "answer": self.answer,
      "topic": self.topic,
      "explanation": self.explanation,
  }
  ```
* best_score: 최고 점수(또는 최고 정답 수 등)  
  관련 코드 (`version-1.0/game.py`, `QuizGame.save_data()` / `load_data()`):
  ```python
  "best_score": self.best_score
  self.best_score = self._valid_nonnegative_integer(data.get("best_score", 0))
  ```


## 보너스 문제 추가 :
#### (1) 랜덤 출제  
-퀴즈 풀기애서 문제 순서가 랜덤으로 섞여 나옵니다.  
-"기초 명령어 퀴즈 게임1.0" 에서 "메뉴 1. 퀴즈풀기"를 선택하면 4가지 주제 고르기를 할 수 있습니다.
-Python, Json, Git, GutHub 중에서 고르면 이에 관련된 문제가 랜덤방식으로 나옵니다.
-그 이후 문제 푸는 방식은 동일합니다.

#### (2) 문제 수 선택  
-퀴즈 풀기 시 몇 문제를 풀지 선택할 수 있습니다.  
-"메뉴 1. 퀴즈풀기"를 선택하면 "몇 문제를 선택할 것인가"에 문제수를 입력하면 됩니다.
-그 이후 문제 푸는 방식은 동일합니다.


묶음	커밋 번호	내용	브랜치
1	1325f97	Python 퀴즈 프로젝트 초기화	백업
1	1466ed7	대시보드와 4개 주제 퀴즈 추가	백업
1	7bb68b2	Python 실행 안내 수정	백업
2	b1d54ff	퀴즈 작성 제한 안내 추가	백업
2	0946f7d	version-1.0 프로젝트 파일 반영	main
2	050ccfc	Git 퀴즈 15개와 해설 추가	main
3	995e4ef	주제별 퀴즈 선택 기능 추가	feature
3	b539709	주제별 퀴즈 기능을 main에 병합	main
3	fabc433	주제 선택 사용법 문서화	main