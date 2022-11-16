select count(distinct(category.category_name)) as sol7 from category inner join bids
on category.itemID = bids.itemID
where bids.amount > 100;