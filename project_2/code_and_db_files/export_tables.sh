SCHEMA="public"
DB="comic_books"

psql -Atc "select tablename from pg_tables where schemaname='$SCHEMA'" $DB |\
  while read -r TBL; do
    if [ "$TBL" = "2016_address" ]; then
      psql -c "COPY \"$TBL\"(address_id,address_name,address_number,country) TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    elif [ "$TBL" = "2016_publisher" ]; then
      psql -c "COPY \"$TBL\"(publisher_id,name,address_id) TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    elif [ "$TBL" = "2016_book" ]; then
      psql -c "COPY \"$TBL\"(book_id,isbn,current_price,publication_year,title,publisher_id) TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    elif [ "$TBL" = "2016_user" ]; then
      psql -c "COPY \"$TBL\"(user_id,username,email,real_name) TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    elif [ "$TBL" = "2016_review" ]; then
      psql -c "COPY \"$TBL\"(review_id,created,score) TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    else
      psql -c "COPY \"$TBL\" TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
    fi
  done