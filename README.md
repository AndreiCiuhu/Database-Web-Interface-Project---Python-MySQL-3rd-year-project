# Interfață Web pentru Gestiunea Studenților și Cursurilor

## Descriere
Proiectul reprezintă o aplicație web implementată în Python, destinată gestionării eficiente a informațiilor legate de studenți, cursuri și înscrieri. Această aplicație permite utilizatorilor să efectueze operații CRUD (Creare, Citire, Actualizare, Ștergere) asupra unei baze de date relaționale MySQL.

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

---

# Web Interface for Student and Course Management

## Description
This project is a web-based application developed to efficiently manage student, course, and enrollment data using Python and a relational MySQL database. It provides a user-friendly interface for CRUD operations.

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

