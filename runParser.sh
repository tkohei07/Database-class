mkdir -p ./dat
chmod 777 ./dat
rm ./dat/*.dat

python3 ./auction_parser.py ./ebay_data/items-*.json

sort ./dat/Category_temp.dat | uniq > ./dat/Category.dat

rm ./dat/User_temp.dat
rm ./dat/User_duplicate.dat
rm ./dat/Category_temp.dat

