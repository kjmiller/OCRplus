
"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012

Skeleton parser for cs145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child

Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar 
with the functions at http://docs.python.org/library/xml.dom.minidom.html and 
http://docs.python.org/library/xml.dom.html

Happy parsing!
"""

import sys
from xml.dom.minidom import parse
from re import sub

columnSeparator = "<>"

delimiter = "#OppanOCRplusDelimiter#"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
	return len(f) > 4 and f[-4:] == '.xml'

"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
	elements = []
	children = elem.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
			elements.append(child)

	return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
	children = elem.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
			return child

	return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
	return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
	if len(elem.childNodes) == 1:
		return pcdata(elem) 

	return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
	curElem = getElementByTagNameNR(elem, tagName)
	if curElem != None:
		return pcdata(curElem)

	return ''

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

#Gets the ItemID from an Item
#-Note: Returns a string
def get_auctioned_item(auction):
	return auction.getAttribute("ItemID")

#Returns list of Item elements that are children of an Items element
def get_auctions(dom):
	return getElementsByTagNameNR(dom, "Item")

#Returns list of categories to which the Item being auctioned off belongs
#-Note: Returns a list of strings
def get_categories(auction):
	return map(getElementText, getElementsByTagNameNR(auction, "Category"))

#Returns list of bids in an auction
def get_bids(auction):
	return getElementsByTagNameNR(getElementByTagNameNR(auction, "Bids"), "Bid")

#Adds a row to the Auction relation in auction_file with info about auction
def insert_auction_row(auction, auction_file):
	itemID = get_auctioned_item(auction)
	userID = getElementByTagNameNR(auction, "Seller").getAttribute("UserID")
	name = getElementTextByTagNameNR(auction, "Name")
	currently = transformDollar(getElementTextByTagNameNR(auction, "Currently"))
	buy_price = getElementTextByTagNameNR(auction, "Buy_Price")
	if buy_price == "":
		buy_price = "NULL"
	else:
		buy_price = transformDollar(buy_price)

	first_bid = transformDollar(getElementTextByTagNameNR(auction, "First_Bid"))
	number_of_bids = str(int(getElementTextByTagNameNR(auction, "Number_of_Bids")))
	started = transformDttm(getElementTextByTagNameNR(auction, "Started"))
	ends = transformDttm(getElementTextByTagNameNR(auction, "Ends"))
	description = getElementTextByTagNameNR(auction, "Description")
	auction_file.write(columnSeparator.join([itemID, userID, name, currently, buy_price, first_bid, number_of_bids, started, ends, description]) + "\n")

#Adds a row to the User relation corresponding to the seller in auction
def insert_seller_row(auction, user_file):
	location = getElementTextByTagNameNR(auction, "Location")
	country = getElementTextByTagNameNR(auction, "Country")
	seller = getElementByTagNameNR(auction, "Seller")
	userID = seller.getAttribute("UserID")
	rating = str(int(seller.getAttribute("Rating")))
	user_file.write(columnSeparator.join([userID, rating, location, country]) + "\n")

#Adds a row to the User relation corresponding to the bidder in bid
def insert_bidder_row(bid, user_file):
	bidder = getElementByTagNameNR(bid, "Bidder")
	location = getElementTextByTagNameNR(bidder, "Location")
	if location == "":
		location = "NULL"

	country = getElementTextByTagNameNR(bidder, "Country")
	if country == "":
		country = "NULL"

	userID = bidder.getAttribute("UserID")
	rating = str(int(bidder.getAttribute("Rating")))
	user_file.write(columnSeparator.join([userID, rating, location, country]) + "\n")

#Adds a row to the Bid relation using info from bid as well as itemID (i.e. what they're bidding on)
def insert_bid_row(bid, itemID, bid_file):
	userID = getElementByTagNameNR(bid, "Bidder").getAttribute("UserID")
	time = transformDttm(getElementTextByTagNameNR(bid, "Time"))
	amount = transformDollar(getElementTextByTagNameNR(bid, "Amount"))
	bid_file.write(columnSeparator.join([userID, itemID, time, amount]) + "\n")

#Adds a row to the Category relation, saying that item itemID is in category category
def insert_category_row(itemID, category, category_file):
	category_file.write(columnSeparator.join([itemID, category]) + "\n")

"""
Parses a single xml file. Currently, there's a loop that shows how to parse
item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
"""
def parseXml(f):
	dom = parse(f) # creates a dom object for the supplied xml file
	auction_file = open("auction.dat", "a")
	user_file = open("user.dat", "a")
	category_file = open("category.dat", "a")
	bid_file = open("bid.dat", "a")
	auctions = get_auctions(getElementByTagNameNR(dom, "Items"))
	for auction in auctions:
		insert_auction_row(auction, auction_file)
		insert_seller_row(auction, user_file)
		itemID = get_auctioned_item(auction)
		categories = get_categories(auction)
		for category in categories:
			insert_category_row(itemID, category, category_file)
		
		bids = get_bids(auction)
		for bid in bids:
			insert_bidder_row(bid, user_file)
			insert_bid_row(bid, itemID, bid_file)

	auction_file.close()
	user_file.close()
	category_file.close()
	bid_file.close()

#Note: some of the code in this function was copied from CS145 starter code
def recursively_get_ocr_lines(node):
	targets = []
	children = node.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE:
			if child.tagName == "span" and child.getAttribute("class") == "ocr_line":
				targets.append(child)
			else:
				targets.extend(recursively_get_ocr_lines(child))

        return targets

def get_bbox(ocr_line):
	return " ".join(ocr_line.getAttribute("title").split(" ")[1:])

def recursively_get_text_helper(node):
	texts = []
	children = node.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE:
			texts.extend(recursively_get_text_helper(child))
		elif child.nodeType == child.TEXT_NODE:
			texts.append(child.data)

	return texts

def recursively_get_text(node):
	return "".join(recursively_get_text_helper(node))

def main(argv):
	input_file_name = argv[1]
	output_file_name = argv[2]
	dom = parse(input_file_name)
	ocr_lines = recursively_get_ocr_lines(dom)
	bboxes = map(get_bbox, ocr_lines)
	texts = map(recursively_get_text, ocr_lines)
	stuff = map(lambda i: bboxes[i] + delimiter + texts[i], range(len(bboxes)))
	output_str = delimiter.join(stuff)
	print(output_str.encode('utf8'))
	output_file = open(output_file_name, "w")
	output_file.write(output_str.encode('utf8') + "\n")
	output_file.close()

"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
#def main(argv):
#	if len(argv) < 2:
#		print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
#		sys.exit(1)
#
#	# loops over all .xml files in the argument
#	for f in argv[1:]:
#		if isXml(f):
#			parseXml(f)
#			print "Success parsing " + f

if __name__ == '__main__':
	main(sys.argv)
