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
23.05.2022 - Added password reset with high security UUID4 token.

## Not working
- Google and facebook authentication.
- Forgot password.
- Get location - works in the backend, not visible to the user.
- When value is null, exception is thrown

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
**Host**:      ec2-52-48-159-67.eu-west-1.compute.amazonaws.com \
**Database**:  d22qmtgc4978dh \
**Post**:      5432 \
**Username**:  yqquhofwbxigmm \
**Password**:  d2f6ddf9087969303f5eedf87b5e124060d4b25532ff0358f830b70ed9045b62 

## Access the website
- [HERE](warehouse-thesis.herokuapp.com)
## Usage

```python
python run.py
```

