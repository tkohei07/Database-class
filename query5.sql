select count(distinct(item.userID)) as sol5 from item inner join user
on item.userID = user.userID and user.rating > 1000;