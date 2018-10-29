# Building InternREQ Database (script)

# Create the Database

CREATE DATABASE internreq;
USE internreq;

# Build USERS table

CREATE TABLE users(
       user_id INT AUTO_INCREMENT,
       email VARCHAR(255),
       password VARCHAR(255),
       role VARCHAR(25),
       PRIMARY KEY(user_id)
);

INSERT INTO users VALUES(0, 'tombirmingham91@gmail.com', 'password1', 'faculty admin');
INSERT INTO users VALUES(0, 'chris.conlon1993@gmail.com', 'password1', 'faculty admin');
INSERT INTO users VALUES(0, 'djaekle123@gmail.com', 'password1', 'faculty admin');
INSERT INTO users VALUES(0, 'mmaarouf95@gmail.com', 'password1', 'faculty admin');
INSERT INTO users VALUES(0, 'glinskid3@gmail.com', 'password1', 'faculty admin');

SELECT * FROM users;

# Build FACULTY, STUDENT, SPONSOR tables
 
CREATE TABLE faculty(
       user_id INT NOT NULL,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       location VARCHAR(50),
       degree VARCHAR(50),
       department VARCHAR(50),
       PRIMARY KEY(user_id),
       FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE student(
       user_id INT NOT NULL,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       location VARCHAR(50),
       major VARCHAR(50),
       graduation_date DATE,
       # DATE type returns format 'YYY-MM-DD' without time        
       GPA FLOAT(3,2),		
       # 3 digits with 2 decimal place        
       PRIMARY KEY(user_id),        
       FOREIGN KEY(user_id) REFERENCES 
       users(user_id)
       );

CREATE TABLE sponsor(
       user_id INT NOT NULL,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       location VARCHAR(50),
       company VARCHAR(50),
       website VARCHAR(255),
       PRIMARY KEY(user_id),
       FOREIGN KEY(user_id) REFERENCES users(user_id)
);

# Create PROFILE, INTERNSHIP, and APPLICATION tables

CREATE TABLE profile(
       user_id INT NOT NULL,
       about VARCHAR(1000),
       skills VARCHAR(1000),
       PRIMARY KEY(user_id),
       FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE internship(
	internship_id INT AUTO_INCREMENT,
	user_id INT NOT NULL,
	about VARCHAR(1000),
	PRIMARY KEY(internship_id),
	FOREIGN KEY(user_id) REFERENCES sponsor(user_id)
);

CREATE TABLE applications(
	user_id INT NOT NULL,
	internship_id INT NOT NULL,
	PRIMARY KEY(user_id, internship_id),
	FOREIGN KEY(user_id) REFERENCES student(user_id),
	FOREIGN KEY(internship_id) REFERENCES internship(internship_id)
);