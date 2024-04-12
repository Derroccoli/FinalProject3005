CREATE TABLE members (
	member_id SERIAL PRIMARY KEY,
	firstName TEXT NOT NULL,
	lastName TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone_number TEXT NOT NULL UNIQUE,
	date_registered DATE NOT NULL
);


CREATE TABLE trainers (
	trainer_id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT
);


CREATE TABLE fitness_goals (
	fitness_id SERIAL PRIMARY KEY,
	member_id INT NOT NULL,
	description TEXT,
	completed BIT,
	FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE achievements (
	achievement_id SERIAL PRIMARY KEY,
	member_id INT,
	date_of_accomplishment DATE,
	feat TEXT,
	FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE health_metrics (
	metric_id SERIAL PRIMARY KEY,
	member_id INT NOT NULL,
	recorded_date DATE NOT NULL,
	metric_type TEXT NOT NULL,
	value TEXT NOT NULL,
	FOREIGN KEY (member_id) REFERENCES members(member_id)
	
);

CREATE TABLE exercises (
	routine_id SERIAL PRIMARY KEY,
	member_id INT NOT NULL,
	date_of_routine DATE,
	exercise TEXT,
	sets INT,
	reps INT,
	duration INT,
	FOREIGN KEY (member_id) REFERENCES members(member_id)
);


CREATE TABLE pt_session(
	session_id SERIAL PRIMARY KEY,
	member_id INT,
	trainer_id INT NOT NULL,
	session_type TEXT NOT NULL,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	FOREIGN KEY (member_id) REFERENCES members(member_id),
	FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);


CREATE TABLE group_fitness(
	group_id SERIAL PRIMARY KEY,
	trainer_id INT NOT NULL,
	class_name TEXT NOT NULL,
	description TEXT NOT NULL,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);


CREATE TABLE group_members (
    group_id INT,
    member_id INT,
    FOREIGN KEY (group_id) REFERENCES group_fitness (group_id),
    FOREIGN KEY (member_id) REFERENCES members (member_id),
    PRIMARY KEY (group_id, member_id)
);


CREATE TABLE bills(
	bill_id SERIAL PRIMARY KEY,
	amount INT NOT NULL,
	member_id INT,
	FOREIGN KEY (member_id) REFERENCES members(member_id)

);

CREATE TABLE payments(
	pay_id SERIAL PRIMARY KEY,
	bill_id INT,
	amount INT,
	date DATE,
	processed BIT,
	FOREIGN KEY (bill_id) REFERENCES bills(bill_id)

);


CREATE TABLE admin_staff(
	staff_id SERIAL PRIMARY KEY,
	firstName TEXT NOT NULL,
	lastName TEXT NOT NULL,
	email TEXT NOT NULL
);


CREATE TABLE equipments(
	equipment_id SERIAL PRIMARY KEY,
	equipment_type TEXT NOT NULL,
	description TEXT NOT NULL,
	maintenance_date DATE
);


CREATE TABLE rooms(
	room_id SERIAL PRIMARY KEY,
	room_name TEXT NOT NULL,
	room_capacity INT NOT NULL
);

CREATE TABLE room_bookings(
	room_booking_id SERIAL PRIMARY KEY,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	room_id INT NOT NULL,
	FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);



CREATE TABLE available_times(
	availability_id SERIAL PRIMARY KEY,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	booked BOOLEAN NOT NULL,
	trainer_id INT NOT NULL,
	FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
)











