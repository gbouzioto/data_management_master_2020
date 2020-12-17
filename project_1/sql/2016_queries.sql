-- a) An SQL query that counts all the comic books in your database.
-- b) An SQL query that returns the average review score for the comic book with title “Feynman”.
-- c) An SQL query that returns the ISBNs and titles for all books authored by “Alan Moore” (in any role).
-- d) An SQL transaction that modifies a user’s order by removing a previous order with a new one of the same user.

select count(b.book_id) as book_count
	from 
		"2016_book";

select avg(r.score) as avg_score
	from
		"2016_review" as r,
		"2016_book" as b,
		"2016_book_review" as br
	where
	    b.title ='Feynman' and
		b.book_id = br.book_id and
		r.review_id = br.review_id
	group by
		b.book_id;

select b.isbn, b.title
	from
		"2016_author" as a,
		"2016_book" as b,
		"2016_book_author" as ba
	where
	    a.name ='Alan Moore' and
		b.book_id = ba.book_id and
		a.author_id = ba.author_id;
  
begin transaction;

commit;
