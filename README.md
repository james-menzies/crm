# Membership-Based CRM 

I know what you may be thinking... **_another_** CRM?? Why on Earth would this be useful? 

**_Well..._**

The desire to create this project stems from needs of a friend of mine, who needs a modest way to track their sales at work. Of all the approaches that could be taken, it was apparent that none really cater for that need. Here's why:
* Proprietary systems are prohibitively expensive.
* Existing solutions are too complex.
* Spreadsheets don't quite cut it.
* Learning something like Microsoft Access is way too much effort. 

The aim with this project is to realise an application which can suit that need, using completely open-source tools and frameworks. 

## Primary Goals

The key goals for this software are simple:

* Keep track of client information.
* Keep track of products that can be offered.
* Keep track of orders made by clients.
* Expose some way of extracting data about the above via some kind of dashboard.

There are however some curve balls:

* Clients can either be **_members_** or **_non-members_**. 
* For every product, there are two price points based on whether or not the client is a member. 
* A membership can be sold to a client as part of an order.
* In that event, the membership takes effect **_immediately_** and a price reduction applies to that order.
* It needs to be clear what the user stands to save by becoming a member in a given order.

It begs that question though, *is a membership a product?* In short no, and the reasons I have to offer for that are as follows:
* A membership has one price, whereas a product has two.
* A membership can only be sold to a non-memmber, a product can be sold to anyone.
* A membership will affect the price of a given order, whereas a product does not.


Therefore, there are 4 major entities that need be managed by the end user; Clients, Products, Orders **and** Memberships.

## Non-Goals

* It is a single-user application. If this application is deployed *"in the wild"*, it will need to be placed behind something like as a reverse proxy server.
* For now it will exist in a desktop-only mode. If there is demand for a mobile version, I'll consider adding one.

## Tech Stack 

I will be using what I call the PDRN stack (Postgres, Django, React, Node). The reason I've done so is because I'm very comfortable with each component of the stack in isolation, but would like some experience in combining the technologies into a single project. I also believe that each element works well in it's own right too:

**React/Node:** Single Page Applications are all the rage right now, and React being by far the most popular Javascript framework makes it an easy choice for the front end of this application. It will be complemented by Redux which will help manage application state and React Router for, you guessed it, routing.

**Postgres:** I feel that a relational database lends itself best to this kind of project given that there will likely be use of making extensive joins when querying the data for statistical purposes. There's also no need to worry about scaling as it's assumed that every implementation will be tracking a single business or system, meaning that it is inherently distributed. PostgresQL was chosen (say, over MYSQL) purely for familiarily.

**Django:** Django is the most funded and robust backend framework in Python as it stands today. It is known for sheer speed when it comes to getting up and running with a backend. I intend to use the Django REST Framework (DRF) to provide data to the front end of the application via and API.

## Mock Ups

As I'm no designer, it would be silly to try and design a user interface from scratch. To that end, I've decided to use Material UI by Google, which is a component library based on Material Design, the same philosophy that exists through most of Google's ecosystem.

There will be 4 main screens that form the application:

* Clients: Client management
* Products: Product **_and_** Membership management.
* Orders: Order searching and management.
* Dashboard: For viewing statistical information.


I've created a rough view of what the application could look like, with the ommission of the dashboard. The reason for this is because it's difficult to determine at this stage what information would be the most useful to convey If you have some ideas I'd be very interested to hear them!


[Click here to view a live version of the prototype.](https://www.figma.com/proto/Fb4F6R6fBhC5aAh4vKRwvU/CRM?page-id=0%3A1&node-id=3%3A10534&viewport=501%2C48%2C0.42&scaling=scale-down&starting-point-node-id=3%3A9845&show-proto-sidebar=1)

Most of it is straightforward to navigate, however here are some extra tips to get the most out of it:

* The three active pages can be navigated to by using the sidebar rather than the nav bar. This is because trying to implement native nagigation via the nav bar itself proved way too fiddly.
* At any point, you can click on the prototype to reveal 'clickable' areas, which will show parts of the prototype that you can interact with. 
* The clients page will contain information about past orders, and the orders page will contain reference to the billed client. These references will be interactive, allowing the user to navigate easily the two entities. 
* The order page will allow the user to dynamically add a membership, and be able to see what the client stands to save by doing so.

## Database

(Coming Soon)

## API Specification

(Coming Soon)

