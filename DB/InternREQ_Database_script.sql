# InternREQ Database (script)


CREATE DATABASE internreq;

USE internreq;


CREATE TABLE users(
    user_id INT AUTO_INCREMENT,
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(25),
    PRIMARY KEY(user_id)
);


INSERT INTO users VALUES (0, 'chris.conlon1993@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES (0, 'tombirmingham91@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES (0, 'djaekle123@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES (0, 'mmaarouf95@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');
INSERT INTO users VALUES (0, 'glinskid3@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');

INSERT INTO users VALUES (0, 'hendell@brandshop.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'sponsor');
INSERT INTO users VALUES (0, 'morroj@southernct.edu', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student');
INSERT INTO users VALUES (0, 'elahia@southernct.edu', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'faculty');


SELECT * FROM users;

 
CREATE TABLE faculty(
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    location VARCHAR(50),
    degree VARCHAR(50),
    department VARCHAR(50),
    position VARCHAR(50),
    profile_img BLOB,
    banner_img BLOB,
    about VARCHAR(1024),
    skills VARCHAR(1024),
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


INSERT INTO faculty (user_id, first_name, last_name, location, degree, department, position, about)
    VALUES(
        8,
        'Ata',
        'Elahi',
        'New Haven, CT',
        'Phd Electrical Engineering',
        'Computer Science Department',
        'Professor',
        'I am an expert in computer organization and hardware, CPU design, networking, and more.'
);

CREATE TABLE student(
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    location VARCHAR(50),
    major VARCHAR(50),
    graduation_date DATE,
    # 'YYY-MM-DD' format
    GPA FLOAT(3,2),
    profile_img BLOB,
    banner_img BLOB,
    about VARCHAR(1024),
    skills VARCHAR(1024),
    PRIMARY KEY(user_id),        
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


INSERT INTO student (user_id, first_name, last_name, location, major, graduation_date, GPA, about, skills)
    VALUES(
        7,
        'Jeff',
        'Morro',
        'New Haven, CT',
        'Fine Arts: Music',
        '2019-05-01',
        3.5,
        'As a music major I am a believer that music can change the world.',
        'Can play several instruments, read sheet music, and excellent communicator.'
);


CREATE TABLE sponsor(
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    location VARCHAR(50),
    title VARCHAR(50),
    company VARCHAR(50),
    url VARCHAR(255),
    profile_picture BLOB,
    banner BLOB,
    about VARCHAR(1024),
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


INSERT INTO sponsor (user_id, first_name, last_name, location, title, company, url, about)
    VALUES(
        6,
        'Reuben',
        'Hendell',
        'Chief Executive Officer',
        'BrandShop',
        'Shelton, CT',
        'https://brandshop.com/',
        'Our mission is to create branded digital commerce experiences
         for the world’s best brands. If you are passionate, motivated,
         collaborative, innovative and a whole lot of fun, then we need your help.'
);


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
    image BLOB,
    title VARCHAR(255),
    location VARCHAR(255),
    overview VARCHAR(1024),
    responsibilities VARCHAR(1024),
    requirements VARCHAR(1024),
    compensation BIT(1),
    type VARCHAR(50), # full, part or internship
    availability VARCHAR(255),
	PRIMARY KEY(internship_id),
	FOREIGN KEY(user_id) REFERENCES sponsor(user_id)
);

INSERT INTO internship (internship_id, user_id, title, location, overview, responsibilities, requirements, compensation, type, availability)
    VALUES(
        0,
        6,
        'Magento 2 Developer',
        'Shelton, CT',
        'The Magento Engineer is responsible for providing quality solutions that meet development requirements in support of our eCommerce platform projects.',
        'The Magento 2 Engineer is primarily responsible for producing quality, on-budget, and on-schedule solutions on projects. Responsibilities and duties include:
        \nCreatively solve complex problems
        \nDevelop on the Magento 2 platform
        \nContribute to our client’s code base using an open source model in Github
        \nDevelop custom extensions to be released as third-party add-ons
        \nContribute to internal initiatives such as improving our development processes
        \nOther duties as needed',
        'Magento Certified Developer
        \nPrefer experience developing on the Magento 2 platform
        \nPrefer 2+ years experience in web development; maintenance programs, integrations, servers.
        \nVery comfortable in HTML/CSS, Javascript & JQuery, XML, SQL, PHP, Git, Node
        \nLikes mentoring, coaching, and training others
        \nExperience in both Agile & Waterfall environments
        \nExcellent written and oral communication skills with team members and clients',
        0,
        'internship',
        'M-F 3:00-5 PM'
    );


CREATE TABLE applications(
	user_id INT NOT NULL,
	internship_id INT NOT NULL,
	PRIMARY KEY(user_id, internship_id),
	FOREIGN KEY(user_id) REFERENCES student(user_id),
	FOREIGN KEY(internship_id) REFERENCES internship(internship_id)
);
