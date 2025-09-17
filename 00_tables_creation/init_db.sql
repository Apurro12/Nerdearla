CREATE TABLE user_info (
	user_id INTEGER,
	age INTEGER,
	gender TEXT,
	name TEXT,
	lastname TEXT
);
CREATE TABLE sell_info (
	user_id INTEGER,
	item_id INTEGER,
	date INTEGER,
	value INTEGER
);
CREATE TABLE items_info (
	item_id INTEGER, 
	item_name TEXT, 
	category TEXT
);
INSERT INTO sell_info (user_id, item_id, date, value ) values (1,1,1,1),(2,2,2,1),(3,3,3,1),(1,2,1,1),(1,3,2,1),(2,3,3,3);
INSERT INTO items_info (item_id, item_name, category) values (1,"item1","toys"), (2,"item2","toys"),(3,"item3","food");
INSERT INTO user_info (user_id, age, gender, name, lastname) values (1, 10,"M","person-1-name","person-1-lastname"), (2, 15,"M","person-2-name","person-2-lastname"),(3, 20,"F","person-3-name","person-3-lastname");