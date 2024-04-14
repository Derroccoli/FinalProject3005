Contributors:
- Kai Sundararaj 101240325
- Derrick Zhang 101232374

Youtube video: https://youtu.be/KDfnUDlImFc

Overall Assumptions
- Trainers manage their schedule and set when they’re available, admins use this info to book classes, members use this schedule to book
- Assume that logging in is done without password
- Assume that payment is done without credit card
- Assume that trainers and admins cannot register as this was not specified in the specifications
- Assume there are no refunds
- Assume there is no need for members to deregister from group classes as it was not specified in the specs
- Assume a member profile when searched by a trainer is their info, fitness goals, and health metrics
- Assume that once a fitness goal is complete it becomes a fitness achievements

CHANGED: DDL AND DML are found in the SQL sub folder


FOR LINKS, CONTROL CLICK ON THE LINK

2.1
ER Diagram: Click [here](ER_Model.drawio.png) to view the ER Diagram.

This database is designed to hold all of the required information to keep track of for a fitness app. The app has three types of users: members, trainers, and admins.

Our program can do everything listed in the problem statement and required functions

Assumptions for database design
- Most things are self explanatory or talked about in video
- Assume members don't need to have group_fitness, pt_session, exercises, achievements, fitness_goals, health_metrics, bills, but all of those need a member
- Assume members can have multiple of all those things, and all those things can have 1 member (except for group_fitness)
- Assume all pt_sessions, group_fitness, and available_times (schedule) have a trainer, but not every trainer has one of those
- Assume those things have one trainer apiece, whereas trainers can have multiple of those
- Assume one payment has one bill and vice versa, assume all payments have a bill, but not all bills have a payment
- Assume all room_bookings need a room, but not all rooms need a room_bookings
- Assume each room_booking has one room, but each room can have many room bookings
- Assumed admins aren't really related to anything in database
- Assumed equipments aren't really related to anything in database





2.2: 
Relational Schema: Click [here](RelationSchema.drawio.png) to view the Relational Schema.



2.3 
DDL File: Click [here](SQL/DDL%20setup.sql) to view the DDL File.



2.4
DML File: Click [here](SQL/DML%20setup.sql) to view the DML File.

2.5
Our application is a command line interface
Our application was made using python
Our application uses a Postgresql SQL database to store information

2.6 
Optional

2.7
Github link: https://github.com/Derroccoli/FinalProject3005
