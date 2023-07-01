import json

lines: list[str] = []
questions: list[dict] = []

with open("questions.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()


question: str = ""
answer: str = ""
for line in lines:
    if len(line.strip()) == 1:
        answer = line.strip()
        questions.append({"question": question, "answer": answer.upper()})
        question = ""
    else:
        question += line

with open("questions.json", "w+", encoding="utf-8") as f:
    print(json.dumps(questions, indent=2, ensure_ascii=False), file=f)

with open("import_me.txt", "w+", encoding="utf-8") as f:
    print("#separator:tab\n#html:true", file=f)
    for question in questions:
        q: str = question.get("question").replace("\n", "<br>")
        a: str = question.get("answer").replace("\n", "<br>")
        print(f'"{q}"\t{a.upper()}', file=f)
