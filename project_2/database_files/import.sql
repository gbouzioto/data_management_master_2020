// load Address table
load csv with headers from 'file:///2016_address.csv' as row
merge (address:Address {address_id: toInteger(row.address_id)})
on create set address.country = row.country;

// load Publisher table
load csv with headers from 'file:///2016_publisher.csv' as row
merge (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
on create set publisher.name = row.name;

// load Book table
load csv with headers from 'file:///2016_book.csv' as row
merge (book:Book {book_id: toInteger(row.book_id)})
on create set book.isbn = row.isbn, book.current_price = toFloat(row.current_price), book.title = row.title, book.publication_year = toInteger(row.publication_year);

// load Author table (file is too big so load only 50000 rows)
load csv with headers from 'file:///2016_author.csv' as row
with row limit 50000
merge (author:Author {author_id: toInteger(row.author_id)})
on create set author.name = row.name, author.gender = row.gender, author.nationality = row.nationality;

// load Review table (file is too big so load only 50000 rows)
load csv with headers from 'file:///2016_review.csv' as row
with row limit 50000
merge (review:Review {review_id: toInteger(row.review_id)})
on create set review.timestamp = row.created, review.score = row.score;

// load User table
load csv with headers from 'file:///2016_user.csv' as row
merge (user:User {user_id: toInteger(row.user_id)})
on create set user.username = row.username, user.email = row.email, user.real_name = row.real_name;

// load Order table
load csv with headers from 'file:///2016_order.csv' as row
merge (order:Order {order_id: toInteger(row.order_id)})
on create set order.placement = row.placement, order.completed = row.completed;

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
schema await

// add edges

// add HAS_HEADQUARTERS_IN edges for Publishers
load csv with headers from 'file:///2016_publisher.csv' as row
match (address:Address {address_id: toInteger(row.address_id)})
match (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
merge (publisher)-[:HAS_HEADQUARTERS_IN]->(address)

// add HAS_ADDRESS edges for Users (a user can have many addresses)
load csv with headers from 'file:///2016_user_address.csv' as row
match (address:Address {address_id: toInteger(row.address_id)})
match (user:User {user_id: toInteger(row.user_id)})
merge (user)-[:HAS_ADDRESS]->(address)

// add PUBLISHED_BY edges
load csv with headers from 'file:///2016_book.csv' as row
match (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
match (book:Book {book_id: toInteger(row.book_id)})
merge (book)-[:PUBLISHED_BY]->(publisher)

// add HAS_ORDERED and SHIPPED_TO edges
load csv with headers from 'file:///2016_order.csv' as row
match (user:User {user_id: toInteger(row.user_id)})
match (address:Address {address_id: toInteger(row.shipping_address_id)})
match (order:Order {order_id: toInteger(row.order_id)})
merge (user)-[:HAS_ORDERED]->(order)
merge (order)-[:SHIPPED_TO]->(address)

// add AUTHORED_BY edges
load csv with headers from 'file:///2016_book_author.csv' as row
match (author:Author {author_id: toInteger(row.author_id)})
match (book:Book {book_id: toInteger(row.book_id)})
merge (book)-[:AUTHORED_BY]->(author)

// add INCLUDES_BOOK edges
load csv with headers from 'file:///2016_book_order.csv' as row
match (order:Order {order_id: toInteger(row.order_id)})
match (book:Book {book_id: toInteger(row.book_id)})
merge (order)-[:INCLUDES_BOOK]->(book)

// add HAS_REVIEW edges
load csv with headers from 'file:///2016_book_review.csv' as row
match (review:Review {review_id: toInteger(row.review_id)})
match (book:Book {book_id: toInteger(row.book_id)})
merge (book)-[:HAS_REVIEW]->(review)