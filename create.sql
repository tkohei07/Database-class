drop table if exists Item;
drop table if exists User;
drop table if exists Category;
drop table if exists Bids;

CREATE TABLE User
(
  userID CHAR(30) NOT NULL,
  rating INTEGER NOT NULL,
  location CHAR(30),
  country CHAR(30),
  PRIMARY KEY (userID)
);

CREATE TABLE Item
(
  itemID INTEGER NOT NULL,
  name CHAR(30) NOT NULL,
  currently REAL(30) NOT NULL,
  Buy_Price REAL(30),
  first_bid REAL(30) NOT NULL,
  num_of_bids INTEGER NOT NULL,
  description CHAR(1024) NOT NULL,
  auction_start NUMERIC(30) NOT NULL,
  auction_end NUMERIC(30) NOT NULL,
  userID CHAR(30) NOT NULL,
  PRIMARY KEY (itemID),
  FOREIGN KEY (userID) REFERENCES User(userID)
);

CREATE TABLE Category
(
  category_name CHAR(30) NOT NULL,
  itemID CHAR(30) NOT NULL,
  FOREIGN KEY (itemID) REFERENCES Item(itemID)
);

CREATE TABLE Bids
(
  time NUMERIC(30) NOT NULL,
  amount REAL(30) NOT NULL,
  itemID INTEGER NOT NULL,
  userID CHAR(30) NOT NULL,
  PRIMARY KEY (itemID, time),
  FOREIGN KEY (itemID) REFERENCES Item(itemID)
);

