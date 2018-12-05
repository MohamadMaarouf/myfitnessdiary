# InternREQ DB Script
#   This script builds the database
#   from the ground up

CREATE DATABASE internreq;
USE internreq;


CREATE TABLE users
(
    user_id INT
    AUTO_INCREMENT,
    email VARCHAR
    (255),
    password VARCHAR
    (255),
    role VARCHAR
    (25),
    name VARCHAR
    (255),
    last_login DATETIME,
    PRIMARY KEY
    (user_id)
);


    CREATE TABLE faculty
    (
        user_id INT NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        title VARCHAR(50),
        department VARCHAR(50),
        location VARCHAR(50),
        about VARCHAR(1024),
        url VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(14),
        phone_desc VARCHAR(50),
        verified BOOL,
        private BOOL,
        education VARCHAR(50),
        additional VARCHAR(1024),
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );


    CREATE TABLE student
    (
        user_id INT NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        title VARCHAR(50),
        major VARCHAR(50),
        location VARCHAR(50),
        about VARCHAR(1024),
        url VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(13),
        phone_desc VARCHAR(50),
        verified BOOL,
        private BOOL,
        education VARCHAR(50),
        additional VARCHAR(1024),
        graduation_date VARCHAR(10),
        GPA VARCHAR(4),
        resume MEDIUMBLOB,
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );


    CREATE TABLE sponsor
    (
        user_id INT NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        title VARCHAR(50),
        company VARCHAR(50),
        location VARCHAR(50),
        about VARCHAR(1024),
        url VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(13),
        phone_desc VARCHAR(50),
        verified BOOL,
        private BOOL,
        education VARCHAR(50),
        additional VARCHAR(1024),
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );


    CREATE TABLE internship
    (
        internship_id INT AUTO_INCREMENT,
        sponsor_id INT NOT NULL,
        image BLOB,
        title VARCHAR (255),
        location VARCHAR (255),
        overview VARCHAR (1024),
        responsibilities VARCHAR (1024),
        requirements VARCHAR (1024),
        compensation BOOL,
        type VARCHAR (50), # full, part or internship
        availability VARCHAR (255),
        PRIMARY KEY (internship_id),
        FOREIGN KEY (sponsor_id) REFERENCES sponsor(user_id)
);


        CREATE TABLE applications
        (
            student_id INT NOT NULL,
            sponsor_id INT NOT NULL,
            internship_id INT NOT NULL,
            PRIMARY KEY(student_id, internship_id),
            FOREIGN KEY(student_id) REFERENCES student(user_id),
            FOREIGN KEY(sponsor_id) REFERENCES sponsor(user_id),
            FOREIGN KEY(internship_id) REFERENCES internship(internship_id)
        );

        # Test Data

        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'chris.conlon1993@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Chris');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'tombirmingham91@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Tom');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'djaekle123@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Davis');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'mmaarouf95@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Mohamad');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'glinskid3@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Dan');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'hendell@brandshop.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'sponsor', 'Rubin');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'morroj@southernct.edu', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'student', 'Jeff');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'elahia@southernct.edu', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'faculty', 'Ata');


        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about, URL, email,
            phone, phone_desc, verified, private, education, additional)
        VALUES
            (1, 'Chris', 'Conlon', 'Software Clown', 'Computer Science Department', 'Wallingford, CT',
                'As a software clown I strive for excellence in comedic value and unbreakable code',
                'https://www.southernct.edu/', 'chris.conlon1993@gmail.com', '(203) 392-7278', 'office phone',
                1, 0,
                'undergrad', 'Python, SQL, Flask, Bootstrap, HTML/CSS, Jinja');
        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about, verified)
        VALUES
            (2, 'Tom', 'Birmingham', 'Software Clown', 'Computer Science Department', 'Brookfield, CT',
                'As a software clown I strive for excellence in comedic value and unbreakable code', 1);
        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about, verified)
        VALUES
            (3, 'Davis', 'Jaekle', 'Demon of Design', 'Computer Science Department', 'Stratford, CT',
                'Master of designing advanced systems built on the basis fear and terror', 1);
        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about,verified)
        VALUES
            (4, 'Mohamad', 'Maarouf', 'Demon of Design', 'Computer Science Department', 'Stratford, CT',
                'Master of designing advanced systems built on the basis fear and terror', 1);
        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about, verified)
        VALUES
            (5, 'Dan', 'Glinski', 'Software Clown', 'Computer Science Department', 'Brookfield, CT',
                'As a software clown I strive for excellence in comedic value and unbreakable code', 1);


        INSERT INTO sponsor
            (user_id, first_name, last_name, title, company, location, about, url, email, verified, education)
        VALUES(6, 'Reuben', 'Hendell', 'Chief Executive Officer', 'BrandShop', 'Shelton, CT',
                'Our mission is to create branded digital commerce experiences for the world’s best brands. If you are passionate, motivated, collaborative, innovative and a whole lot of fun, then we need your help.',
                'https://brandshop.com/', 'rhendell@brandshop.com', 1, 'MBA');
        INSERT INTO student
            (user_id, first_name, last_name, title, major, location, about, education, additional,
            graduation_date, GPA)
        VALUES(7, 'Jeff', 'Morro', 'Student', 'Fine Arts & Music', 'New Haven, CT',
                'As a music major I am a believer that music can change the world.',
                'undergrad', 'Can play several instruments, read sheet music, and excellent communicator.',
                '2019-05-01', 3.5);
        INSERT INTO faculty
            (user_id, first_name, last_name, title, department, location, about, url, email,
            phone, phone_desc, verified, education)
        VALUES(8, 'Ata', 'Elahi', 'Professor', 'Computer Science Department', 'New Haven, CT',
                'I am an expert in computer organization and hardware, CPU design, networking, and more.',
                'https://southernct.edu/', 'elahia@southernct.edu', '(203) 392-7278', 'office phone',
                1, 'Ph.D. Elec. Engineering');


        INSERT INTO internship
            (internship_id, sponsor_id, title, location, overview, responsibilities, requirements, compensation, type, availability)
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
