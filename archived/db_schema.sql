CREATE TABLE Event(
	EID INT AUTO_INCREMENT,
	event_name VARCHAR(50) NOT NULL,
	event_date VARCHAR(15) NOT NULL,
	event_place VARCHAR(50) NOT NULL,
	event_sport VARCHAR(50) NOT NULL,
	PRIMARY KEY (EID)
);

CREATE TABLE EventHasUser(
	EUID INT AUTO_INCREMENT,
	EID INT,
	user_name VARCHAR(20) NOT NULL,
	FOREIGN KEY (EID) REFERENCES Event (EID) ON DELETE NO ACTION,
	PRIMARY KEY (EUID)
);


INSERT INTO Event(event_name, event_date, event_place, event_sport)
VALUES ('test event', '05/01/2022', 'Benson', 'tennis');