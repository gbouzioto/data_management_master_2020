// load Address table
load csv with headers from 'file:///2016_address.csv' as row
create (address:Address {address_id: toInteger(row.address_id), country: row.country});

// load Publisher table
load csv with headers from 'file:///2016_publisher.csv' as row
create (publisher:Publisher {publisher_id: toInteger(row.publisher_id), name: row.name});

// load Book table
load csv with headers from 'file:///2016_book.csv' as row
create (book:Book {book_id: toInteger(row.book_id), isbn: row.isbn, current_price: toFloat(row.current_price), title: row.title, publication_year: toInteger(row.publication_year)});

// load Author table (note that this needs to be run separately in neo4j broswer as it does not support auto transactions in multi statement query editor)
:auto using periodic commit 50000 load csv with headers from 'file:///2016_author.csv' as row
create (author:Author {author_id: toInteger(row.author_id), name: row.name, gender: row.gender, nationality: row.nationality});

// load Review table (note that this needs to be run separately in neo4j broswer as it does not support auto transactions in multi statement query editor)
:auto using periodic commit 50000 load csv with headers from 'file:///2016_review.csv' as row
create (review:Review {review_id: toInteger(row.review_id), timestamp: row.created, score: row.score});

// load User table
load csv with headers from 'file:///2016_user.csv' as row
create (user:User {user_id: toInteger(row.user_id), username: row.username, email: row.email, real_name: row.real_name});

// load Order table and assign current datetime to completed field if it is null
load csv with headers from 'file:///2016_order.csv' as row
create (order:Order {order_id: toInteger(row.order_id), placement: row.placement, completed: coalesce(row.completed, datetime())});

// add constraints
CREATE INDEX address_id FOR (address:Address) ON (address.address_id);
CREATE INDEX publisher_id FOR (publisher:Publisher) ON (publisher.publisher_id);
CREATE INDEX book_id FOR (book:Book) ON (book.book_id);
CREATE INDEX isbn FOR (book:Book) ON (book.isbn);
CREATE INDEX author_id FOR (author:Author) ON (author.author_id);
CREATE INDEX review_id FOR (review:Review) ON (review.review_id);
CREATE INDEX user_id FOR (user:User) ON (user.user_id);
CREATE INDEX username FOR (user:User) ON (user.username);
CREATE INDEX email FOR (user:User) ON (user.email);
CREATE INDEX order_id FOR (order:Order) ON (order.order_id);

// add edges

// add HAS_HEADQUARTERS_IN edges for Publishers
load csv with headers from 'file:///2016_publisher.csv' as row
match (address:Address {address_id: toInteger(row.address_id)})
match (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
create (publisher)-[:HAS_HEADQUARTERS_IN]->(address);

// add HAS_ADDRESS edges for Users (a user can have many addresses)
load csv with headers from 'file:///2016_user_address.csv' as row
match (address:Address {address_id: toInteger(row.address_id)})
match (user:User {user_id: toInteger(row.user_id)})
create (user)-[:HAS_ADDRESS]->(address);

// add PUBLISHED_BY edges
load csv with headers from 'file:///2016_book.csv' as row
match (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
match (book:Book {book_id: toInteger(row.book_id)})
create (book)-[:PUBLISHED_BY]->(publisher);

// add HAS_ORDERED and SHIPPED_TO edges
load csv with headers from 'file:///2016_order.csv' as row
match (user:User {user_id: toInteger(row.user_id)})
match (address:Address {address_id: toInteger(row.shipping_address_id)})
match (order:Order {order_id: toInteger(row.order_id)})
create (user)-[:HAS_ORDERED]->(order);
create (order)-[:SHIPPED_TO]->(address);

// add AUTHORED_BY edges
load csv with headers from 'file:///2016_book_author.csv' as row
match (author:Author {author_id: toInteger(row.author_id)})
match (book:Book {book_id: toInteger(row.book_id)})
create (book)-[:AUTHORED_BY]->(author);

// add INCLUDES_BOOK edges
load csv with headers from 'file:///2016_book_order.csv' as row
match (order:Order {order_id: toInteger(row.order_id)})
match (book:Book {book_id: toInteger(row.book_id)})
create (order)-[:INCLUDES_BOOK]->(book);

// add HAS_REVIEW edges
load csv with headers from 'file:///2016_book_review.csv' as row
match (review:Review {review_id: toInteger(row.review_id)})
match (book:Book {book_id: toInteger(row.book_id)})
create (book)-[:HAS_REVIEW]->(review);