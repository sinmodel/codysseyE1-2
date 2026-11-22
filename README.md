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

#### (3) 설명 기능 추가

- `Quiz`의 `explanation` 속성에 각 퀴즈의 해설을 저장합니다.
- 정답·오답 안내 뒤에 해설이 있으면 `해설: ...` 형식으로 표시합니다.
- 기본 퀴즈에서 해설이 비어 있던 항목만 보완하고, 기존 해설은 유지합니다. 저장된 `state.json`도 실행 시 비어 있는 기본 퀴즈 해설을 보완합니다.
- 퀴즈를 새로 추가할 때도 해설을 입력받아 함께 저장합니다. 힌트와 점수 차감 기능은 추가하지 않았습니다.
- [힌트 기능]을 대신하여 설명 기능을 넣었습니다.
----------------------------------------------------------------------------------
## 과제를 하면서 잘 알게된 사항들 :  
🟢본 과제의 핵심은 Python으로 데이터를 다루고, 프로그램을 구조화하며,   
file과 Git으로 작업을 관리하는 것입니다.  
🟢최근에, 윈도우 노트북에 필수적 설치는 Python과 Git이라고 볼 수 있는데,   
JSON은 별도 프로그램을 설치하지 않아도 파이썬에서 사용할 수 있고,   
GitHub는 웹사이트이므로 계정만 있으면 됩니다.

|항목|설치 사항|설명|
|---|------------|---|
|Python|Python 3 설치|-파이썬 코드를 실행합니다. 설치 화면에서 “Add Python to PATH”를 체크하세요.|
|JSON|별도 설치 없음|-데이터를 저장하는 형식입니다. Python에 내장된 json 기능을 사용합니다.|
|Git|Git for Windows 설치|-코드 변경 이력을 관리하고 GitHub와 주고받습니다.|
|GitHub|GitHub 계정 만들기|-코드를 온라인 저장소에 보관하는 서비스입니다.<br>-프로그램 설치는 필수가 아닙니다.<br>-이미 사용 중인 VS Code가 코드 편집기 역할을 하므로 그대로 사용하면 됩니다.<br>-GitHub Desktop을 추가 설치해 Git 작업을 버튼으로 할 수도 있지만, 필수는 아닙니다.|

🟢설치 후 확인하는 명령어 : 버전 번호가 나오면 기본 준비가 된 것입니다.  
VS Code 터미널에서,   
```
        python --version    
		git --version    
```
## Python 기초

🟢변수(變數)는 어떤 값들을 다시 사용하거나 바꿀 수 있도록 임시 저장하기 위한 목적으로 대입하기 위해 만든 명칭입니다.  

🟢다음과 같은 기본 자료형들이 있습니다.   
```
int(integer)는 정수,   
str(String) 은 문자열,    
bool(Boolean 논리형)은 참·거짓,   
list는 순서가 있는 여러 값의 모음,   
dict(Dictionary)는 이름표와 값이 짝을 이루는 데이터입니다.  
```
🟢if / elif(Else If) / else는 조건에 따라서 각각 3가지로 적용되는 일을 합니다.  
🟢for 는 정해진 항목이나 횟수만큼 반복 합니다.   
🟢while 은 조건이 참인 동안 반복 합니다.   

🟢함수는 재사용할 작업을 묶어 두는 코드입니다.   
  매개변수로 값을 받아 처리하고, return으로 결과를 돌려줍니다.  

## 클래스와 객체

🟢클래스(Class)는 비슷한 데이터와 기능을 모아 만든 설계도이고,     
🟢객체(Object)는 그 설계도로 만든 실제 대상입니다.  
🟢__init__(Initialize)은 객체가 만들어질 때 초기 실행되어 필요한 값을 설정합니다.     
🟢self는 지금 다루는 객체 자신을 가리킵니다.  
🟢속성(Attribute 또는 Property)은 객체가 가진 데이터이고,   
🟢메서드(Method)는 객체가 할 수 있는 동작입니다.  

## 파일의 입출력

파일을 열고, 내용을 읽거나 쓰고, 작업이 끝나면 닫는 방식으로 코딩을 합니다.   
🟢Python의 with open(...)은 파일을 안전하게 다루는 데 사용합니다.   
🟢Json은 데이터를 정해진 구조로 표현하는 형식입니다.   
   프로그램을 종료해도 데이터를 저장해 두거나 다른 프로그램과 주고받을 때 사용합니다.  
🟢try와 except는 오류가 발생할 수 있는 코드를 감싸고,   
   오류가 생겼을 때 프로그램이 적절히 대응하기 위해 사용합니다.  

## Git 기초  

🟢Git은 파일의 변경 이력을 기록하고,   
   여러 사람이 함께 작업할 수 있도록 하는 버전 관리 프로그램입니다.  
🟢init은 현재 폴더에서 Git 관리를 시작합니다.  

🟢add → commit → push 3단계 :   
```
add는 변경한 파일을 커밋할 준비 목록에 올리고   
commit은 그 시점의 변경사항을 기록하며,     
push는 그 기록들을 원격 저장소에 올립니다.    
```

|비교 항목|git add|git commit|git push|
|--------|--------------|-----------------|-----------------|
|핵심 역할|	저장할 변경 파일 선택|	선택한 파일들을 하나의 버전으로 확정|	확정된 버전을 원격 서버로 전송|   
|데이터 위치 변화|	작업 폴더 → 대기 공간(Staging)|	대기 공간 → 내 컴퓨터 저장소(Local)|	내 컴퓨터 저장소 → 원격 저장소(Remote)|     
|대표 명령어|git add . (모든 변경 파일 담기)|git commit -m "작업 설명"|git push origin main|   
|실수 시 되돌리기|git restore --staged .|git reset --soft HEAD~1|git revert 커밋ID|   


🟢git status : add나 commit을 실수했을 때 되돌리는 방법으로,   
                현재 내 파일들이 3단계 중 어디에 있는지 확인하는 명령어 입니다.  
```
🟢fetch와 pull과 clone :  
• fetch : 원격 저장소의 변경사항을 '확인만' 하기 위해 가져오는 것이고    
• pull  : 원격 저장소의 변경사항을 가져와 내 작업에 반영하는 것입니다.   
        그래서 pull = fetch + merige 입니다.     

🟢clone과 pull :  
  -같은 점 (방향): 둘 다 원격 저장소 → 내 컴퓨터 방향으로 데이터를 가져오는 명령어입니다.  
  -다른 점 (범위와 시점):  
• clone: 처음 시작할 때 전체를 통째로 1회 복제해 옵니다.  
• pull : 이후 작업하면서 변경사항만 골라서 수시로 가져와 합칩니다.  

🟢원격 저장소에서 가져온 후 내 작업을 다시 올리는 전체 협업 사이클    
        clone ---→ (수정 → add, commit, push) ---→ pull    	

🟢branch와 checkout :   
• branch : 기존 작업을 건드리지 않고 새 작업을 별도로 진행하는 명령어입니다.  
           다 만든 뒤 병합(merge) 하면 변경사항을 합칠 수 있습니다.  

• checkout : 브랜치나 특정 기록으로 이동할 때 사용합니다.  
             작업할 브랜치(작업 공간)를 바꾸거나, 수정한 파일을 이전 상태로 되돌릴 때   
             사용하는 명령어입니다.
```
### (1) checkout의 3가지 역할

1️⃣ 다른 브랜치로 이동하기    
```
   현재 작업 중인 가지(Branch)에서 다른 가지로 작업 위치를 옮깁니다.   
   예: git checkout main (메인 브랜치로 이동)
```      
2️⃣ 새 브랜치를 만들면서 동시에 이동하기 (-b 옵션)   
```
   새로운 기능 개발용 브랜치를 생성(branch)하고,   
   그곳으로 즉시 이동(checkout)하는   가장 많이 쓰이는 단축 명령어입니다.   
  	예: git checkout -b login (login 브랜치를 새로 만들고 바로 이동)   
```     
3️⃣ 수정한 파일 되돌리기 (변경사항 취소)   
```
   아직 add나 commit 하지 않고 수정만 한 파일을 마지막 커밋 시점으로 되돌립니다.   
  	예: git checkout -- index.html   
	(index.html 파일의 수정 내용을 버리고 원상복구)   
```
### (2) switch와 restore   

( checkout 하나에 너무 많은 기능이 섞여 있어 초보자들이 헷갈려 했기 때문에, )  
checkout 대신으로 Git에서는 최근에 switch는 브랜치 이동에, restore는 파일 복구에 사용하도록 권장하고 있습니다.      

|핵심 역할|최신 권장 명령어|기존 checkout 명령어|
|-----|-----|-----|
|다른 브랜치로 이동|git switch 브랜치명|git checkout 브랜치명|  
|새 브랜치 생성 후 이동 (c = create)|git switch -c 새브랜치|git checkout -b 새브랜치|   
|수정한 파일 내용 원상복구|git restore 파일명|git checkout -- 파일명|  


### (3) pull을 할 때 다른 사람의 코드와 내 코드가 겹쳐서 생기는 충돌(Conflict) 대처법 :   
-Git에서 같은 부분을 서로 다르게 수정했을 때 생기는 문제로서,<br> 충돌 난 파일을 직접 정리한 뒤 Git에 해결했다고 알려주면 됩니다.   
-먼저, 충돌 파일을 확인합니다. : 
```
git status
```   
-파일을 열면 보통 다음과 같은 에러표시가 나오는데,   
-두 변경 중 하나를 선택하거나 필요한 내용을 합쳐서,<br> <<<<<<<, =======, >>>>>>> 표시를 모두 지웁니다.   

### 에러표시 예시:    
`<<<<<<< HEAD` (내 변경), `=======` (구분선), `>>>>>>> 브랜치명` (가져온 변경의 끝)   

### 충돌 표시 줄을 모두 지운 뒤 파일에 남길 결과 예시:    
```python   
print("내 변경")   
```
### 가져온 코드만 선택한 경우 :   
```python   
print("가져온 변경")   
```
### 두 변경을 합쳐서 모두 사용한 경우 :   
```python   
print("내 변경")   
print("가져온 변경")   
```
-그 다음으로, Python 문법과 동작을 확인합니다. : 
```
python -m py_compile 파일명.py   
```
-프로젝트에 테스트가 있으면 테스트도 실행합니다.   
-그리고, 해결한 파일을 스테이징합니다. : 
```
git add 파일명.py
```   
-마지막으로 다음 4가지 중에 선택 실행하여, 작업을 마무리합니다.   
-일반적인 merge라면 : 
```
git commit   
```
-rebase 중이라면    : 
```
git rebase --continue   
```
-어떻게 합칠지 모르겠거나 아직 정리하지 않은 상태라면, 작업을 중단합니다. : 
```
git merge --abort   
```   
-rebase 중일 때는 
```
git rebase --abort를 사용하여 작업을 중단합니다.   
```   
-주의할 점은, 파일을 정리하기 전에는 무작정 git reset이나 변경사항 삭제 명령을     
 실행하지 않는 게 안전합니다.    

 명령어 clone과 pull의 실습 :

처음 복제할 때
git clone <저장소 주소> [새 폴더 이름]
예: git clone https://github.com/sinmodel/codysseyE1-2.git clone-practice

기존 저장소에 새 변경을 가져올 때
git pull <원격 이름> <브랜치 이름>
예: git pull origin main

origin은 원격 저장소 별칭, main은 브랜치 이름입니다.

전체 브랜치의 커밋 이력을 나타내는 명령어 :
현재 작업장인 로컬 저장소에서,
다음 명령어를 실행합니다.
```
git log --oneline --graph --decorate --all

git --no-pager log --oneline --graph --decorate --all -n 15
```
프로젝트 관련 커밋 12개 (자동 생성된 세션 기록 제외)

| 묶음 | 커밋 번호 | 내용 | 브랜치 |
|---|---|---|---|
| 1 | `1325f97` | Python 퀴즈 프로젝트 초기화 | `backup-before-replacement-20261121` |
| 1 | `1466ed7` | 대시보드와 4개 주제 퀴즈 추가 | `backup-before-replacement-20261121` |
| 1 | `7bb68b2` | Python 실행 안내 수정 | `backup-before-replacement-20261121` |
| 2 | `b1d54ff` | 퀴즈 작성 제한 안내 추가 | `backup-before-replacement-20261121` |
| 2 | `0946f7d` | version-1.0 프로젝트 파일 반영 | `main` |
| 2 | `050ccfc` | Git 퀴즈 15개와 해설 추가 | `main` |
| 3 | `995e4ef` | 주제별 퀴즈 선택 기능 추가 | `feature/topic-based-quiz` |
| 3 | `b539709` | 주제별 퀴즈 기능을 main에 병합 | `main` |
| 3 | `fabc433` | 주제 선택 사용법 문서화 | `main` |
| 4 | `8c73ead` | README 설명 보완 | `main` |
| 4 | `d2fe63c` | clone/pull 실습 파일 추가 | `main` |
| 4 | `0b3dab8` | 기본 퀴즈 설명 추가 | `main` |