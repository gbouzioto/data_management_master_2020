SCHEMA="public"
DB="comic_books"

psql -Atc "select tablename from pg_tables where schemaname='$SCHEMA'" $DB |\
  while read -r TBL; do
    psql -c "COPY \"$TBL\" TO STDOUT WITH CSV HEADER" $DB > "$TBL.csv"
  done