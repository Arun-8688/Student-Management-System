
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

import sqlite3


class Student(BaseModel):
    name: str
    age: int = Field(ge=18, le=30)
    gender: str
    marks: int = Field(ge=0, le=100)
    course: str
    image: str
    status: int


def get_connection():
    connection = sqlite3.connect("students.db")
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    q = """CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        marks INTEGER,
        course TEXT,
        image TEXT,
        status INTEGER
    )"""

    cursor.execute(q)
    connection.commit()
    connection.close()


create_table()

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# View All Students
@app.get("/")
def Home(req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    q = "SELECT * FROM students"
    cursor.execute(q)

    students = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"std": students}
    )


# Add Student Page
@app.get("/students/add")
def std_add(req: Request):

    return templates.TemplateResponse(
        request=req,
        name="add.html",
        context={}
    )


# Insert Student
@app.post("/students/add")
def create_std(
    name: str = Form(),
    age: int = Form(),
    gender: str = Form(),
    marks: int = Form(),
    course: str = Form(),
    image: str = Form(),
    status: int = Form()
):

    std = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    values = (
        std.name,
        std.age,
        std.gender,
        std.marks,
        std.course,
        std.image,
        std.status
    )

    connection = get_connection()
    cursor = connection.cursor()

    q = """INSERT INTO students
    (name, age, gender, marks, course, image, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""

    cursor.execute(q, values)

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# View Single Student
@app.get("/students/{id}")
def student_details(id: int, req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    q = "SELECT * FROM students WHERE id = ?"
    cursor.execute(q, (id,))

    student = cursor.fetchone()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="std.html",
        context={"student": student}
    )


# Delete Student
@app.post("/students/delete/{id}")
def delete_student(id: int):

    connection = get_connection()
    cursor = connection.cursor()

    q = "DELETE FROM students WHERE id = ?"
    cursor.execute(q, (id,))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )
 

# Edit Student Page
@app.get("/students/edit/{id}")
def edit_student(id: int, req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    q = "SELECT * FROM students WHERE id = ?"
    cursor.execute(q, (id,))

    student = cursor.fetchone()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="edit.html",
        context={"student": student}
    )


# Update Student
@app.post("/students/update/{id}")
def update_student(
    id: int,
    name: str = Form(),
    age: int = Form(),
    gender: str = Form(),
    marks: int = Form(),
    course: str = Form(),
    image: str = Form(),
    status: int = Form()
):

    std = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    values = (
        std.name,
        std.age,
        std.gender,
        std.marks,
        std.course,
        std.image,
        std.status,
        id
    )

    connection = get_connection()
    cursor = connection.cursor()

    q = """UPDATE students
    SET name = ?, age = ?, gender = ?, marks = ?,
    course = ?, image = ?, status = ?
    WHERE id = ?"""

    cursor.execute(q, values)

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )