select I1.itemID as sol4 from Item I1
where I1.currently = (select Max(I2.currently) from Item I2);