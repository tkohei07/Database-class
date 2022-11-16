select count(*) as sol3 from (
select count(itemID) as cnt from category group by ItemID
having cnt = 4 );