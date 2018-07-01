class MyGrade:
    def __init__(self):
        self._value = 0

    def __set__(self, instance, value):
        if not 0 <= value <= 100:
            raise ValueError("blabla")
        self._value = value

    def __get__(self, instance, owner):
        return self._value


class MyExam:
    def __init__(self):
        self.grade = MyGrade()

exam = MyExam()
exam.grade = 20

exam2 = MyExam
exam2.grade = 30

print(exam.grade)
print(exam2.grade)


exam3 = MyExam
exam3.grade = 130

print(exam3.grade)
