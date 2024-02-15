CREATE DATABASE datamining;
USE datamining;

SET SQL_SAFE_UPDATES = 0;

CREATE TABLE User (email_id VARCHAR(500),
				   password VARCHAR(500),
                   PRIMARY KEY (email_id)
                  );

CREATE TABLE Restaurants (rest_id INT NOT NULL,
					rest_name VARCHAR(500),
                    rest_city VARCHAR(50),
                    rest_budget INT NOT NULL,
                    rest_cuisine VARCHAR(500),
					  PRIMARY KEY (rest_id)
					 );


