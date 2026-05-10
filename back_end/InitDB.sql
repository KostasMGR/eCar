drop database if exists eCar_db;
create database eCar_db;
use eCar_db;

create table cars(car_id int(8) auto_increment primary key,
brand varchar(13) not null,
model varchar(34) not null,
production_year year not null,
license_plate char(7) unique,
seats int(1) not null,
doors int(1) not null,
cc int(4),
state Enum('Available', 'In_Service', 'Unavailable') default 'Available',
car_description tinytext,
fuel_type Enum('Gas', 'Diesel', 'Hybrid', 'Electric'),
transmission_type enum('Manual', 'Auto'),
horsepower int(4),
image_path varchar(255),
price decimal(6,1) not null,
availability boolean default true);  

create table users(user_id int(3) primary key auto_increment,
username varchar(255) not null,
user_password varchar(255) not null,
user_role enum('Admin', 'Dealer', 'Customer') default 'Customer',
first_name varchar(40) not null,
surname varchar(40) not null,
email varchar(39) unique,
phone_number varchar(15),
registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
license_number varchar(20) unique,
license_type varchar(3));
 
 create table reservations(reservation_id int auto_increment primary key,
 car_id int(8),
 user_id int(3) not null,
 start_date datetime,
 end_date datetime,
 total_price decimal(6,1),
 reservation_status varchar(21) not null,
 FOREIGN KEY (Car_ID) REFERENCES cars(Car_ID) ON DELETE RESTRICT,
 FOREIGN KEY (User_ID) REFERENCES users(User_ID) ON DELETE CASCADE);

INSERT INTO cars 
(brand, model, production_year, license_plate, seats, doors, cc, state, car_description, fuel_type, transmission_type, horsepower, image_path, price, availability)
VALUES
('Toyota', 'Corolla', 2020, 'ABC1234', 5, 4, 1600, 'Available', 'Reliable compact sedan', 'Gas', 'Manual', 132, 'ABC1234', 45.0, TRUE),

('Tesla', 'Model 3', 2022, 'TES5678', 5, 4, NULL, 'Available', 'Electric sedan with autopilot', 'Electric', 'Auto', 283, 'TES5678', 120.0, TRUE),

('Volkswagen', 'Golf', 2019, 'GOL9012', 5, 4, 1400, 'In_Service', 'Popular hatchback', 'Gas', 'Manual', 125, 'GOL9012', 40.0, FALSE),

('BMW', 'X5', 2021, 'BMW3456', 5, 5, 3000, 'Unavailable', 'Luxury SUV', 'Diesel', 'Auto', 265, 'BMW3456', 150.0, FALSE),

('Hyundai', 'i20', 2018, 'HYU7890', 5, 4, 1200, 'Available', 'Economic city car', 'Gas', 'Manual', 84, 'HYU7890', 30.0, TRUE);


INSERT INTO users
(username, user_password, user_role, first_name, surname, email, phone_number, license_number, license_type)
VALUES
('john_doe', 'pass123', 'Customer', 'John', 'Doe', 'john@email.com', '6900000001', 'LIC12345', 'B'),

('alice_smith', 'pass123', 'Customer', 'Alice', 'Smith', 'alice@email.com', '6900000002', 'LIC67890', 'B'),

('mike_brown', 'pass123', 'Customer', 'Mike', 'Brown', 'mike@email.com', '6900000003', 'LIC54321', 'B');

INSERT INTO reservations
(car_id, user_id, start_date, end_date, total_price, reservation_status)
VALUES

-- Toyota Corolla (car_id = 1)
(1, 1,
'2026-05-15 10:00:00',
'2026-05-18 10:00:00',
135.0,
'Confirmed'),

-- Tesla Model 3 (car_id = 2)
(2, 2,
'2026-05-20 09:00:00',
'2026-05-25 09:00:00',
600.0,
'Confirmed'),

-- Hyundai i20 (car_id = 5)
(5, 3,
'2026-05-12 14:00:00',
'2026-05-14 14:00:00',
60.0,
'Pending'),

-- Another reservation for Corolla
(1, 2,
'2026-05-22 08:00:00',
'2026-05-24 08:00:00',
90.0,
'Confirmed'),

-- Cancelled reservation (should NOT block availability)
(2, 1,
'2026-05-28 10:00:00',
'2026-05-30 10:00:00',
240.0,
'Cancelled');