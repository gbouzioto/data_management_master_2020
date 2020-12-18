-- a) An SQL query that counts all the comic books in your database.
-- b) An SQL query that returns the average review score for the comic book with title “Feynman”.
-- c) An SQL query that returns the ISBNs and titles for all books authored by “Alan Moore” (in any role).
-- d) An SQL transaction that modifies a user’s order by removing a previous order with a new one of the same user.

select count(book_id) as book_count
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

with q1 as (delete from "2016_book_order" 
	where order_id in (
					    select order_id
					    from "2016_order"
					    where user_id in
					          (select distinct u.user_id
					           from "2016_user" as u,
					                "2016_order" as o,
					                "2016_book_order" as bo,
					                "2016_user_address" as ua,
					                "2016_address" as a,
					                "2016_book" as b
					           where u.user_id = ua.user_id
					             and a.address_id = ua.address_id
					             and u.user_id = o.user_id
					             and o.order_id = bo.order_id
					             and b.book_id = bo.book_id
					           limit 1
      						)
					    order by order_id DESC
					    limit 1
					) returning order_id),
	q2 as (delete from "2016_order"
			where order_id in (select q1.order_id from q1) returning user_id, billing_address_id, shipping_address_id),
	q3 as (insert into "2016_order" (user_id, billing_address_id, shipping_address_id, placement)
			select q2.user_id, q2.billing_address_id, q2.shipping_address_id, now() from q2 returning order_id)
	insert into "2016_book_order" (book_id, order_id) select (select book_id from "2016_book" limit 1), q3.order_id from q3;

commit;