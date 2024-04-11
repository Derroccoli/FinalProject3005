-- Inserting sample data into the 'members' table
INSERT INTO members (firstName, lastName, email, phone_number, date_registered) 
VALUES 
    ('John', 'Doe', 'john.doe@example.com', '1234567890', '2023-01-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '0987654321', '2023-01-02'),
    ('Alice', 'Johnson', 'alice.johnson@example.com', '5551234567', '2023-01-03'),
    ('Bob', 'Brown', 'bob.brown@example.com', '9876543210', '2023-01-04');

-- Inserting sample data into the 'trainers' table
INSERT INTO trainers (name, email) 
VALUES 
    ('Trainer 1', 'trainer1@example.com'),
    ('Trainer 2', 'trainer2@example.com'),
    ('Trainer 3', 'trainer3@example.com'),
    ('Trainer 4', 'trainer4@example.com');

-- Inserting sample data into the 'fitness_goals' table
INSERT INTO fitness_goals (member_id, description, completed) 
VALUES 
    (1, 'Lose 10 pounds', B'1'),
    (2, 'Run a marathon',  B'0'),
    (3, 'Gain muscle mass', B'0'),
    (4, 'Improve flexibility', B'1');

-- Inserting sample data into the 'achievements' table
INSERT INTO achievements (member_id, date_of_accomplishment, feat) 
VALUES 
    (1, '2023-01-10', 'Completed 5K run'),
    (2, '2023-01-15', 'Completed half marathon'),
    (3, '2023-01-20', 'Increased bench press by 20kg'),
    (4, '2023-01-25', 'Achieved full splits');

-- Inserting sample data into the 'health_metrics' table
INSERT INTO health_metrics (member_id, recorded_date, metric_type, value) 
VALUES 
    (1, '2023-01-05', 'Weight', '180 lbs'),
    (2, '2023-01-06', 'Body fat percentage', '15%'),
    (3, '2023-01-07', 'Muscle mass', '75 kg'),
    (4, '2023-01-08', 'Flexibility', 'Excellent');

-- Inserting sample data into the 'exercises' table
INSERT INTO exercises (member_id, date_of_routine, exercise, sets, reps, duration) 
VALUES 
    (1, '2023-01-05', 'Squats', 3, 12, 30),
    (2, '2023-01-06', 'Running', 1, 10, 60),
    (3, '2023-01-07', 'Bench press', 4, 8, 45),
    (4, '2023-01-08', 'Yoga', 1, 15, 60);

-- Inserting sample data into the 'pt_session' table
INSERT INTO pt_session (member_id, trainer_id, session_type) 
VALUES 
    (1, 1, 'Weight training'),
    (2, 2, 'Cardio'),
    (3, 3, 'Strength training'),
    (4, 4, 'Flexibility');

-- Inserting sample data into the 'group_fitness' table
INSERT INTO group_fitness (trainer_id, class_name, description, time, date) 
VALUES 
    (1, 'Yoga Class', 'Beginner-friendly yoga class', '10:00 AM', '2023-01-10'),
    (2, 'Bootcamp', 'High-intensity interval training', '6:00 PM', '2023-01-12'),
    (3, 'Spin Class', 'Indoor cycling workout', '7:00 AM', '2023-01-14'),
    (4, 'Zumba', 'Dance-based fitness class', '5:00 PM', '2023-01-16');

-- Inserting sample data into the 'group_members' table
INSERT INTO group_members (group_id, member_id) 
VALUES 
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4);

-- Inserting sample data into the 'bills' table
INSERT INTO bills (amount, member_id) 
VALUES 
    (50, 1),
    (75, 2),
    (60, 3),
    (80, 4);

-- Inserting sample data into the 'payments' table
INSERT INTO payments (bill_id, amount, date, processed) 
VALUES 
    (1, 50, '2023-01-10', B'1'),
    (2, 75, '2023-01-12', B'1'),
    (3, 60, '2023-01-14', B'0'),
    (4, 80, '2023-01-16', B'0');

-- Inserting sample data into the 'admin_staff' table
INSERT INTO admin_staff (firstName, lastName, email) 
VALUES 
    ('Admin', 'One', 'admin1@example.com'),
    ('Admin', 'Two', 'admin2@example.com'),
    ('Admin', 'Three', 'admin3@example.com'),
    ('Admin', 'Four', 'admin4@example.com');

-- Inserting sample data into the 'equipments' table
INSERT INTO equipments (equipment_type, description, maintenance_date) 
VALUES 
    ('Treadmill', 'Brand new treadmill', '2023-01-01'),
    ('Dumbbells', 'Set of 5-50 lb dumbbells', '2023-01-02'),
    ('Yoga mats', 'High-quality yoga mats', '2023-01-03'),
    ('Resistance bands', 'Set of resistance bands', '2023-01-04');

-- Inserting sample data into the 'rooms' table
INSERT INTO rooms (room_name, room_capacity) 
VALUES 
    ('Room 1', 20),
    ('Room 2', 30),
    ('Room 3', 25),
    ('Room 4', 15);
