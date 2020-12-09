#ALL porject 2 app

import sqlite3 as sql
import random

acc_imp = ("y","n")

def home():
    print ("You are back to the begining of the program, press ENTER to continue...")
    input()
    return signup()

def signup():
    print ("Would you like to sign up ? y/n")
    ans = str(input())
    if ans in acc_imp:
        if ans == "y":
            return register()
        elif ans == "n":
            return is_user()
    else:
        print ("Not an acceptable input, try again. Please enter y or n ONLY")
        return signup()

def register ():
    print ("Welcome new user")
    #Generates unique login code

    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT Login FROM Customer")
    EveryLogin = c.fetchall()
    
    
    LOGIN = (random.randint(1000,9999)) #Randomly generates login code
    while LOGIN in EveryLogin: #Checks if unique login code already exitst
        LOGIN = (random.randint(1000,9999)) #If it does a login code is assigned
        continue #Keeps looping till assigned login code is not an login code
    print ("We have generated your customer ID")
    print (LOGIN)
    conn.close()

    print ("Please enter your first name")
    FNAME = str(input())
    print ("Please enter your last name")
    LNAME = str(input())
    print ("Please enter your gender e.g M/F")
    GENDER = str(input())
    print ("Please enter date of birth in this format 1JUL1997")
    DOB = str(input())
    print ("Please enter an email address")
    EMAIL = str(input())
    print ("Please enter a phonenumber")
    PHONENUMBER = int(input())

    xsessions = (1, 2, 3)
    sessions = (0, 1, 2, 3)
    print ("Please enter a session one ID ([1] weights, [2] cardio, [3] flexibility)")
    session1 = int(input())
    while session1 not in xsessions:
        print ("Enter a valid ID for session 1")
        session1 = int(input())
        
    print ("Please enter a session two ID ([1] weights, [2] cardio, [3] flexibility)")
    print ("If you aren't doing a second session enter [0]")
    session2 = int(input())
    while session2 not in sessions:
        print ("Enter a valid ID for session 2")
        session2 = int(input())

    if session2 == 0:
        session2 = 4

    print ("Please enter a session three ID ([1] weights, [2] cardio, [3] flexibility)")
    print ("If you aren't doing a third session enter [0]")
    session3 = int(input())
    while session3 not in sessions:
        print ("Enter a valid ID for session 3")
        session3 = int(input())
    
    if session3 == 0:
        session3 = 4

    if session2 == 4 and session3 == 4:
        fee = 1*15
        comment = "fee for one session in GBP£"
        
    elif session2 != 4 and session3 == 4:
        fee = 2*15
        comment = "fee for two sessions in GBP£"
    else:
        fee = 3*15
        comment = "fee for three sessions in GBP£"

    #Generates PIN
    PIN = (random.randint(100,999)) #Randomly generates PIN
    print ("We have generated your 3 digit PIN")
    print ("Your 3 digit PIN is", PIN, "Don't forget it")

    #Saves customer info to database
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("INSERT INTO Customer VALUES (:CID, :Fname, :Lname, :Gender, :DOB, :Email, :PhoneNumber, :Login, :PIN)",
              {'CID':None,'Fname': FNAME,'Lname': LNAME,'Gender': GENDER,'DOB': DOB,'Email': EMAIL,'PhoneNumber': PHONENUMBER,'Login': LOGIN,'PIN': PIN})
    conn.commit()

    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cidseq = c.fetchone()
    cid = cidseq[0]

    c.execute("INSERT INTO CustomerSession VALUES (:csCustID, :sID)",{'csCustID':cid,'sID':session1})
    c.execute("INSERT INTO CustomerSession VALUES (:csCustID, :sID)",{'csCustID':cid,'sID':session2})
    c.execute("INSERT INTO CustomerSession VALUES (:csCustID, :sID)",{'csCustID':cid,'sID':session3})

    c.execute("INSERT INTO Invoices VALUES (:InvoiceID, :iCustID, :Fee, :Comment)",{'InvoiceID':None,'iCustID':cid,'Fee':fee,'Comment':comment})

    conn.commit()
    conn.close()

    print ("Details SAVED, please keep a note of your login info")
    print ("LOGIN code :", LOGIN)
    print ("PIN :", PIN)
    return welcome(LOGIN, PIN)

#Function responsible for welcoming thing user
def welcome (LOGIN, PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cidseq = c.fetchone()
    cid = cidseq[0]

    c.execute("SELECT Fname AND Lname FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    names = c.fetchone()
    print ("Welcome user", names)

    conn.close()
    return data_collector (LOGIN,PIN,cid)

#Function responsible for gathering user data
def data_collector(LOGIN,PIN,cid):
    print ("please enter number of steps")
    s = input()
    print ("please enter calories burnt")
    c = input()
    print ("please enter time taken in seconds")
    t = input()
    print ("please enter heart rate")
    hr = input()
    print ("please enter weight")
    w = input()
    print ("please enter height in cm")
    h = input()
    print ("Calculating BMI...")

    try: #checks to see if user has entered numbers if not then the function is re-called
        steps = int(s)
        cals = float(c)
        time = int(t)
        hrt = float(hr)
        weight = float(w)
        height = float(h)

    except ValueError: #if the values cannot be converted to an int, tell the user what went wrong and recall the function
        print ("ERROR, please enter numbers ONLY")
        return data_collector(CID,PIN,name)

    #Calculates BMI
    bmi = round(weight/((height/100)**2),2)
    print ("BMI calculated", bmi)

    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("INSERT INTO Performance VALUES (:pCustID, :Weight, :Height, :CalsBurnt, :HeartRate, :TimeTaken, :BMI, :Steps)",
              {'pCustID': cid,'Weight': weight,'Height': height,'CalsBurnt': cals,'HeartRate': hrt,'TimeTaken': time,'BMI': bmi,'Steps': steps})
    conn.commit()
    conn.close()
    
    return data_processor(cid,cals,hrt,time,steps)

#Function responsible for taking collected data and pefroming certain actions and the given data
def data_processor(cid,cals,hrt,time,steps):
    score = round((cals+hrt+time+steps))
    if score < 1000:
        print("no discount")
        discountID = 4
        conn = sql.connect("GymDataBase.db")
        c = conn.cursor()
        c.execute("INSERT INTO CustomerDiscount VALUES (:cdCustID, :DiscID)",{'cdCustID': cid,'DiscID': discountID})
        conn.commit()
        conn.close()
        
    if score > 1000 and score <= 1500:
        print("You can do better !, 5% discount")
        discountID = 5
        conn = sql.connect("GymDataBase.db")
        c = conn.cursor()
        c.execute("INSERT INTO CustomerDiscount VALUES (:cdCustID, :DiscID)",{'cdCustID': cid,'DiscID': discountID})
        conn.commit()
        conn.close()
        
    if score > 1500 and score <= 2000:
        comment = "You're doing well, 10% discount"
        discountID = 1
        conn = sql.connect("GymDataBase.db")
        c = conn.cursor()
        c.execute("INSERT INTO CustomerDiscount VALUES (:cdCustID, :DiscID)",{'cdCustID': cid,'DiscID': discountID})
        conn.commit()
        conn.close()
        
    if score > 2000 and score <= 2500:
        comment = "You're doing very well ! 15% discount"
        discountID = 2
        conn = sql.connect("GymDataBase.db")
        c = conn.cursor()
        c.execute("INSERT INTO CustomerDiscount VALUES (:cdCustID, :DiscID)",{'cdCustID': cid,'DiscID': discountID})
        conn.commit()
        conn.close()
        
    if score > 2500:
        comment = "Your performance is amazing, 20% discount"
        discountID = 3
        conn = sql.connect("GymDataBase.db")
        c = conn.cursor()
        c.execute("INSERT INTO CustomerDiscount VALUES (:cdCustID, :DiscID)",{'cdCustID': cid,'DiscID': discountID})
        conn.commit()
        conn.close()

    print ("results save")
    return home()

#Function responsible for checking if a user is an existing customer
def is_user ():
    print ("Enter login code")
    L = input()
    print ("Enter PIN")
    P = input()

    try:
        LOGIN = int(L)
        PIN = int(P)

    except TypeError:
        print ("please enter numbers only")
        return is_user()

    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    loginvals = c.fetchone()
    if LOGIN and PIN in loginvals:
        conn.close()
        return output(LOGIN,PIN)
    else:
        print ("Couldnt find user")
        conn.close()
        return signup()

#Function responsible for displaying user data
def output(LOGIN,PIN):
    print("Press specified number to see related details")
    print(" ")
    print("[1] FOR PERSONAL DETAILS")
    print("[2] FOR PERFORMANCE & FITNESS INFO")
    print("[3] FOR INVOICES")
    print("[4] FOR DISCOUNTS")
    print("[5] FOR SESSIONS")
    print("              OR             ")
    print("[0] TO EXIT TO HOME")
    print(" ")
    u = input()
    try:
        USERIN = int(u)
    except TypeError:
        print ("please enter specified options ONLY")
        return output(LOGIN,PIN)

    if USERIN == 1:
        return personal_details(LOGIN,PIN)
    if USERIN == 2:
        return fitness_info(LOGIN,PIN)
    if USERIN == 3:
        return invoices(LOGIN,PIN)
    if USERIN == 4:
        return discounts(LOGIN,PIN)
    if USERIN == 5:
        return sessions(LOGIN,PIN)
    if USERIN == 0:
        return home()
    else:
        print ("Not a valid option, try again")
        return output(LOGIN,PIN) 

def personal_details(LOGIN,PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    customerdata = c.fetchone()
    print(*customerdata, sep = "\n")
    conn.close()
    print ("\n"+"press enter to go back")
    i = input ()
    return output(LOGIN,PIN)
    
def fitness_info(LOGIN,PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cid = c.fetchone()
    #cid = seq[0]
    c.execute("SELECT * FROM Performance WHERE pCustID = ?", (cid))
    fitnessdata = c.fetchone()
    print(*fitnessdata, sep = "\n")
    conn.close()
    print ("\n"+"press any enter to go back")
    i = input ()
    return output(LOGIN,PIN)

def invoices(LOGIN,PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cid = c.fetchone()
    c.execute("SELECT Fee, Comment FROM Invoices WHERE iCustID = ?", (cid))
    invoicedata = c.fetchall()
    print(*invoicedata, sep = "\n")
    conn.close()
    print ("\n"+"press enter to go back")
    i = input ()
    return output(LOGIN,PIN)

def discounts(LOGIN,PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cid = c.fetchone()
    #cid = seq[0]
    c.execute("SELECT DiscID FROM CustomerDiscount WHERE cdCustID = ?", (cid))
    discountids = c.fetchall()
    for dID in discountids:
        c.execute("SELECT Ammount FROM Discount WHERE DiscountID = ?", (dID))
        discounts = c.fetchone()
        print ("Discount/s \n", discounts)

    conn.close()
    print ("\n"+"press enter to go back")
    i = input ()
    return output(LOGIN,PIN)

def sessions(LOGIN,PIN):
    conn = sql.connect("GymDataBase.db")
    c = conn.cursor()
    c.execute("SELECT CID FROM Customer WHERE Login = ? AND PIN = ?", (LOGIN, PIN))
    cid = c.fetchone()

    c.execute("SELECT sID FROM CustomerSession WHERE csCustID = ?", (cid))
    sessionids = c.fetchall()
    for SID in sessionids:
        c.execute("SELECT SessionName FROM Session WHERE SessionID = ?", (SID))
        Sessions = c.fetchone()
        print ("Session \n", Sessions)

    conn.close()
    print ("\n"+"press enter to go back")
    i = input ()
    return output(LOGIN,PIN)
    
home()
