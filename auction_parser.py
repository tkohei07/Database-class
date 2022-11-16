
import sys
import os
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def escape_quotation(string):
    return string.replace('"', '""')

# param duplication : Used in duplicate_elimination_from_User
def write_files(path, data, duplication):
    if not os.path.isfile(path):
        with open(path, mode='w') as f:
            f.write(data)
    elif not duplication:
        with open(path, mode='a') as f:
            f.write('\n' + data)
    else:
        with open(path, mode='a') as f:
            f.write(data)


def output_user(userID, rating, location, country):
    path_w = 'dat/User_duplicate.dat'
    if userID is not None:
        userID = escape_quotation(userID)
    if location is not None:
        location = escape_quotation(location)
    if country is not None:
        country = escape_quotation(country)    
    data = '"{}"|{}|"{}"|"{}"'.format(userID, rating, location, country)
    write_files(path_w, data, False)

def output_item(itemID, name, currently, buyPrice, firstBid, numberOfBids, description, 
    auction_start, auction_end, userID):
    path_w = 'dat/Item.dat'
    if description is not None:
        description = escape_quotation(description)
    if name is not None:
        name = escape_quotation(name)
    if userID is not None:
        userID = escape_quotation(userID)
    data = '{}|"{}"|{}|{}|{}|{}|"{}"|{}|{}|"{}"'.format(itemID, name, currently, buyPrice, firstBid, numberOfBids, 
        description, auction_start, auction_end, userID)
    write_files(path_w, data, False)

def output_category(category, itemID):
    path_w = 'dat/Category_temp.dat'
    if category is not None:
        category = escape_quotation(category)
    data = '"{}"|{}'.format(category, itemID)
    write_files(path_w, data, False)

def output_bids(time, amount, itemID, userID):
    path_w = 'dat/Bids.dat'
    data = '{}|{}|{}|{}'.format(time, amount, itemID, userID)
    write_files(path_w, data, False)


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        # items are all data in a file, item is each auction data(dictionary)
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            # Only outputting a Seller
            # Location, country : whether or not Null
            if item['Location'] is not None:
                temp_location = item['Location']
            else:
                temp_location = None
            if item['Country'] is not None:
                temp_country = item['Country']
            else:
                temp_country = None
            output_user(item['Seller']['UserID'], item['Seller']['Rating'], temp_location, temp_country)

            # Buy_Price : whether or not it is Null
            if 'Buy_Price' in item.keys():
                temp_buy_price = transformDollar(item['Buy_Price'])
            else:
                temp_buy_price = None

            output_item(item['ItemID'], item['Name'], transformDollar(item['Currently']), temp_buy_price, transformDollar(item['First_Bid']), 
                item['Number_of_Bids'], item['Description'], transformDttm(item['Started']), transformDttm(item['Ends']), item['Seller']['UserID'])

            for category in item['Category']:
                output_category(category, item['ItemID'])

            if item['Bids'] is None:
                pass
            else:
                for bid in item['Bids']:
                    tmp_bid_time = transformDttm(bid['Bid']['Time'])
                    output_bids(tmp_bid_time, transformDollar(bid['Bid']['Amount']), item['ItemID'], bid['Bid']['Bidder']['UserID'])

                    # Location, country : whether or not Null
                    if 'Location' in bid['Bid']['Bidder'].keys():
                        temp_location = bid['Bid']['Bidder']['Location']
                    else:
                        temp_location = None
                    if 'Country' in bid['Bid']['Bidder'].keys():
                        temp_country = bid['Bid']['Bidder']['Country']
                    else:
                        temp_country = None
                    
                    output_user(bid['Bid']['Bidder']['UserID'], bid['Bid']['Bidder']['Rating'], temp_location, temp_country)
            pass

# eliminate the ALL COLUMN's duplication in User
# Ex) eliminate "ID, rating, None, None" and "ID, rating, None, None".
def duplicate_elimination_from_User():
    lines_seen = set()
    path_w = 'dat/User_temp.dat'
    path_r = 'dat/User_duplicate.dat'
    with open(path_r, "r") as f:
        for line in f:
            if line not in lines_seen:
                write_files(path_w, line, True)
                lines_seen.add(line)

# eliminate the UserID's duplication in User
# Ex) eliminate "ID, rating, None, None" and "ID, rating. loc, country".
def duplicate_elimination_UserID_from_User():
    path_w = 'dat/User.dat'
    path_r = 'dat/User_temp.dat'
    line_list = []
    split_list = []
    userID_list = []
    with open(path_r, "r") as f:
        for line in f:
            line_split =  line.split('|')
            userID = line_split[0]
            rating = line_split[1]

            # If UserID is duplicated, they are "ID, rating, None, None" and "ID, rating. loc, country".
            # So, eliminate "UserID, rating, None, None"
            if userID in userID_list:
                if line_split[2] == 'None':
                    pass
                else:
                    old_line = '{}|{}|None|None'.format(userID, rating)
                    old_split = [[userID], [rating], ['None'], ['None']]
                    idx = userID_list.index(userID)
                    split_list.pop(idx)
                    userID_list.pop(idx)
                    line_list.pop(idx)
                    split_list.append(line_split)
                    userID_list.append(userID)
                    line_list.append(line)
            else:
                split_list.append(line_split)
                userID_list.append(userID)
                line_list.append(line)

        for line in line_list:
            write_files(path_w, line, True)

                    
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    count = 0
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            if count == 39:
                duplicate_elimination_from_User()
                duplicate_elimination_UserID_from_User()
            count += 1
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
