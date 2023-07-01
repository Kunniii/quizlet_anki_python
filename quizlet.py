from requests import get
from bs4 import BeautifulSoup as bs4
from os import path
import json


class Quizlet:
    url: str = None
    soup: bs4 = None
    file_path: str = None

    def from_url(self, url: str) -> None:
        self.url = url
        self.soup = bs4(get(url).text, "html.parser")

    def from_file(self, file_name: str) -> None:
        self.file_path = path.abspath(file_name)
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.soup = bs4(f.read(), "html.parser")

    def get_file_path(self) -> str:
        return self.file_path

    def get_url(self) -> str:
        return self.url

    def get_raw_json(self) -> dict:
        script = self.soup.find("script", {"id": "__NEXT_DATA__"}).text
        raw_json: dict = json.loads(script)
        redux_state = json.loads(
            raw_json["props"]["pageProps"]["dehydratedReduxStateKey"]
        )
        return redux_state

    def get_json(self, reverse=False) -> dict:
        raw = self.get_raw_json()
        raw_questions: dict = raw["setPage"]["termIdToTermsMap"]
        questions = []

        if reverse:
            for k, v in raw_questions.items():
                questions.append(
                    {"id": k, "answer": v["word"], "question": v["definition"]}
                )
        else:
            for k, v in raw_questions.items():
                questions.append(
                    {"id": k, "question": v["word"], "answer": v["definition"]}
                )

        return questions

    def export(self, file_name, reverse=False) -> None:
        with open(path.abspath(file_name), "w+", encoding="utf-8") as f:
            print("#separator:tab\n#html:true", file=f)
            questions = self.get_json(reverse)
            for question in questions:
                q: str = question.get("question").replace("\n", "<br>")
                a: str = question.get("answer").replace("\n", "<br>")
                print(f"{q}\t{a}", file=f)


if __name__ == "__main__":
    quizlet = Quizlet()
    quizlet.from_file("quizlet.html")

    with open("question_bank.json", "w+", encoding="utf-8") as f:
        print(json.dumps(quizlet.get_json(), indent=2, ensure_ascii=False), file=f)
    quizlet.export("import_MLN.txt")
