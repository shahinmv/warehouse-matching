# Warehouse app 
Authentication and login system with a smart search and query engine in the back-end tier. Simple front-end layer for showing the suitable warehouse options.

## State of the app
18.05.2022 - Still designing the UI elements for home, login and register page. \
18.05.2022 - Added backend for login, signup and logout features. \
18.05.2022 - Added admin rank to users, working on admin page for adding warehouses. \
18.05.2022 - Added flash messages, required checkbox in sign up page. \
19.05.2022 - Deployed postgresql database on heroku. Credentials will be given below. \
19.05.2022 - Added auto locate features to get location of users(Location is printed on terminal, not on web app yet). \
20.05.2022 - Added warehouse and warehouse services models. \
20.05.2022 - Extended admin page, now can edit the warehouses and add them. \
20.05.2022 - Added prices page in admin panel, can add and change prices of warehouses. \
21.05.2022 - Fixed small bugs in price change page. \
21.05.2022 - Added delete button, it deletes warehouse and prices associated. \
23.05.2022 - Fixed labels overlapping the input fields. \
23.05.2022 - Fixed buttons inside admin page, more responsive and returns in one click.  \
23.05.2022 - Added password reset with high security UUID4 token. \
24.05.2022 - Added merchant and warehouse owner ranks, can choose in registration page. \
24.05.2022 - Dashboard for warehouse owner, adding their warehouse and editing it. \
24.05.2022 - Removed admin route, now uses joint route /dashboard, but admin has more options. \
24.05.2022 - Bug fix, now turning of a feature removes the price associated to it.  \
25.05.2022 - Added error handling. Gives proper errors incase of misuse or server issues. \
25.05.2022 - Added static images, links to the home page for each type of users.  \
26.05.2022 - New profile page, displaying name, surname and email of the user. \
26.05.2022 - Added username column to user db, can now login with email and username. \
26.05.2022 - Title changes according to the URL. Small design modifications in dashboard. \
26.05.2022 - Fixed JS error that blocked me from using JS functions for the last few days. \
26.05.2022 - New search tab, which displays warehouses to merchant, details page coming soon. \
27.05.2022 - Photo upload logic is written, not accessible yet, need to get better DB server. \
27.05.2022 - search/details page displays warehouse info, and button to check availability. \
27.05.2022 - Small algorithm to check if warehouse has available storage, send email containing information. \
30.05.2022 - Disabled the process to send email containing information if warehouse has available storage. \
30.05.2022 - Search tab inside search page, can query through warehouses using name, storage, services and prices. \
31.05.2022 - Receive merchants address, calculate distance matrix and return back distance and time to destination. \
31.05.2022 - Sort the warehouses with the temporary array created, which includes time and distance matrix. \ 
31.05.2022 - Added autocomplete for address field. Now shows similar addresses while user types along. \
01.06.2022 - Optimized the models by adding association proxy for easily accessing the one to one relationship services table prices. No need to loop everytime, looking if owner ID matches the owner. 
01.06.2022 - Added filtering by 4 services prices provided by the warehouses.

## Not working
- Google and facebook authentication.

## To do
- Organize the directory.

## Technologies

- Flask framework 
- Flask SQL Alchemy
- Bootstrap 5.1.3
- Material Design 4.0.0
- PostgreSQL
- Heroku
- Google Maps API
- Ajax

## Access to database
**Host**:      ec2-54-76-43-89.eu-west-1.compute.amazonaws.com \
**Database**:  d1s5qe2312f8bg \
**Post**:      5432 \
**Username**:  fnqgcgvmozpmyl \
**Password**:  f28265da2ca5f4fddc9de7e25e5cf8c7c06c95739d5d2ce3c4275d0fb3cc922f 

## Access the website
- [HERE](warehouse-thesis.herokuapp.com)
## Usage

```python
python run.py
```

