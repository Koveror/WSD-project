# WSD 2018 Project

Project repository for web software development course 2018

* Virva Norja 619925
* Niko Aarnio 523707
* Risto Koverola 479699

### Implemented features

* Authentication:
Login, logout, register and email validation were all implemented using django auth.
Email validation is done using django's console backend, so the confirmation email is posted directly on the site.
We had some problems when thinking about a sensible user model, but using the django default user model proved to be sufficient.
We think the implemantation is worth 200 points.

* Basic player functionalities:
Players can buy games and play games.
Players can also filter games by genres both in the shop and in owned games.
Sufficient security checks are in place.
We think the implementation is worth 300 points.

* Basic developer functionalities:
Developers can add games and set their price and modify them later in whatever way they want.
Developers can see their own games in the developer view and check detailed statistics for each one.
Security checks are in place.
Removal of games is not possible with the current implementation.
We think the implementation is worth 175 points.

* Game/service interaction:
The service listens to the game and high scores are recorded.
Scores are tracked to individual players and are displayed as a global highscore list.
Messages from the service to the game are implemented as well.
Implementing the game service interaction was problematic, since ajax was a bit complicated.
We think the implementation is worth 200 points.

* Quality of Work:
The quality of code in this project is overall good.
It is structured as a single app and different components are seperated into files of their own as necessary. Comments are used when appropriate.
The framework is used purposefully and concerns are seperated.
We decided to use class based views for our implementations and they turned out to be challenging and often unecessarily complicated.
We have paid attention to the user experience and we think interaction with the service works well.
We have styled the front end with bootstrap and our own css.
We created some unit tests, but we could have used more.
In the end not a whole lot of attention was given to the unit tests.
We think the quality of our work is worth 75 points.

* Non-functional requirements:
Project plan was delivered in time.
All the required documentation was provided and teamwork was well balanced and split between the team members.
We think for non-functional requirements we should get 200 points.

* Save/load and resolution feature:
Save and load features were implemented according to specification.
Resolution feature was not implemented.
Saving and loading was problematic mostly because of json formatting.
We think the implementation is worth 85 points.

* RESTful API:
RESTful API was implemented. It can be queried for games available in the shop.
We think the implementation is worth 100 points.

* Mobile Friendly:
Our implementation of the service is mobile friendly.
We used bootstrap to achieve a scalable front end.
We tested it with developer tools and mobile devices.
We think the implementation is worth 50 points.

### Responsibilities of the team members
We worked face-to-face each week and each member of the team picked features they would like to implement. We tried not get into specific roles or areas of expertise, but some division was there.
Niko worked most on the front-end, while Risto and Virva worked on back end. Heroku deployment and management was handled by Risto.

### Instructions
Our application can be accessed at:
https://frozen-meadow-25693.herokuapp.com/home

Out api can be queried for all games available in the shop at:
https://frozen-meadow-25693.herokuapp.com/game_api

The usage of the application should be self explanatory.
When registering a new account, the validation email is provided as a message on the web page.
To activate a new account, simply follow the provided link.
All users can become developers when registering or later by clicking the developer tab.
All users can play and buy games.