# Warehouse app 
Authentication and login system with a smart search and query engine in the back-end tier. Simple front-end layer for showing the suitable warehouse options.

## State of the app
****18.05.2022**** - Still designing the UI elements for home, login and register page. \
**18.05.2022** - Added backend for login, signup and logout features. \
**18.05.2022** - Added admin rank to users, working on admin page for adding warehouses. \
**18.05.2022** - Added flash messages, required checkbox in sign up page. \
**19.05.2022** - Deployed postgresql database on heroku. Credentials will be given below. \
**19.05.2022** - Added auto locate features to get location of users(Location is printed on terminal, not on web app yet). \
**20.05.2022** - Added warehouse and warehouse services models. \
**20.05.2022** - Extended admin page, now can edit the warehouses and add them. \
**20.05.2022** - Added prices page in admin panel, can add and change prices of warehouses. \
**21.05.2022** - Fixed small bugs in price change page. \
**21.05.2022** - Added delete button, it deletes warehouse and prices associated. \
**23.05.2022** - Fixed labels overlapping the input fields. \
**23.05.2022** - Fixed buttons inside admin page, more responsive and returns in one click.  \
**23.05.2022** - Added password reset with high security UUID4 token. \
**24.05.2022** - Added merchant and warehouse owner ranks, can choose in registration page. \
**24.05.2022** - Dashboard for warehouse owner, adding their warehouse and editing it. \
**24.05.2022** - Removed admin route, now uses joint route /dashboard, but admin has more options. \
**24.05.2022** - Bug fix, now turning of a feature removes the price associated to it.  \
**25.05.2022** - Added error handling. Gives proper errors incase of misuse or server issues. \
**25.05.2022** - Added static images, links to the home page for each type of users.  \
**26.05.2022** - New profile page, displaying name, surname and email of the user. \
**26.05.2022** - Added username column to user db, can now login with email and username. \
**26.05.2022** - Title changes according to the URL. Small design modifications in dashboard. \
**26.05.2022** - Fixed JS error that blocked me from using JS functions for the last few days. \
**26.05.2022** - New search tab, which displays warehouses to merchant, details page coming soon. \
**27.05.2022** - Photo upload logic is written, not accessible yet, need to get better DB server. \
**27.05.2022** - search/details page displays warehouse info, and button to check availability. \
**27.05.2022** - Small algorithm to check if warehouse has available storage, send email containing information. \
**30.05.2022** - Disabled the process to send email containing information if warehouse has available storage. \
**30.05.2022** - Search tab inside search page, can query through warehouses using name, storage, services and prices. \
**31.05.2022** - Receive merchants address, calculate distance matrix and return back distance and time to destination. \
**31.05.2022** - Sort the warehouses with the temporary array created, which includes time and distance matrix. \ 
**31.05.2022** - Added autocomplete for address field. Now shows similar addresses while user types along. \
**01.06.2022** - Optimized the models by adding association proxy for easily accessing the one to one relationship services table prices. No need to loop everytime, looking if owner ID matches the owner. \
**01.06.2022** - Added filtering by 4 services prices provided by the warehouses. \
**02.06.2022** - Based on checked services options, filtering algorithm queries the warehouses offering not only checked services, but offering single service for more options. \
**02.06.2022** - When services checkboxes are checked, all the warehouses providing that service(not only multiple checked options, but the ones who provides only one of the services) will be shown. Front end now has alcd gorithm to always show the correct results based on filters. \
**02.06.2022** - Search input is now kept in local storage.
**03.06.2022** - Model for booking requests are created, new relationship is created between user and warehouses table.
**03.06.2022** - Demo version of succession process number 3 is deployed. More details below. \
**06.06.2022** - Booking table now automatically sets the date of the request. \
**06.06.2022** - Same merchant can not request a booking on the same warehouse more than once. \
**06.06.2022** - Warehouse owner can now accept the request and view them on new page /dashboard/active-booking. \
**06.06.2022** - Merchant has new dashboard page to view the requested bookings and active ones. **Not finished yet**

## Succession process - DEMO
Demo version for succession process(step 3) is now functional. By clicking the **Request booking** button on warehouse details page, modal component will open where you input all the required fields. I followed succession processes steps closely, with minor changes. Table properties are as described in the document, only that contracted boolean variable is set to NULL at the beginning. Reason for that is, when the warehouse owner rejects the booking request, it will be set to false, and wont be visible to warehouse owner anymore. So in the future, we can use the data, maybe for ML algorithm, more data better results. 
\
\
When merchant fills in the form fields and submits the form, both merchant and warehouse owner receives a mail, with related information. Warehouse owner can go to their dashboard and view booking requests, just basic information such as merchant name, which warehouse is requested, check-in and check-out. By pressing on more details, modal component opens up showing all the details, and there warehouse owner can decide to reject or accept. By rejecting the request, contracted field is set to false, and merchant receives mail saying their request is rejected. 
\
\
**What is missing?**
- Accept button does not work.
- Merchant can not view their requests yet.

## Search page - NEW FEATURES
Old algorithm has been heavily revised, now when you want to see warehouses that offers specific services, lets say merchant checks Labelling and Item packaging. Algorithm will first take in the filters such as name and needed storage. Then it will query the warehouses which offers labelling service. It will keep does warehouses in memory and then will query looking for warehouses that offer palette packaging service. Now we have 2 lists of warehouses objects, and most probably both lists have duplicate warehouses. What our algorithm does, it checks what services were asked for, and then we use except logic to remove the duplicate objects from lists, and at the end we join them all and return it to front end so merchant can see. 
\
\
For prices part, our algorithm creates 2 dictionaries which keeps the minimum and maximum price in memory and 2nd dictionary which keeps booleans to later check if options were true of false. The algorithm described in the previous paragraph works great, but lets say there are 2 warehouses: Warehouse A and B. Warehouse A has labelling priced at €50 and item packaging at €20 and Warehouse B has manual geo data priced at €30 and labelling at €40. When Merchant wants to find warehouses with services labelling prices at minimum €45 and manual geo priced at maximum €35, algorithm will return warehouse A and B, but we see that Warehouse B has labelling service which is priced below the given minimum price. So the algorithm created in the front end checkes two dictionaries to determine the which prices to show.


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

