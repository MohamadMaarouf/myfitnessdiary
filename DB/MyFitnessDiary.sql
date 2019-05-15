# MyFitnessDiary DB Script
#   This script builds the database
#   from the ground up

CREATE DATABASE MyFitnessDiary;
USE MyFitnessDiary;


CREATE TABLE users
(
    user_id INT
    AUTO_INCREMENT,
    email VARCHAR (255),
    password VARCHAR (255),
    role VARCHAR (25),
    name VARCHAR (255),
    last_login DATETIME,
    PRIMARY KEY (user_id)
);

    CREATE TABLE member
    (
        user_id INT NOT NULL,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        title VARCHAR(255),
        location VARCHAR(255),
        about VARCHAR(1024),
        url VARCHAR(255),
        goalWeight VARCHAR(255),
        mainExercise VARCHAR(255),
        workoutOne VARCHAR(255),
        workoutTwo VARCHAR(255),
        workoutThree VARCHAR(255),
        verified BOOL,
        private BOOL,
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)    
    );


    CREATE TABLE diaryPosting
    (
        diary_id INT AUTO_INCREMENT,
        member_id INT NOT NULL,
        image BLOB,
        dateOfPost DATE,
        exercise VARCHAR (255),
        overview VARCHAR (1024),
        current VARCHAR(255),
        goal VARCHAR(255),
        PRIMARY KEY (diary_id),
        FOREIGN KEY (member_id) REFERENCES member(user_id)
);

        # Test Data

        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'mmaarouf95@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'member', 'Mohamad');
        INSERT INTO users
            (user_id, email, password, role, name)
        VALUES
            (0, 'mmaarouf95@yahoo.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                'member', 'Mohamad');



        INSERT INTO member
            (user_id, first_name, last_name, title, location, about, url, goalWeight, verified)
        VALUES
            (1, 'Mohamad', 'Maarouf', 'Dedicated to the fitness lifestyle', 'Edge Fitness-Stratford, CT',
                'Fitness is a lifestyle and i live every moment in accordance with it.', 'mmaarouf95@gmail.com', '315', 1);

       INSERT INTO member
            (user_id, first_name, last_name, title, location, about, url, goalWeight, verified)
        VALUES(2, 'Mohamad', 'Maarouf', 'Let the results speak', 'Edge Fitness-Orange, CT',
                'Fitness Enthusiast since the age of 15.',
                'mmaarouf95@yahoo.com', '315', 1);
 
        INSERT INTO diaryPosting
            (diary_id, member_id, dateOfPost, exercise, overview, current, goal)
        VALUES(
                0,
                2,
                '2010-01-01',
                'Benchpress',
                'An amazing workout. Had a healthy breakfast and was energetic for the duration of the workout. Should focus more on form and explosiveness to increase max benchpress.',
                '135',
                '315'
    );