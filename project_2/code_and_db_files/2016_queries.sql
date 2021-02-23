match (author)<-[:AUTHORED_BY]-(book)-[:PUBLISHED_BY]->(publisher)-[:HAS_HEADQUARTERS_IN]->(address {country: 'France'}) return book, author;
match p = (user)-[:HAS_ORDERED]->(order) with user, count(relationships(p)) as rels where rels >= 5 return user, rels order by rels desc;
