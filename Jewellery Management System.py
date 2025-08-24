import mysql.connector
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

# function to accquire DB connectivity
def getDbConnection():
    conn = mysql.connector.connect(host='localhost', user='root', password='12345', database='JIBS')
    if conn.is_connected():
        # print('Connection Sucessfully Established With Database !')
        # print()
        return conn
    else:
        print('Connection Not Accquired !')
        return 0

def NorMenu():
    print('                                          ----------------------------------------------------------- ')
    print("                                         |                   LOGGED IN AS SALES PERSON               | ")
    print('                                         |-----------------------------------------------------------| ')
    print('                                         |           JEWELLERY INVENTORY AND BILLING SYSTEM          |')
    print('                                         |-----------------------------------------------------------|')
    print('                                         ************************* M E N U ***************************')
    print('                                         *************************************************************')
    print('                                         **                                                         **')
    print('                                         **                  1. Show List Of Products               **')
    print('                                         **                  2. Search A Product                    **')
    print('                                         **                  3. Add A Customer                      **')
    print('                                         **                  4. Search Customer                     **')
    print('                                         **                  5. Purchase                            **')
    print('                                         **                  6. Supplier Details                    **')
    print('                                         **                  7. Exit JIBS                           **')
    print('                                         *************************************************************')
    print('                                         *************************************************************')
    print()


def MangMenu():
    print('                                          ----------------------------------------------------------- ')
    print("                                         |                     LOGGED IN AS MANAGER                  | ")
    print('                                         |-----------------------------------------------------------| ')
    print('                                         |           JEWELLERY INVENTORY AND BILLING SYSTEM          |')
    print('                                         |-----------------------------------------------------------|')
    print('                                         ************************* M E N U ***************************')
    print('                                         *************************************************************')
    print('                                         **                                                         **')
    print('                                         **                  1. Add A Product                       **')
    print('                                         **                  2. Add A Supplier                      **')
    print('                                         **                  3. Show List Of Products               **')
    print('                                         **                  4. Search A Product                    **')
    print('                                         **                  5. Add A Customer                      **')
    print('                                         **                  6. Search Customer                     **')
    print('                                         **                  7. Purchase                            **')
    print('                                         **                  8. Update Product Quantity             **')
    print('                                         **                  9. Monthly Sales Report                **')
    print('                                         **                 10. See Payment Details                 **')
    print('                                         **                 11. Add New Employee                    **')
    print('                                         **                 12. Exit JIBS                           **')
    print('                                         *************************************************************')
    print('                                         *************************************************************')
    print()


def login():
    isValidUser = 0
    while (isValidUser != 1 and isValidUser != 2):
        print()
        print('    ------------------------  ')
        print('   |       LOGIN PAGE       | ')
        print('    ------------------------  ')
        print()
        uname = input('   Enter Your Username : ')
        password = input('   Enter Your Password : ')
        print()
        isValidUser = authenticate(uname, password)
        return isValidUser


def authenticate(uname, password):
    conn = getDbConnection()
    mycur = conn.cursor()
    query = 'select l.username,l.password,e.employee_type from login as l,employee as e where l.username=e.username and l.USERNAME=%s AND l.PASSWORD=%s;'
    data = (uname, password)
    mycur.execute(query, data)
    result = mycur.fetchall()
    validLogin = 0
    conn.commit()
    conn.close()
    for i in result:
        if (i[0] == uname and i[1] == password and i[2] == "MANAGER"):
            print()
            print('   -> Login Sucessful !')
            print()
            validLogin = 1

        elif (i[0] == uname and i[1] == password and i[2] == "SALES PERSON"):
            print()
            print('   -> Login Sucessful !')
            print()
            validLogin = 2

    if validLogin == 0:
        print('Invalid Username Or Password,Please Try Again ! ')

    return validLogin




def addProduct():
    conn = getDbConnection()
    suppId = input("Enter The Supplier Id : ")
    productName = input(' Enter The Product Name         : ')
    material = input(' Enter The Product Material     : ')
    productWt = int(input(' Enter The Product Weight         : '))
    proQty = int(input(' Enter The Product Quantity       : '))
    goldWt = int(input(' Enter The Gold Weight(Gm)        : '))
    goldCrt = int(input(' Enter The Gold Carat             : '))
    silverWt = int(input(' Enter The Silver Weight(Gm)      : '))
    diamondCrt = int(input(' Enter The Diamond Carat          : '))
    diamondCost = int(input(' Enter The Diamond Cost          : '))
    makeCharge = int(input(' Enter The Making Charges  : '))
    productPrice = 0
    proStr = "P0"
    mycur1 = conn.cursor()
    mycur2 = conn.cursor()
    mycur3 = conn.cursor()
    queryProId = "SELECT COUNT(PRODUCT_ID) FROM PRODUCT"
    mycur3.execute(queryProId)
    pid = mycur3.fetchone()
    autoProId = pid[0] + 1
    productId = proStr + str(autoProId)
    query1 = '''INSERT INTO PRODUCT(Product_ID,Product_Name,Product_Material,NET_WT,Gold_Wt,Gold_Crt,Silver_Wt,Diamond_Crt,Diamond_Cost,Making_Charge,Total_Price)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    value1 = (
    productId, productName, material, productWt, goldWt, goldCrt, silverWt, diamondCrt, diamondCost, makeCharge,
    productPrice)
    mycur1.execute(query1, value1)
    query2 = 'INSERT INTO INVENTORY(PRODUCT_ID,PRODUCT_QUANTITY,SUPPLIER_ID)VALUES(%s,%s,%s)'
    value2 = (productId, proQty, suppId)
    mycur2.execute(query2, value2)
    print()
    print('   ->Record Inserted !')
    print()
    conn.commit()
    conn.close()
    CalGoldRate()


def CalGoldRate():
    GoldRate = int(input("Enter Today's Gold Rate : "))
    SilverRate = int(input("Enter Today's Silver Rate : "))
    conn = getDbConnection()
    queryCal = 'select Product_ID,Net_Wt,Gold_Wt,Diamond_Cost,Silver_Wt,Making_Charge,Total_Price from PRODUCT ORDER BY PRODUCT_ID;'
    mycur = conn.cursor()
    mycur.execute(queryCal)
    result = mycur.fetchall()
    for i in result:
        ProId = i[0]
        NetWt = i[1]
        Gold_Wt = i[2]
        Diamond_Cost = i[3]
        Silver_Wt = i[4]
        Making_Charge = i[5]
        Total_Price = i[6]
        calGold = GoldRate * Gold_Wt
        calSilver = SilverRate * Silver_Wt
        totalCost = calGold + calSilver + Diamond_Cost + Making_Charge
        queryUp = 'UPDATE PRODUCT SET TOTAL_PRICE = %s WHERE PRODUCT_ID=%s'
        x = (totalCost, ProId)
        mycur.execute(queryUp, x)
    conn.commit()
    conn.close()


def addCustomer():
    conn = getDbConnection()
    customerName = input(' Enter The Customer Name          : ')
    custPh = int(input(' Enter The Customer Phone Number  : '))
    custEmail = input(' Enter The Customer Email ID      : ')
    custAddress = input(' Enter The Customer Address       : ')
    custStr = "C0"
    mycur = conn.cursor()
    mycurCust = conn.cursor()
    queryCustomerId = "SELECT COUNT(CUSTOMER_ID) FROM CUSTOMER"
    mycurCust.execute(queryCustomerId)
    cid = mycurCust.fetchone()
    custId = cid[0] + 1
    customerId = custStr + str(custId)
    queryCust = '''INSERT INTO CUSTOMER(Customer_ID,Customer_Name,Cust_PHONENO,Cust_Email,Cust_Address)VALUES(%s,%s,%s,%s,%s);'''
    valueCust = (customerId, customerName, custPh, custEmail, custAddress)
    mycur.execute(queryCust, valueCust)
    print()
    print('   ->Record Inserted !')
    print()
    conn.commit()
    conn.close()


def listProduct():
    conn = getDbConnection()
    query3 = 'select P.PRODUCT_ID,P.PRODUCT_NAME,P.PRODUCT_MATERIAL,P.NET_WT,P.GOLD_CRT,P.DIAMOND_CRT,I.PRODUCT_QUANTITY,P.TOTAL_PRICE from PRODUCT AS P,INVENTORY AS I WHERE I.PRODUCT_ID=P.PRODUCT_ID ORDER BY P.PRODUCT_ID;'
    mycur = conn.cursor()
    mycur.execute(query3)
    result = mycur.fetchall()
    print()
    print('-' * 200)
    print('-' * 200)
    print(
        "   {0:20}{1:30}{2:30}{3:10}{4:10}{5:10}{6:10}{7:20}".format('  ID  ', '  NAME  ', '  MATERIAL  ', '  NET_WT  ',
                                                                     '  GOLD_CRT  ', '  DIAMOND_CRT  ', '  QTY  ',
                                                                     '  COST  '))
    print('-' * 200)
    print('-' * 200)
    for x in result:
        print("   {0:20}{1:30}{2:30}{3:10}{4:10}{5:10}{6:10}{7:20}".format(x[0], x[1], x[2], x[3], x[4], x[5], x[6],
                                                                           x[7]))
    print('-' * 200)
    print('-' * 200)
    print()
    print()
    conn.commit()
    conn.close()


def searchProduct():
    op = 0
    while op >= 0 < 4:
        print('    ------------------------------- ')
        print('   | 1. Search Product By ID       |')
        print('   |-------------------------------|')
        print('   | 2. Search Product By Name     |')
        print('   |-------------------------------|')
        print('   | 3. Search Product By Material |')
        print('   |-------------------------------|')
        print('   | 4. Go To Main Menu            |')
        print('    ------------------------------- ')
        print()
        op = int(input('   Choose An Option From The Menu : '))
        print()

        if op == 1:
            conn = getDbConnection()
            mycur = conn.cursor()
            productID = input('   Enter The ID Of The Product You Want To Search : ')
            query6 = 'SELECT * FROM PRODUCT WHERE PRODUCT_ID LIKE %s'
            value6 = ['%' + productID + '%']
            mycur.execute(query6, value6)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()

        elif op == 2:

            conn = getDbConnection()
            mycur = conn.cursor()
            productName = input('   Enter The Name Of The Product You Want To Search : ')
            query7 = 'SELECT * FROM PRODUCT WHERE PRODUCT_NAME LIKE %s'
            value7 = ['%' + productName + '%']
            mycur.execute(query7, value7)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()
        elif op == 3:

            conn = getDbConnection()
            mycur = conn.cursor()
            material = input('   Enter The Material Of The Product You Want To Search : ')
            query8 = 'SELECT * FROM PRODUCT WHERE PRODUCT_MATERIAL LIKE %s'
            value8 = [material]
            mycur.execute(query8, value8)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()
        else:
            break

        if op == 4:
            return


def searchCustomer():
    op = 0
    while op >= 0 < 4:
        print('    ------------------------------- ')
        print('   | 1. Search Customer By Name    |')
        print('   |-------------------------------|')
        print('   | 2. Search Customer By PhoneNo |')
        print('   |-------------------------------|')
        print('   | 3. Go To Main Menu            |')
        print('    ------------------------------- ')
        print()
        op = int(input('   Choose An Option From The Menu : '))
        print()

        if op == 1:
            conn = getDbConnection()
            mycur = conn.cursor()
            custName = input('   Enter The Name Of The Customer You Want To Search : ')
            query6 = 'SELECT * FROM CUSTOMER WHERE CUSTOMER_NAME LIKE %s'
            value6 = ['%' + custName + '%']
            mycur.execute(query6, value6)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()

        if op == 2:
            conn = getDbConnection()
            mycur = conn.cursor()
            custPhone = input('   Enter The Phone Number Of The Customer You Want To Search : ')
            query7 = 'SELECT * FROM CUSTOMER WHERE CUST_PHONENO LIKE %s'
            value7 = ['%' + custPhone + '%']
            mycur.execute(query7, value7)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()

        if op == 4:
            return
        else:
            return


def searchSupplier():
    op = 0
    while op >= 0 < 4:
        print('    ------------------------------- ')
        print('   | 1. Search Supplier By Name    |')
        print('   |-------------------------------|')
        print('   | 2. Search Supplier By PhoneNo |')
        print('   |-------------------------------|')
        print('   | 3. Go To Main Menu            |')
        print('    ------------------------------- ')
        print()
        op = int(input('   Choose An Option From The Menu : '))
        print()

        if op == 1:
            conn = getDbConnection()
            mycur = conn.cursor()
            custName = input('   Enter The Name Of The Customer You Want To Search : ')
            query6 = 'SELECT * FROM SUPPLIER WHERE SUPPLIER_NAME LIKE %s'
            value6 = ['%' + custName + '%']
            mycur.execute(query6, value6)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()

        if op == 2:
            conn = getDbConnection()
            mycur = conn.cursor()
            custPhone = input('   Enter The Phone Number Of The Customer You Want To Search : ')
            query7 = 'SELECT * FROM SUPPLIER WHERE SUPPLIER_PHONENO LIKE %s'
            value7 = ['%' + custPhone + '%']
            mycur.execute(query7, value7)
            x = mycur.fetchall()
            print()
            for i in x:
                print(i)
            conn.commit()
            conn.close()

        if op == 4:
            return
        else:
            return


def addSupplier():
    conn = getDbConnection()
    supplierName = input(" Enter The Supplier's Name        : ")
    supplierPh = int(input(" Enter The Supplier's Phone Number: "))
    supplierEmail = input(" Enter The Supplier's Email ID    : ")
    supplierAddress = input(" Enter The Supplier's Address     : ")
    mycur = conn.cursor()
    mycurSupp = conn.cursor()
    supStr = "S00"
    querySupplierId = "SELECT COUNT(SUPPLIER_ID) FROM SUPPLIER"
    mycurSupp.execute(querySupplierId)
    sid = mycurSupp.fetchone()
    supId = sid[0] + 1
    supplierId = supStr + str(supId)
    querySupp = '''INSERT INTO SUPPLIER(SUPPLIER_ID,SUPPLIER_Name,SUPPLIER_PHONENO,SUPPLIER_Address,SUPPLIER_EMAIL)VALUES(%s,%s,%s,%s,%s);'''
    valueSupp = (supplierId, supplierName, supplierPh, supplierAddress, supplierEmail)
    mycur.execute(querySupp, valueSupp)
    print()
    print('   ->Record Inserted !')
    print()
    conn.commit()
    conn.close()


def verifyProduct(proId):
    conn = getDbConnection()
    mycurB = conn.cursor()
    queryChkProduct = 'SELECT PRODUCT_QUANTITY FROM INVENTORY WHERE PRODUCT_ID=%s ;'
    valueChkProduct = (proId,)
    mycurB.execute(queryChkProduct, valueChkProduct)
    chk1 = mycurB.fetchone()
    conn.commit()
    conn.close()
    return chk1[0]


def purchase():
    count = 0
    CustId = input('  Enter Customer ID     : ')
    proId = input('   Enter Product ID      : ')
    payType = input('  Enter Payment Type       : ')
    isProductValid = verifyProduct(proId)
    payStr = "PAY0"
    billStr = "B0"
    if isProductValid > 0:
        conn = getDbConnection()
        mycurPay = conn.cursor()
        mycurPurchase = conn.cursor()
        mycurSel = conn.cursor()
        mycurUpd = conn.cursor()
        mycurAmt = conn.cursor()
        mycurPayment = conn.cursor()
        mycurAutoBill = conn.cursor()
        mycurBill1 = conn.cursor()
        mycurBill2 = conn.cursor()
        mycurInv = conn.cursor()
        mycurCustomer = conn.cursor()
        queryPayId = "SELECT COUNT(PAYMENT_ID) FROM PAYMENT"
        mycurPayment.execute(queryPayId)
        pid1 = mycurPayment.fetchone()
        paymentId = pid1[0] + 1
        PayId = payStr + str(paymentId)

        queryBillId = "SELECT COUNT(BILL_ID) FROM PURCHASE"
        mycurAutoBill.execute(queryBillId)
        bid1 = mycurAutoBill.fetchone()
        autoBillId = bid1[0] + 1
        billId = billStr + str(autoBillId)

        queryChkProduct = 'SELECT PRODUCT_QUANTITY FROM INVENTORY WHERE PRODUCT_ID=%s ;'
        valueChkProduct = (proId,)
        mycurSel.execute(queryChkProduct, valueChkProduct)
        qty = mycurSel.fetchone()
        print(qty[0])
        x = qty[0] - 1
        # print('verifyBook=',chk1)
        if qty[0] > 0:
            qp = 'UPDATE INVENTORY SET PRODUCT_QUANTITY=%s WHERE PRODUCT_ID=%s ;'
            vcp = (x, proId)
            mycurUpd.execute(qp, vcp)
            chk1 = mycurUpd.fetchone()
            amtQuery = 'SELECT TOTAL_PRICE FROM PRODUCT WHERE PRODUCT_ID=%s'
            amtVal = (proId,)
            mycurAmt.execute(amtQuery, amtVal)
            payAmt = mycurAmt.fetchone()
            paymentQuery = '''INSERT INTO PAYMENT(PAYMENT_ID,PAYMENT_DATE,PAYMENT_AMOUNT,PAYMENT_TYPE)VALUES(%s,NOW(),%s,%s)'''
            count += 1
            paymentValue = (PayId, payAmt[0], payType)
            mycurPay.execute(paymentQuery, paymentValue)
            print()
            print('   Payment has been Done for Payment ID', PayId, '!')
            print()
            purchaseQuery = '''INSERT INTO PURCHASE(PRODUCT_ID,CUSTOMER_ID,PAYMENT_ID,PURCHASE_DATE,BILL_AMOUNT,BILL_ID)VALUES(%s,%s,%s,NOW(),%s,%s)'''
            valuePurchase = (proId, CustId, PayId, payAmt[0], billId)
            mycurPurchase.execute(purchaseQuery, valuePurchase)
            billQuery1 = 'SELECT PUR.CUSTOMER_ID,PUR.BILL_ID,PUR.PAYMENT_ID,PUR.PURCHASE_DATE,PUR.BILL_AMOUNT,PAY.PAYMENT_TYPE FROM PURCHASE AS PUR,PAYMENT AS PAY WHERE PUR.PAYMENT_ID = PAY.PAYMENT_ID AND PAY.PAYMENT_ID=%s'
            billVal1 = (PayId,)
            mycurBill1.execute(billQuery1, billVal1)
            billFetch1 = mycurBill1.fetchall()
            billQuery2 =  'SELECT PRODUCT_ID,PRODUCT_NAME,NET_WT,GOLD_WT,GOLD_CRT,SILVER_WT,DIAMOND_CRT,DIAMOND_COST,MAKING_CHARGE FROM PRODUCT WHERE PRODUCT_ID =%s'
            billVal2 = (proId,)
            mycurBill2.execute(billQuery2, billVal2)
            billFetch2 = mycurBill2.fetchall()
            invQuery = 'SELECT BILL_ID FROM PURCHASE WHERE PAYMENT_ID = %s'
            valInv = (PayId,)
            mycurInv.execute(invQuery, valInv)
            invFetch = mycurInv.fetchone()
            for bill in billFetch2:

                tableData2 = [["PRODUCT ID","PRODUCT NAME","NET WT","GOLD WT","GOLD CRT", "SILVER WT", "DIAMOND CRT", "DIAMOND COST", "MAKING CHARGE" ],
                              [bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6],bill[7],bill[8]]
                              ]

            for bill2 in billFetch1:
                tableData1 = [

                    ["CUSTOMER ID", "BILL ID", "PAYMENT ID", "PURCHASE DATE", "PAYMENT TYPE", "TOTAL AMOUNT"],
                    [bill2[0], bill2[1], bill2[2], bill2[3], bill2[5], bill2[4]]
                    ]

            queryCustomer = 'SELECT CUSTOMER_NAME,CUST_PHONENO,CUST_EMAIL,CUST_ADDRESS FROM CUSTOMER WHERE CUSTOMER_ID = %s'
            valCustomer = (CustId,)
            mycurCustomer.execute(queryCustomer,valCustomer)
            custValue = mycurCustomer.fetchall()
            custVal1 = "  "
            custVal2 = "  "
            custVal3 = "  "
            custVal4 = "  "
            b1 = "  "
            b2 = "  "
            b3 = "  "
            b4 = "  "
            b5 = "  "
            b6 = "  "
            for i in custValue:
                custVal1 = str(i[0])
                custVal2 = str(i[1])
                custVal3 = str(i[2])
                custVal4 = str(i[3])

            # creating a Document structure with A4 size page
            fname = invFetch[0]
            docu = SimpleDocTemplate("C:/Users/adity/Desktop/'%s'.pdf"%fname, pagesize=(landscape(A4)))
            styles = getSampleStyleSheet()

            doc_style = styles["Heading1"]
            doc_style2 = styles["Heading2"]
            doc_style3 = styles["Heading2"]
            doc_style4 = styles["Heading3"]
            doc_style5 = styles["Heading4"]
            doc_style.alignment = 1
            doc_style2.alignment = 2
            doc_style3.alignment = 2
            doc_style4.alignment = 0
            doc_style5.alignment = 1
            title = Paragraph("MAAHIRA DIAMOND", doc_style)
            title2 = Paragraph("INVOICE", doc_style)
            inv = Paragraph("Invoice No . ", doc_style2)
            invno = Paragraph(invFetch[0], doc_style3)
            addl1 = Paragraph("126/8/24, , VIDYARTHI MARKET", doc_style5)
            addl2 = Paragraph("GOVIND NAGAR, KANPUR, Uttar Pradesh", doc_style5)
            addl3 = Paragraph("Pincode, 208006", doc_style5)
            cust1 = Paragraph(custVal1,doc_style4)
            cust2 = Paragraph(custVal2,doc_style4)
            cust3 = Paragraph(custVal3,doc_style4)
            cust4 = Paragraph(custVal4,doc_style4)
            bb1= Paragraph(b1,doc_style4)
            bb2= Paragraph(b2,doc_style4)
            bb3= Paragraph(b3,doc_style4)
            bb4=Paragraph(b4,doc_style4)
            bb5=Paragraph(b5,doc_style4)
            bb6=Paragraph(b6,doc_style4)







            style = TableStyle([
                ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),

            ])
            TableStyle.Align = 'BOTTOM'
            TableStyle.vAlign = 'BOTTOM'
            # creates a table object using the Table() to pass the table data and the style object

            table1 = Table(tableData1, style=style)
            table2 = Table(tableData2, style=style)
            # finally, we have to build the actual pdf merging all objects together

            docu.build([title, title2, inv, invno, cust1,cust2,cust3,cust4,bb1,bb2,bb3, table2, table1,bb4,bb5,bb6,addl1, addl2, addl3])
            print("Your Bill ",billId," has Been generated !")
            conn.commit()
            conn.close()
        else:
            print("Product Out Of Stock !")






def addEmployee():
    conn = getDbConnection()
    employeeName = input(" Enter The Employee's Name        : ")
    username = input(" Enter The Employee's Username : ")
    employeePhone = int(input(" Enter The Employee's Phone Number:    : "))
    employeeEmail = input(" Enter The Employee's Email ID    : ")
    employeeAddress = input(" Enter The Employee's Address     : ")
    employeeType = input(" Enter The Employee Type     : ")
    password = input(" Enter The Employee's Login Password    : ")
    mycur1 = conn.cursor()
    mycur2 = conn.cursor()
    mycurEmployee = conn.cursor()
    empStr = "E00"
    queryEmployeeId = "SELECT COUNT(EMPLOYEE_ID) FROM EMPLOYEE"
    mycurEmployee.execute(queryEmployeeId)
    eid = mycurEmployee.fetchone()
    empId = eid[0] + 1
    employeeId = empStr + str(empId)
    queryLogin = 'INSERT INTO LOGIN(USERNAME,PASSWORD)VALUES(%s,%s)'
    valueLogin = (username, password)
    mycur1.execute(queryLogin, valueLogin)
    queryEmp = '''INSERT INTO EMPLOYEE(EMPLOYEE_ID,EMPLOYEE_Name,USERNAME,EMPLOYEE_PHONENO,EMPLOYEE_EMAIL,EMPLOYEE_Address,EMPLOYEE_TYPE)VALUES(%s,%s,%s,%s,%s,%s,%s);'''
    valueEmp = (employeeId, employeeName, username, employeePhone, employeeEmail, employeeAddress, employeeType)
    mycur2.execute(queryEmp, valueEmp)
    print()
    print('   ->Record Inserted !')
    print()
    conn.commit()
    conn.close()


def UpdateQuantity():
    conn = getDbConnection()
    mycurUpdQty = conn.cursor()
    proId = input("Enter the Product Id : ")
    pQty = int(input(" Enter The Quantity : "))
    queryUpdQty = "UPDATE INVENTORY SET PRODUCT_QUANTITY = %s WHERE PRODUCT_ID = %s"
    valUpdQty = (pQty, proId,)
    mycurUpdQty.execute(queryUpdQty, valUpdQty)
    print()
    print("  -> Product Quantity has Been Updated !")
    print()
    conn.commit()
    conn.close()

def salesReport():
    conn = getDbConnection()
    mycur = conn.cursor()
    salesReportQuery = 'SELECT*FROM PURCHASE'
    mycur.execute(salesReportQuery)
    data = mycur.fetchall()
    wfile = open("C:/Users/adity/Desktop/SalesReport.txt", 'w')
    wfile.write(
        'PRODUCT ID' + ';' + 'CUSTOMER ID' + ';' + 'PAYMENT ID' + ';' + 'SALE DATE' + ';' + 'BILL ID' + ';' + 'BILL AMOUNT' + '\n')
    for row in data:
        wfile.write(
            row[0] + ';' + '        ' + row[1] + ';' + '    ' + row[2] + ';' + '    ' + str(row[3]) + ';' + '    ' +
            row[5] + ';' + '    ' + str(row[4]) + '\n')
    conn.commit()
    conn.close()
    wfile.close()
    print(
        "Report Has Been Generated Successfully ! ")
    print()
    askReport = input('Do You Want To Read This File Now ?(Y/N) ')
    print()
    if askReport == 'N':
        return 
    elif askReport == 'Y':
        rfile = open("C:/Users/adity/Desktop/SalesReport.txt", 'r')
        readdata = rfile.readlines()
        for i in readdata:
            data = i.replace(';', '     ')
            print(data)
        rfile.close()
    else:
        print('Invalid Entry !')

def supDetails():
    conn = getDbConnection()
    mycur = conn.cursor()
    supID = input('Enter Supplier Id : ')
    mycur.callproc('GetSupplierDetails', (supID,))
    for result in mycur.stored_results():
            print(result.fetchall())
    conn.commit()
    conn.close()

def payDetails():
    conn = getDbConnection()
    mycur = conn.cursor()
    payID = input('Enter Payment Id : ')
    mycur.callproc('GetPaymentDetails', (payID,))
    for result in mycur.stored_results():
            print(result.fetchall())
    conn.commit()
    conn.close()



# MAIN EXECUTION LOGGING STARTS

validLogin = 0
validLogin = login()
CalGoldRate()

if validLogin == 0:

    print('   Wrong User Name Or Password !')

elif validLogin == 1:
    ch = 0
    print()
    while True:
        MangMenu()
        ch = int(input('   Choose An Option From The Menu -: '))
        print()

        if ch == 1:
            addProduct()

        if ch == 2:
            addSupplier()
        if ch == 3:
            listProduct()

        if ch == 4:
            searchProduct()

        if ch == 5:
            addCustomer()

        if ch == 6:
            searchCustomer()

        if ch == 7:
            purchase()

        if ch == 8:
            UpdateQuantity()

        if ch == 9:
            salesReport()

        if ch == 10:
            payDetails()

        if ch == 11:
            addEmployee()

        elif ch == 12:
            exit()


elif validLogin == 2:
    ch = 0
    print()
    while True:
        NorMenu()
        ch = int(input('   Choose An Option From The Menu -: '))
        print()

        if ch == 1:
            listProduct()

        if ch == 2:
            searchProduct()

        if ch == 3:
            addCustomer()

        if ch == 4:
            searchCustomer()

        if ch == 5:
            purchase()

        if ch == 6:
            supDetails()

        elif ch == 7:
            exit()

