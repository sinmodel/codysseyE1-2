class Quiz:
    def __init__(self, question, choices, answer, topic="Python"):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용은 비어 있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("퀴즈 선택지는 정확히 4개여야 합니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지 내용은 비어 있을 수 없습니다.")
        if not isinstance(answer, int) or isinstance(answer, bool) or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1부터 4 사이여야 합니다.")
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("주제 이름은 비어 있을 수 없습니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.topic = topic.strip()

    def get_answer_number(self, response):
        answer_text = str(response).strip()
        if not answer_text:
            return None

        try:
            answer_number = int(answer_text)
        except ValueError:
            matches = [
                index
                for index, choice in enumerate(self.choices, start=1)
                if answer_text.casefold() == choice.casefold()
            ]
            return matches[0] if len(matches) == 1 else None

        return answer_number if 1 <= answer_number <= 4 else None

    def is_correct(self, response):
        return self.get_answer_number(response) == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "topic": self.topic,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            topic=data.get("topic", "Python"),
        )


DEFAULT_QUIZZES = [
    Quiz("Python에서 정수 자료형의 이름은 무엇인가요?", ["int", "str", "bool", "list"], 1, "Python"),
    Quiz("문자열 자료형을 나타내는 이름은 무엇인가요?", ["int", "str", "dict", "bool"], 2, "Python"),
    Quiz("참 또는 거짓을 나타내는 자료형은 무엇인가요?", ["list", "str", "bool", "dict"], 3, "Python"),
    Quiz("여러 값을 순서대로 담는 자료형은 무엇인가요?", ["bool", "int", "list", "None"], 3, "Python"),
    Quiz("이름표와 값의 쌍으로 데이터를 담는 자료형은 무엇인가요?", ["dict", "str", "int", "bool"], 1, "Python"),
    Quiz("조건이 참인지에 따라 코드를 나누는 문법은 무엇인가요?", ["for", "if", "def", "import"], 2, "Python"),
    Quiz("목록의 각 항목을 차례로 처리할 때 주로 쓰는 반복문은 무엇인가요?", ["for", "try", "class", "return"], 1, "Python"),
    Quiz("함수에서 호출한 곳으로 결과를 돌려주는 키워드는 무엇인가요?", ["input", "print", "return", "while"], 3, "Python"),
    Quiz("JSON은 주로 어떤 용도로 쓰이는 데이터 형식인가요?", ["화면 색상 지정", "데이터 저장과 교환", "Python 설치", "브랜치 병합"], 2, "JSON"),
    Quiz("Python의 json.load()는 어떤 작업을 하나요?", ["JSON 파일을 읽어 Python 데이터로 변환", "JSON 파일에 쓰기", "폴더 만들기", "Git 커밋 생성"], 1, "JSON"),
    Quiz("Python의 json.dump()는 어떤 작업을 하나요?", ["JSON 파일을 삭제", "Python 데이터를 JSON으로 기록", "파일 이름 변경", "문자열을 정수로 변환"], 2, "JSON"),
    Quiz("파일을 열 때 with를 사용하면 좋은 점은 무엇인가요?", ["파일이 자동으로 닫힘", "인터넷에 업로드됨", "오류가 모두 사라짐", "파일이 암호화됨"], 1, "JSON"),
    Quiz("예외가 발생했을 때 처리하는 구문은 무엇인가요?", ["if/else", "try/except", "for/in", "def/return"], 2, "Python"),
    Quiz("변경한 파일을 다음 커밋에 포함할 준비 목록에 올리는 명령은 무엇인가요?", ["git push", "git add", "git clone", "git pull"], 2, "Git"),
    Quiz("준비된 변경사항을 로컬 저장소의 이력으로 기록하는 명령은 무엇인가요?", ["git commit", "git pull", "git status", "git clone"], 1, "Git"),
    Quiz("로컬 커밋을 원격 저장소에 올리는 명령은 무엇인가요?", ["git add", "git checkout", "git push", "git init"], 3, "Git"),
    Quiz("원격 저장소의 변경사항을 가져와 현재 브랜치에 반영하는 명령은 무엇인가요?", ["git pull", "git clone", "git commit", "git init"], 1, "Git"),
    Quiz("원격 저장소를 새 폴더에 복제할 때 사용하는 명령은 무엇인가요?", ["git merge", "git clone", "git add", "git status"], 2, "Git"),
    Quiz("새 브랜치로 이동하거나 브랜치를 바꿀 때 사용하는 명령은 무엇인가요?", ["git push", "git add", "git checkout", "git commit"], 3, "Git"),
    Quiz("두 브랜치의 작업을 합칠 때 사용하는 명령은 무엇인가요?", ["git merge", "git init", "git clone", "git status"], 1, "Git"),
    Quiz("Git과 GitHub의 관계를 가장 잘 설명한 것은 무엇인가요?", ["같은 프로그램의 두 이름", "Git은 버전 관리 도구, GitHub는 원격 저장소 서비스", "GitHub가 Git을 대체함", "Git은 웹 브라우저"], 2, "GitHub"),
    Quiz("GitHub의 원격 저장소 주소를 복사해 내 컴퓨터에 처음 가져오는 작업은 무엇인가요?", ["commit", "clone", "push", "add"], 2, "GitHub"),
    Quiz("변수는 어떤 역할을 하나요?", ["값을 담아 이름으로 다시 사용하게 한다", "프로그램을 자동으로 인터넷에 올린다", "모든 오류를 없앤다", "파일을 반드시 삭제한다"], 1, "Python"),
    Quiz("조건이 참인 동안 반복을 계속하는 문법은 무엇인가요?", ["if", "while", "class", "import"], 2, "Python"),
    Quiz("앞선 if 조건이 거짓일 때 다음 조건을 검사하는 키워드는 무엇인가요?", ["elif", "return", "break", "with"], 1, "Python"),
    Quiz("함수를 새로 정의할 때 사용하는 키워드는 무엇인가요?", ["class", "try", "def", "yield"], 3, "Python"),
    Quiz("함수를 정의할 때 괄호 안에 적어 함수가 받을 값을 나타내는 것은 무엇인가요?", ["매개변수", "반환값", "주석", "모듈"], 1, "Python"),
    Quiz("객체를 만들 때 초기 속성을 설정하는 특별한 메서드는 무엇인가요?", ["__main__", "__name__", "__init__", "__file__"], 3, "Python"),
    Quiz("인스턴스 메서드 안에서 현재 객체를 가리키는 관례적인 첫 매개변수는 무엇인가요?", ["this", "self", "object", "current"], 2, "Python"),
    Quiz("JSON 객체의 자료 구조와 가장 가까운 Python 자료형은 무엇인가요?", ["dict", "tuple", "set", "bytes"], 1, "JSON"),
    Quiz("JSON 배열을 Python으로 읽었을 때 보통 어떤 자료형이 되나요?", ["list", "set", "bool", "int"], 1, "JSON"),
    Quiz("파일이 아닌 문자열에 들어 있는 JSON을 Python 값으로 바꾸는 함수는 무엇인가요?", ["json.load", "json.loads", "json.dump", "json.dumps"], 2, "JSON"),
    Quiz("Python 데이터를 JSON 문자열로 바꾸는 함수는 무엇인가요?", ["json.loads", "json.load", "json.dumps", "json.read"], 3, "JSON"),
    Quiz("JSON 문자열에서 객체의 키를 감쌀 때 사용하는 따옴표는 무엇인가요?", ["작은따옴표", "큰따옴표", "역따옴표", "따옴표 없이 작성"], 2, "JSON"),
    Quiz("한글이 포함된 JSON을 사람이 읽기 쉽게 저장할 때 json.dump에 주는 설정은 무엇인가요?", ["ensure_ascii=False", "ensure_ascii=True", "encoding=None", "indent=0"], 1, "JSON"),
    Quiz("json.dump(..., indent=2)에서 indent 옵션의 역할은 무엇인가요?", ["JSON 내용을 들여쓰기해 읽기 좋게 표시", "파일을 두 개로 나눔", "문자열을 두 번 저장", "정답 번호를 바꿈"], 1, "JSON"),
    Quiz("JSON 문법이 잘못되어 파싱할 수 없을 때 json 모듈이 발생시키는 예외는 무엇인가요?", ["IndexError", "JSONDecodeError", "NameError", "StopIteration"], 2, "JSON"),
    Quiz("파일을 읽으려 했지만 파일 자체가 없을 때 주로 처리할 예외는 무엇인가요?", ["FileNotFoundError", "KeyError", "ZeroDivisionError", "AssertionError"], 1, "JSON"),
    Quiz("프로그램을 종료한 뒤에도 사용자 퀴즈와 점수를 유지하는 방법은 무엇인가요?", ["변수에만 보관", "파일에 저장하고 다음 실행 때 읽기", "화면에 출력", "함수 이름 변경"], 2, "JSON"),
    Quiz("과제에서 state.json을 두도록 지정한 위치는 어디인가요?", ["프로젝트 루트 폴더", "Python 설치 폴더", "바탕 화면", "Git 설치 폴더"], 1, "JSON"),
    Quiz("Git 저장소로 관리할 폴더에서 처음 실행해 저장소를 만드는 명령은 무엇인가요?", ["git init", "git status", "git log", "git diff"], 1, "Git"),
    Quiz("현재 변경된 파일과 스테이징 상태를 확인하는 명령은 무엇인가요?", ["git status", "git push", "git merge", "git clone"], 1, "Git"),
    Quiz("아직 커밋하지 않은 코드 변경 내용을 자세히 비교하는 명령은 무엇인가요?", ["git diff", "git init", "git pull", "git branch"], 1, "Git"),
    Quiz("짧은 한 줄 형식으로 커밋 기록을 확인하는 명령은 무엇인가요?", ["git log --oneline", "git add --short", "git push --history", "git pull --log"], 1, "Git"),
    Quiz("새 기능을 별도 브랜치에서 바로 만들고 이동하는 명령은 무엇인가요?", ["git checkout -b feature-name", "git status feature-name", "git push -b feature-name", "git clone feature-name"], 1, "Git"),
    Quiz("작업 중인 브랜치를 main 브랜치에 합치려면 보통 어떤 순서로 하나요?", ["main으로 이동한 뒤 git merge 작업브랜치", "작업브랜치에서 git init main", "main에서 git clone 작업브랜치", "git add main 작업브랜치"], 1, "Git"),
    Quiz("git add를 했지만 아직 git commit을 하지 않은 상태를 가장 잘 설명한 것은 무엇인가요?", ["변경사항이 GitHub에 공개됨", "다음 커밋에 포함할 준비가 됨", "변경사항이 삭제됨", "브랜치가 자동 병합됨"], 2, "Git"),
    Quiz("GitHub에 올리기 전에 커밋 메시지를 작성하는 이유는 무엇인가요?", ["변경 기록의 목적을 남기기 위해", "Python을 설치하기 위해", "파일 권한을 바꾸기 위해", "브랜치 수를 줄이기 위해"], 1, "Git"),
    Quiz("GitHub 저장소는 주로 무엇을 제공하나요?", ["Git 저장소를 온라인에 보관하고 협업하는 공간", "Python 문법을 실행하는 인터프리터", "JSON 파일 전용 편집기", "컴퓨터의 로컬 폴더"], 1, "GitHub"),
    Quiz("로컬 커밋을 GitHub 원격 저장소에 반영할 때 사용하는 Git 명령은 무엇인가요?", ["git push", "git status", "git init", "git diff"], 1, "GitHub"),
    Quiz("GitHub에서 프로젝트 첫 화면에 설명을 보여주는 대표 문서 파일은 무엇인가요?", ["README.md", "state.json", "main.exe", "password.txt"], 1, "GitHub"),
    Quiz("저장소에서 공개적으로 공유할 파일과 올리지 않을 파일을 정하는 데 쓰는 파일은 무엇인가요?", [".gitignore", "requirements.lock", "index.html", "LICENSE.tmp"], 1, "GitHub"),
    Quiz("GitHub의 Pull Request는 보통 어떤 목적으로 사용하나요?", ["변경사항을 검토하고 다른 브랜치에 합치도록 요청", "Python 패키지를 설치", "저장소를 컴퓨터에서 삭제", "비밀번호를 변경"], 1, "GitHub"),
    Quiz("GitHub Issue는 주로 어떤 일을 기록하나요?", ["할 일, 질문, 버그 보고", "Python 변수의 값", "로컬 파일의 저장 경로", "컴퓨터의 로그인 암호"], 1, "GitHub"),
    Quiz("저장소를 Public으로 설정하면 일반적으로 어떻게 되나요?", ["누구나 저장소 내용을 볼 수 있음", "소유자만 볼 수 있음", "저장소가 자동 삭제됨", "Git 명령을 사용할 수 없음"], 1, "GitHub"),
    Quiz("다른 사람의 GitHub 저장소를 내 계정 공간에 복사해 독립적으로 작업하려면 무엇을 사용하나요?", ["Fork", "Pull", "Commit", "Stash"], 1, "GitHub"),
    Quiz("GitHub에서 저장소를 Clone한 뒤 로컬에 생기는 것은 무엇인가요?", ["작업할 수 있는 로컬 저장소 복사본", "웹 브라우저의 북마크만", "원본 저장소의 소유권", "새 GitHub 계정"], 1, "GitHub"),
    Quiz("GitHub 원격 저장소에 코드를 올리기 전에 확인해야 할 보안상 중요한 항목은 무엇인가요?", ["비밀번호나 API 키가 코드에 포함되지 않았는지", "모든 변수 이름이 한 글자인지", "화면 배경색이 어두운지", "파일이 모두 같은 크기인지"], 1, "GitHub"),
    Quiz("GitHub 저장소에 새 브랜치를 두는 가장 알맞은 이유는 무엇인가요?", ["기존 작업을 보존하면서 새 변경을 독립적으로 진행", "저장소를 인터넷에서 숨김", "모든 파일을 자동 백업", "Python 버전을 바꿈"], 1, "GitHub"),
    Quiz("GitHub 웹사이트에서 README.md를 열면 보통 어떻게 표시되나요?", ["Markdown 서식이 적용된 문서", "Python 프로그램 실행 화면", "편집 불가능한 이미지", "JSON 데이터베이스"], 1, "GitHub"),
    Quiz("팀원이 만든 변경사항을 내 로컬 브랜치에 가져와 반영할 때 쓰는 명령은 무엇인가요?", ["git pull", "git init", "git add", "git status"], 1, "GitHub"),
    Quiz("GitHub 저장소에서 Issue를 열어 작업을 논의하는 좋은 이유는 무엇인가요?", ["논의와 진행 상황을 한곳에서 추적", "모든 커밋을 지우기", "로컬 브랜치를 자동 삭제", "Python을 관리자 권한으로 실행"], 1, "GitHub"),
]