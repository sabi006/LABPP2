#ex1
class m1:
    count = 0

    def __init__(self):
        m1.count += 1

    @classmethod
    def show_count(cls):
        print(f"Ex1 - Total objects: {cls.count}")

e1a = m1()
e1b = m1()
m1.show_count()
#ex2
class m2:
    default_color = "blue"

    @classmethod
    def show_color(cls):
        print(f"Ex2 - Default color: {cls.default_color}")

m2.show_color()
#ex3
class m3:
    discount = 0.1

    @classmethod
    def show_discount(cls):
        print(f"Ex3 - Discount: {cls.discount * 100}%")

m3.show_discount()
#ex4
class m4:
    school_name = "Sunrise High"

    @classmethod
    def show_school(cls):
        print(f"Ex4 - School name: {cls.school_name}")

m4.show_school()

