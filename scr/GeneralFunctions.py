import mysql.connector
# from kivy.core.image import Image as CoreImage
# from io import BytesIO
try:
    from scr.GU import GU
    from scr.Item import Item
except ModuleNotFoundError:
    from GU import GU
    from Item import Item

class General():
    def __init__(self,cursor,cnx):
        self.cnx = cnx
        self.cursor = cursor

    def login_check(self, username, password):
        '''
        function: check login info with DB
        :param username:
        :param password:
        :return:
            -   dict{'ID','userType','status'}  for correct login OU
            -   dict{'ID','userType'}           for correct login SU
            -   1                               for password not match
            -   2                               for in GU application
            -   3                               for in blacklist
            -   False                           nothing found
        '''
        qry = "SELECT ID, userType FROM User WHERE username=%s AND password=%s;"
        self.cursor.execute(qry,(username,password))

        user = self.cursor.fetchone()
        if user:
            if not user[1]:     # For OU
                self.cursor.execute("SELECT status FROM OUstatus WHERE ouID = %s;" % user[0])
                return {'ID': user[0], 'userType': user[1],'status':self.cursor.fetchone()[0]}
            return {'ID': user[0], 'userType': user[1]}  # For SU

        tempGU = GU(cnx=self.cnx,cursor=self.cursor)
        return tempGU.checkUsername(username)


    def removeOU(self,username):
        """
        Remove OU from DB, and add his/her username to blacklist
        """
        try:
            qry = "DELETE FROM User WHERE username = '%s';" % username
            self.cursor.execute(qry)
            self.cursor.execute("INSERT INTO ouBlacklist VALUE ('%s');"%username)
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Remove OU: %s"%ERR)
            return False


    def popularItem(self):
        """
        :return: list of Item()
        """
        qry = "SELECT itemID FROM ItemInfo WHERE saleStatus = True;"
        self.cursor.execute(qry)
        allItem = []
        allItems = self.cursor.fetchall()
        for info in allItems:
            allItem.append(Item(cnx=self.cnx,cursor=self.cursor,itemID=info[0]))
        return allItem

    def appeal(self,ouID,message):
        qry = "INSERT INTO Appeal VALUE (%s,'%s');" %(ouID,message)
        try:
            self.cursor.execute(qry)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print("Error in submit appeal: %s" % err)



    def searchItem(self,keywords):
        """
        :param keywords: search keyword
        :return:
            - False if not found, add to Notification DB
            - list of item, if found
        """

        qry = ("INSERT INTO searchKeyword(keyword) VALUES ('%s') ON DUPLICATE KEY UPDATE frequency =frequency+1;" % (keywords))
        self.cursor.execute(qry)
        self.cnx.commit()

        qry = ("SELECT itemID FROM ItemInfo WHERE (title LIKE '%s' OR description LIKE '%s') AND approvalStatus = True;"
               % (('%'+keywords+'%','%'+keywords+'%')))
        self.cursor.execute(qry)

        allItem = []
        allItems = self.cursor.fetchall()
        if allItems is None:
            self.cursor.execute("INSERT INTO Notification VALUE ('%s');"% keywords)
            self.cnx.commit()
            return False
        else:
            for info in allItems:
                allItem.append(Item(cnx=self.cnx,cursor=self.cursor,itemID=info[0]))
            return allItem



    def sortItem(self,items,attribute, decs):
        """
        :param items:  list of item object
        :param attribute:  attribute to be sort (string)
        :param decs: True for sorted in Descending order, False for ascend
        :return:
        """
        k = sorted(items, key=lambda x: getattr(x, attribute),reverse= decs)
        return k


    def checkStaus(self, ouID):
        # return status of the select OU
        pass

    def changeStaus(self, ouID):
        #update new status
        # get call when receive warning or low rating
        pass

    def manageWarnig(self,ouID):
        # called when add a warning
        # check number warning receive, if greater or equal to 2, suspend OU
        # else make sure that ou is not VIP
        pass

    # def ouBlacklist(self,ouID):
    #     # remove the ou from all DB and all active sale item post by that ou,
    #     # but not the sold item by he/she, the seller will be None
    #     # add the username to ouBlacklist
    #     pass


