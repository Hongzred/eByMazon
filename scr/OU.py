from mysql.connector import OperationalError
try:
    from scr.Item import Item
except ModuleNotFoundError:
    from Item import Item

class OU():
    def __init__(self,cnx, cursor,ouID):
        self.cursor = cursor
        self.cnx = cnx
        self.ID = ouID
        self.getOUInfo()
        self.getItem()


    def getOUInfo(self):
        # Return ou information in strings: name, card number, address, state, phone
        self.cursor.execute("SELECT * FROM OU WHERE ouID = %s"% self.ID)

        for info in self.cursor:
            self.name, self.card, self.email= info[1],info[2],info[3]
            self.address, self.state, self.phone = info[4],info[5],info[6]

        self.cursor.execute("SELECT * FROM OUstatus WHERE ouID = %s" % self.ID)
        for status in self.cursor:
            self.moneySpend, self.avgRate, self.status,self.statusTime= status[1],status[2],status[3],status[4]


    def updateOUInfo(self, name, card, phone, address, state):
        # update OU info in DB
        qry = "UPDATE OU SET name = %s, cardNumber= %s, address =%s, state =%s, phone=%s WHERE ouID=%s;"

        try:
            self.cursor.execute(qry,(name, card,address,state,phone,self.ID))
            return True
        except OperationalError:
            print("Error in update OU Info")
            return False

    def getItem(self):
        qry = "SELECT itemID FROM ItemOwner WHERE ownerID = %s;" % self.ID
        self.cursor.execute(qry)
        self.items = []

        allitem = self.cursor.fetchall()
        for item in allitem:
            self.items.append(Item(cnx=self.cnx, cursor=self.cursor,itemID=item[0]))


    def changePassword(self,password):
        #update password in DB
        print()

    def editFriend(self,ownID,friendID,discount = 0.05):
        # add friend relation to DB,
        # each friend can have customer discount, if not provide, default is 5%
        pass

    def submitItem(self,image, title, priceType, usedStatus):
        # add submit item to itemDB
        pass

    def submitFixedPrice(self,itemID, price, numAvailable):
        # add price for fixed price item
        pass

    def submitBiddingInfo(self, itemID, startPrice, endDay):
        # add price for bidding item
        pass

    def bidding(self,itemID, bidderID, price):
        # record bidding in BidRecord
        pass

    def calculateTotal(self, price, buyerID,itemID):
        # get taxrate from taxDB by buyer address
        # get vip status from buyer
        # check if buyer if friend of owner in friendDB
        # can combine two discount
        # return total cost
        pass

    def purchaseFixedPrice(self, itemID, buyerID, numBuy):
        # get price from itemDB by itemID
        # get finalPrice by call self.calculateTotal
        # add to transactionDB and update buyer money spend
        pass

    def purchaseBidding(self, itemID):
        # get called when reach to the endDay of bidding
        # get second highest bidder from BidRecordDB
        # get finalPrice by call self.calculateTotal
        # add to transactionDB and update buyer money spend
        pass

    def declineTransaction(self, itemID, buyerID):
        # No available if the shipping status is true for item
        # Else: remove from transaction, deduct moneyspend from buyer status
        # Add warning to OU
        pass

    def viewTransactionHistory(self,ouID):
        # get transaction History from DB
        # Separate for sell and purchase, return dict{'sell','buy'}
        # each is list of transaction in form[itemID, buyerID, priceDeal, dealTime]
        pass

    def submitRating(self,itemID, raterID, rating):
        # add rating to DB
        # check for bad rating that will cause warning or depromotion
        # check for good rating that will cause promotion
        pass

    def submitCompliant(self,itemID, complianterID, description):
        # add compliant to DB
        pass