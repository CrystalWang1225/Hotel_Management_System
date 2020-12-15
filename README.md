# Hotel Mangement System
## Final Project for ECE 464 Database

#### A Flask Full-Stack Hotel Management Web System with SQLalchemy, SQLite, Bootstrap, CSS, HTML, Javascript

#### Crystal Yuecen Wang
#### Professor: Eugene Sokolov

### Purpose:
The purpose of the final project is to build an efficient and secure hotel management system that helps the hotel business stay organized and keep information easily accessible. The functionalities involve reservations of rooms, payment transactions, logins for guest booking details, and reservation modifications.

### Interface:
The hotel management system is deployed on a web application using python Flask framework with Bootstrap template frontend page that consists of HTML, CSS and JavaScript. The database part is constructed by ORM with SQLalchemy connected to a SQLite database. The database is populated either by inserting new entries from the webpage or by SQL. The user is able to log in from the web page and reserve rooms from it under proper authentication using sessions. Furthermore, the system allows modification or deletion of reservations. Payment details can be filled out by the user for each specific reservation. The user can also check availability of the rooms available by filling out the checkin and checkout date inside the “Check Availability” tab. If the tab isn’t filled out, it will show all the rooms that this hotel has. The user is able to make reservations through the “Reservation” tab, which specifies your check-in , check-out date, number of guests, and the desired room numbers. The user is allowed to reserve more than one room. The management system will also check for potential errors : reserving a check in date that is in the past; rooms not being available during the time selected; the rooms selected won’t fit the entire number of guests put in for example. Once reservation is successfully made, the user is able to view all their reservations and account information in the “My Account” Tab. From the tab, the user can make decisions on deleting the reservation or updating the reservation, which will also be protected by the availability check system in the backend of the code. The cost of all the rooms per reservation is calculated at the backend and can be viewed in this tab as well. By clicking the payment icon, the url can be redirected to the payment page where the user can enter their credit card information, and we assume here that once the credit card information is filled, the payment status can be confirmed and will be shown in the reservation.

### Prerequisites
All the requirements for the system can installed by 
```
pip install -r requirements.txt
```
### Running the program
The program can be run by 
```
python app.py
```
