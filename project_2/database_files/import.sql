-- load Address table with country
load csv with headers from 'file:///2016_address.csv' as row
merge (address:Address {address_id: toInteger(row.address_id)})
on create set address.country = toString(row.country);

-- load Publisher table and create the lives in edges
load csv with headers from 'file:///2016_publisher.csv' as row
match (address:Address {address_id: toInteger(row.address_id)})
merge (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
merge (publisher)-[:LIVES_IN]->(address)
on create set publisher.name = toString(row.name);

-- load Book table and create the published by edges
load csv with headers from 'file:///2016_book.csv' as row
match (publisher:Publisher {publisher_id: toInteger(row.publisher_id)})
merge (book:Book {book_id: toInteger(row.book_id)})
merge (book)-[:PUBLISHED_BY]->(publisher)
on create set book.isbn = row.isbn, book.current_price = toFloat(row.current_price), book.title = row.title, book.publication_year = toInteger(row.publication_year);

-- add constraints
CREATE INDEX address_id FOR (address:Address) ON (address.address_id);
CREATE INDEX publisher_id FOR (publisher:Publisher) ON (publisher.publisher_id);
CREATE INDEX book_id FOR (book:Book) ON (book.book_id);
CREATE CONSTRAINT ON (book:Book) ASSERT book.isbn IS UNIQUE;
