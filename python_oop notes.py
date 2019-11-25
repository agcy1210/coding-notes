class User:
    count = 0   #class attribute
    def __init__(self):         #non-parametized constructor also called default constructor
        User.count = User.count+1

class Student:
    def __init__(self,first,last,age):  #parametrized constructor
        self.first = first
        self.last = last
        self.age = age

    def print_attrs(self):
        print("name: {}\nage: {}".format(self.first,self.age))

    def total_marks(self,marks1,marks2):
        self.marks1 = marks1
        total = marks1 + marks2
        print(total)

    def test(self):
        print(self.marks1)
        #print(self.marks2)     This generates error as it is not assigned to self so it can't be called outside the total_marks function

user1 = User()  #user1 is the object/instance of class User
user2 = User()
user3 = User()
print(User.count)   #calling the class attribute

stud = Student('aman', 'chaudhary', 19)
stud.print_attrs()
stud.total_marks(99, 97)
stud.test()

print(stud.marks1)
print(stud.first)
#print(stud.marks2) it shows error as marks2 is not assigned to self so it can't be accesses directly outside the function total_marks


class College:
    @classmethod
    def from_string(cls,data_str):  #used when working with csv file. It assigns the attributes of class from just one line
        name,area,unq_id = data_str.split(",")
        return cls(name,area,unq_id)

    def __init__(self,name,area,unq_id):
        self.name = name
        self.area = area
        self.unq_id = unq_id

    def print_details(self):
        print("name: {}\narea: {}\nunq_id:{}".format(self.name,self.area,self.unq_id))

cllg_1 = College.from_string("ldce,navrangpura,28")
print(cllg_1.name)
cllg_1.print_details()

cllg_2 = College("daiict","gandhinagar",2)
print(cllg_2.area)
cllg_2.print_details()






