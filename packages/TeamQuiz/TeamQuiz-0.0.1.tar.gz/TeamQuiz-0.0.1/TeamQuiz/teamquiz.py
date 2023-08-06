class Quiz:
    def __init__(self):
      self.questions=["What is the name of our planet?","what color is a banana?","what is your root name?"]
      self.answers=["Earth","Yellow","FACE18G"]
    def generate_map(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        map = ""
        for i in range(self.rows):
            for j in range(self.columns):
                map += "#"
            map += "\n"
        return map

    def get_all(self):
        return self.questions


    def get_question(self,num: int):
        self.num=num
        return self.questions[self.num]

    def submit(self,question_num: int, answer: str):
        if answer.lower()==self.answers[question_num].lower():
            return "Correct"
        else:
            return "Wrong"

