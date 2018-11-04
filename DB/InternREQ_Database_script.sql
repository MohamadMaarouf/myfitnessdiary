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

INSERT INTO users VALUES(0, 'tombirmingham91@gmail.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES(0, 'chris.conlon1993@gmail.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES(0, 'djaekle123@gmail.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES(0, 'mmaarouf95@gmail.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES(0, 'glinskid3@gmail.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');

SELECT * FROM users;

# Build FACULTY, STUDENT, SPONSOR tables
 
CREATE TABLE faculty(
        user_id INT NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        location VARCHAR(50),
        degree VARCHAR(50),
        department VARCHAR(50),
        position VARCHAR(50),
        profile_picture BLOB,
        banner BLOB,
        about VARCHAR(1024),
        skills VARCHAR(1024),
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
);


CREATE TABLE student(
       user_id INT NOT NULL,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       location VARCHAR(50),
       major VARCHAR(50),
       profile_picture BLOB,
       banner BLOB,
       about VARCHAR(1024),
       skills VARCHAR(1024),
       resume BLOB,
       graduation_date DATE, 	# DATE type returns format 'YYY-MM-DD' without time
       GPA FLOAT(3,2),		# 3 digits with 2 decimal place      
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
        url VARCHAR(255),
        profile_picture BLOB,
        banner BLOB,
        about VARCHAR(1024),
        skills VARCHAR(1024),
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
);


# Create PROFILE, INTERNSHIP, and APPLICATION tables

CREATE TABLE profile(
       user_id INT NOT NULL,
       about VARCHAR(1024),
       skills VARCHAR(1024),
       PRIMARY KEY(user_id),
       FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE internship(
	internship_id INT AUTO_INCREMENT,
	user_id INT NOT NULL,
	about VARCHAR(1024),
        image BLOB,
        title VARCHAR(255),
        location VARCHAR(255),
        overview VARCHAR(1024),
        responsiblities VARCHAR(1024),
        requirements VARCHAR(1024),
        compensation BIT(1),
        type VARCHAR(50), # full, part or internship
        availability VARCHAR(255),
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
