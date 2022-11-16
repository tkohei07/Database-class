select count(distinct(Item.userID)) as sol6 from Item, Bids 
where Item.userID = Bids.userID;