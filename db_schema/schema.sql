CREATE TABLE branch (
	id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	location VARCHAR(500) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_branch_name ON branch (name);
CREATE TABLE faculty (
	id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	description TEXT, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_faculty_name ON faculty (name);
CREATE TABLE audit_log (
	id INTEGER NOT NULL, 
	table_name VARCHAR(50) NOT NULL, 
	record_id INTEGER NOT NULL, 
	action VARCHAR(10) NOT NULL, 
	old_values TEXT, 
	new_values TEXT, 
	timestamp DATETIME, 
	PRIMARY KEY (id)
);
CREATE TABLE book (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	authors TEXT NOT NULL, 
	publisher VARCHAR(200) NOT NULL, 
	year INTEGER NOT NULL, 
	pages INTEGER NOT NULL, 
	illustrations INTEGER, 
	cost FLOAT NOT NULL, 
	copies_available INTEGER, 
	times_issued INTEGER, 
	branch_id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(branch_id) REFERENCES branch (id)
);
CREATE INDEX ix_book_title ON book (title);
CREATE TABLE book_faculties (
	book_id INTEGER NOT NULL, 
	faculty_id INTEGER NOT NULL, 
	PRIMARY KEY (book_id, faculty_id), 
	FOREIGN KEY(book_id) REFERENCES book (id), 
	FOREIGN KEY(faculty_id) REFERENCES faculty (id)
);
