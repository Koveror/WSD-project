# Project plan

## 1. Team
 * Virva Norja 619925
 * Niko Aarnio 523707
 * Risto Koverola 479699

## 2. Planned features 

We plan to implement all the functional requirements listed in the project description.

* Authentication

* Basic player functionalities

* Basic developer functionalities

* Game/service interaction

* Quality of Work

* Quality of code

In addition we want to implement the following extra features,

* RESTful API

* Mobile Friendly

* 3rd party login

## 3. Unlisted features

During the planning phase we did not come up with any extra features. We will stick to the features listed above unless we come up with something during implementation.

## 4. Feature implementation

### Authentication

We will use Django auth for authentication, registering users, logging in and logging out. We will also implement email authentication.

### Basic player functionalities

When a game is bought it will be associated to the user in the database. Security checks will be put into place to allow users to only play the games they own.

As a minimum viable solution we will have the games in an unordered list. We will add features such as sorting, genres and game search as possible.

### Basic developer functionalities

Each game will have statistics assosiated with it. The statistics can be queried from the database. Each game will also have its own developer which can modify it.

### Game/service interaction

We will have a highscore table in the database. The service will save/query the highscore table when needed. The games themselves will only post messages to the service if the highscores need to be updated.

We will use postMessage method to communicate between game and the service. The messages will be implemented using the specification in the project description document.

### Quality of Work

We will try to use a linter, for example pylint, to assure the quality of the code. Validators for HTML and CSS should be used as well. We will use comments in a normal fashion. Refactoring is done as necessary.

We will try to use the framework correctly. This also means seperating pieces of code into their own functions and objects as the codebase grows to assure speration of concerns and dry principle.

We will use a javascript library, for example bootsrap, to create our user interface. This in itself will help in producing a good user experience.

We will use the built in django test framework for our unit tests. We will write unit tests for our most important methods.

### RESTful API

We will look into creating a REST API for our gamestore. A minimum implementation will allow to query the highscores table information.

### Mobile Friendly

We will use a javascript library such as bootstrap to implement our user interface. As a bonus, it should work on mobile devices without significant extra work.

### 3rd party login

We will use a third party django app that implements login.

## 5. Working on the project

We will try to meet twice a week to work on the project face-to-face and use 6-8 hours per week on the project. For project management we will use trello. The telegram channel of the group is used for general communication.

## 6. Models
We will have the following models with the following fields. The structure will be modified as needed.

### User:
* UserId int (PK)
* UserName varchar
* Password varchar
* Email varchar

### Developer:
* DeveloperId int (PK)
* Username varchar
* Password varchar

### Score: 
* UserId int (FK)
* GameId int (FK)
* Score int
* Timestamp datetime

### Game:
* GameId int (PK)
* Name varchar
* DeveloperId int (FK)
* Price decimal
* NumberSold int
* Genre varchar
* DateCreated datetime

### GameState:
* UserId int (FK)
* GameId int (FK)
* GameState textfield
* TimeStamp datetime

### Purchases:
* UserId int (FK)
* GameId int (FK)


## 7. Timetable

The estimate for our projects timetable is as follows:

* Start of implementation 2.1
* First deployment to heroku 11.1
* Functional requirements done 8.2
* Final submission 19.2