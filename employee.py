from db import c, conn


"""
PK - Primary Key
"""



class Employee(object):
    def __init__(self, name, surname, age, pk=None):
        self.id = pk
        self.name = name
        self.surname = surname
        self.age = age

    @classmethod
    def get(cls, pk):
        result = c.execute("SELECT * FROM employee WHERE id = ?", (pk,))
        values = result.fetchone()
        if values is None:
            return None
        employee = Employee(values["name"], values["surname"], values["age"], values["id"])
        return employee

    def __repr__(self):
        return "<Employee {}>".format(self.name)

    def update(self):
        c.execute("UPDATE employee SET name = ?, surname = ?, age = ? WHERE id = ?",
                  (self.name, self.surname, self.age, self.id))

    def create(self):
        c.execute("INSERT INTO employee (name, surname, age) VALUES (?, ?, ?)", (self.name, self.surname, self.age))
        self.id = c.lastrowid

    def save(self):
        if self.id is not None:
            self.update()
        else:
            self.create()
        return self

    def delete(self):
        c.execute("DELETE FROM employee WHERE id = ?", (self.id,))
        del self

    def __ge__(self, other):
        if isinstance(other, Employee):
            return self.age >= other.age
        else:
            raise ValueError("Can't compare Employee with {}".format(type(other)))

    def __gt__(self, other):
        if isinstance(other, Employee):
            return self.age > other.age
        else:
            raise ValueError("Can't compare Employee with {}".format(type(other)))

    def __le__(self, other):
        if isinstance(other, Employee):
            return self.age <= other.age
        else:
            raise ValueError("Can't compare Employee with {}".format(type(other)))

    def __lt__(self, other):
        if isinstance(other, Employee):
            return self.age < other.age
        else:
            raise ValueError("Can't compare Employee with {}".format(type(other)))



    @classmethod
    def get_list(csl,**kwargs):
    
        if kwargs:
            query = "SELECT * FROM employee WHERE "
            query += " AND ".join([f"{key} = ?" for key in kwargs.keys()])
            result = c.execute(query, tuple(kwargs.values()))
        else:
            result = c.execute("SELECT * FROM employee")
        return [Employee(values["name"], values["surname"], values["age"], values["id"]) for values in result.fetchall()]
