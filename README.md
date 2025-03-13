# Interfață Web pentru Gestiunea Studenților și Cursurilor

## Descriere
Proiectul constă într-o aplicație web dezvoltată pentru gestionarea eficientă a informațiilor legate de studenți, cursuri și înscrierile acestora. Interfața permite efectuarea operațiilor CRUD (Creare, Citire, Actualizare, Ștergere), facilitând gestionarea interactivă a unei baze de date relaționale realizată în MySQL.

## Funcționalități principale
- Vizualizare, adăugare, editare și ștergere informații despre studenți, cursuri și înscrieri
- Gestionarea relațiilor complexe (M:N) între studenți și cursuri
- Validarea informațiilor introduse pentru asigurarea integrității datelor
- Gestionarea erorilor și redirecționarea către pagini specifice în caz de probleme

## Tehnologii utilizate
- Python cu Flask (back-end)
- HTML și CSS (front-end și design)
- MySQL Workbench (baza de date)

## Structura bazei de date
- **students:** ID, prenume, nume, an curent, serie, număr grupă
- **courses:** ID curs, nume curs, credite, tip curs
- **enrollments:** ID student, ID curs, data înscrierii, notă

## Implementare
Interfața web a fost realizată utilizând Flask pentru gestionarea interacțiunilor dintre utilizator și baza de date MySQL. HTML și CSS au fost folosite pentru design-ul paginilor web, oferind o navigare intuitivă și o interfață prietenoasă.

## Pași principali ai implementării
1. Crearea și structurarea bazei de date în MySQL
2. Dezvoltarea aplicației Flask pentru conectarea și gestionarea bazei de date
3. Implementarea paginilor web și operațiilor CRUD folosind Flask, HTML și CSS
4. Adăugarea validărilor și gestionarea erorilor în aplicație

## Instalare și rulare
1. Clonează repository-ul:
```bash
git clone https://github.com/user/student-course-management.git
```

2. Instalează dependențele necesare:
```bash
pip install -r requirements.txt
```

3. Configurează baza de date MySQL:
- Creează baza de date utilizând scriptul SQL furnizat (`edu_track.sql`).
- Actualizează configurația aplicației Flask cu detaliile conexiunii MySQL.

4. Rulează aplicația Flask:
```bash
python app.py
```

5. Accesează aplicația din browser la adresa:
```
http://localhost:5000
```

---

# Web Interface for Student and Course Management

## Description
This project is a web application designed for efficient management of student, course, and enrollment data. The interface allows CRUD operations (Create, Read, Update, Delete), providing an interactive management experience with a MySQL relational database.

## Main Features
- Viewing, adding, editing, and deleting student, course, and enrollment records
- Managing complex M:N relationships between students and courses
- Input validation to ensure data integrity
- Error handling with dedicated error pages

## Technologies Used
- Python with Flask (back-end)
- HTML and CSS (front-end and styling)
- MySQL Workbench (database)

## Database Structure
- **students:** ID, first name, last name, current year, series, group number
- **courses:** Course ID, course name, credits, course type
- **enrollments:** Student ID, course ID, enrollment date, grade

## Implementation
The web interface was developed using Flask to manage interactions between the user and the MySQL database. HTML and CSS provided an intuitive and user-friendly web page design.

## Main Implementation Steps
1. Database creation and structure definition in MySQL
2. Flask application development for database connectivity and management
3. Web pages and CRUD operations implementation using Flask, HTML, and CSS
4. Implementation of input validation and comprehensive error handling

## Installation and Running
1. Clone the repository:
```bash
git clone https://github.com/user/student-course-management.git
```

2. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the MySQL database:
- Create the database using the provided SQL script (`edu_track.sql`).
- Update the Flask application configuration with your MySQL connection details.

4. Run the Flask application:
```bash
python app.py
```

5. Access the application via browser at:
```
http://localhost:5000
```

