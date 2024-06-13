CREATE TABLE People (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, father_name TEXT, height REAL);

INSERT INTO People VALUES (1, "Steven", 56, "Giannis", 1.61);
INSERT INTO People VALUES (2, "Peter", 24, "Ntinos", 1.76);
INSERT INTO People VALUES (3, "John", 21, "Dimitris", 1.75);
INSERT INTO People VALUES (4, "Maria", 37, "Argyris", 1.64);
INSERT INTO People VALUES (5, "Kathrin", 32, "Stefanos", 1.66);
INSERT INTO People VALUES (6, "Peter", 50, "Christos", 1.91);
INSERT INTO People VALUES (7, "Kostas", 25, "Petros", 1.96);
INSERT INTO People VALUES (8, "Chris", 46, "Giorgos", 1.84);
INSERT INTO People VALUES (9, "Helen", 49, "Antonis", 1.45);
INSERT INTO People VALUES (10, "Garufallia", 30, "Petros", 1.57);
INSERT INTO People VALUES (11, "Minas", 18, "Giannis", 1.89);
INSERT INTO People VALUES (12, "Antonis", 37, "Andreas", 1.74);
INSERT INTO People VALUES (13, "George", 24, "Hlias", 1.92);
INSERT INTO People VALUES (14, "Eirini", 28, "Sokratis", 1.59);
INSERT INTO People VALUES (15, "Nefeli", 46, "Spyros", 1.67);

SELECT * FROM People;
SELECT name FROM People WHERE age > 30 ORDER BY name;

SELECT SUM(height) FROM People;
SELECT MAX(age) FROM People;
SELECT MIN(age) FROM People;