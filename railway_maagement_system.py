from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import mysql.connector 

global db
global arrival
global arr

con = mysql.connector.connect(host ="localhost", user = "root", password = "Summer123&")

cur = con.cursor()

cur.execute("create database if not exists train")
cur.execute("use train")

# create tables
cur.execute("create table if not exists passengers(name varchar(30),age int,gender varchar(10),phn_no int,trn_nme varchar(20),cls varchar(10),frm varchar(20),to_ varchar(20),dte varchar(10),tme varchar(10),pid varchar(40),trn_no int)")
cur.execute("create table if not exists train(frm varchar(50),to_ varchar(50),dte varchar(20),tme varchar(20),trn_nme varchar(100),pantry varchar(100),trn_no bigint)")
cur.execute("create table if not exists admin (name varchar(100), id varchar(100))") 
def warnMessage(msg1,msg2):
    messagebox.showwarning(msg1,msg2)

def infoMessage(msg1,msg2):
    messagebox.showinfo(msg1,msg2)

def bookTicket(arrival): # Book Ticket Function For Database
    
    arr = [str(x.get()) for x in arrival]
    mi = min(arr)

    if ((mi!="") and (mi!="")):
            cur.execute(" select * from train where trn_no ='{}'".format(arr[-1]))
            flag = cur.fetchall()

            if(flag):

                cur.execute("""insert into passengers(name,age,gender,phn_no,trn_nme,cls,frm,to_,dte,tme,pid,trn_no) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",arr)
                
                print(arrival)
                for x in arrival:
                    x.delete(0,END)
                infoMessage("Train Ticket Reservation","Ticket Booked")
                print("ticket booked")
                con.commit()

            else:
                warnMessage("Train Ticket Reservetion - Admin","Invalid Train Number")

    else:
        warnMessage("Train Ticket Reservation","Please Fill All The Fields !!!")
        print("ticket not booked")


def inputTrain(fn):#arrival

    arr = [str(x.get()) for x in arrival]
    mi = min(arr)
    
    if ((mi!="") and (mi!=" ")):

        if(fn=="Insert"):

            cur.execute("""insert into train(frm,to_,dte,tme,trn_nme,pantry,trn_no) values (%s,%s,%s,%s,%s,%s,%s)""",arr)

            print(arrival)
            for x in arrival:
                x.delete(0,END)
            txtm = "Train " + fn +"ed" 
            infoMessage("Train Ticket Reservation - Admin",txtm)
            print(fn + " - train - query")
            con.commit()

        else:
            cur.execute(" select * from train where trn_no ='{}'".format(arr[-1]))
            flag = cur.fetchall()
            if(flag):
                cur.execute("""update train set frm =%s ,to_ =%s ,dte =%s ,tme =%s ,trn_nme =%s ,pantry =%s where trn_no =%s""",arr)

                print(arrival)
                for x in arrival:
                    x.delete(0,END)
                txtm = "Train " + fn +"ed" 
                infoMessage("Train Ticket Reservation - Admin",txtm)
                print(fn + " - train - query")
                con.commit()
            else:
                warnMessage("Train Ticket Reservetion - Admin","Invalid Train Number")
                print(fn + " - train - query - warning - invalid tn")
    else:
        warnMessage("Train Ticket Reservation - Admin","Please Fill All The Fields !!!")

        print(fn + " - train - query")

def deleteTrain(arrival):

    arr = [str(x.get()) for x in arrival]
    mi = min(arr)

    if ((mi!="") and (mi!=" ")):

        cur.execute(" select * from train where trn_no ='{}'".format(arr[0]))
        flag = cur.fetchall()

        if(flag):
            cur.execute("""delete from train where trn_no =%s""",arr)

            for x in arrival:
                x.delete(0,END)

            infoMessage("Train Ticket Reservation - Admin","Train Deleted")

            print("Deleted - train - query")
            con.commit()
        else:
            warnMessage("Train Ticket Reservetion - Admin","Invalid Train Number")
            print("Delete - train - query - warning - inv tn")
    else:
        warnMessage("Train Ticket Reservation - Admin","Please Enter Train No")

        print("Delete - train - query")


def cancelTicket(arrival):
    l=[] 
    arr = [str(x.get()) for x in arrival]
    mi = min(arr)
##    l.append(arr[0])
    
    

    if ((mi!="") and (mi!=" ")):

        cur.execute(" select * from passengers where name ='{}'".format(arr[0]))
        flag = cur.fetchall()

        if(flag):
            cur.execute("delete from passengers where name ='{}'".format(arr[0]))

            for x in arrival:
                x.delete(0,END)

            infoMessage("Train Ticket Reservation","Train Ticket Cancelled")

            print("Deleted - train - ticket - query")
            con.commit()
        else:
            warnMessage("Train Ticket Reservetion - Admin","Invalid Passenger ID (or) Train Number")
            print("Delete - train - query - warning - inv tn")
    else:
        warnMessage("Train Ticket Reservation","Please Fill The Fields")

        print("Delete - train - Ticket - query")


def passadmntab(tree):

    cur.execute("""select * from passengers""")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)  

    print("passengers - admin - view")


def adminLogin(admin):
    
    admn_nme = str(admin[0].get())
    admn_id = str(admin[1].get())

    if((admn_nme == "") or (admn_nme == " ")or(admn_id == "") or (admn_id == " ")):
        warnMessage("Train Ticket Reservation","Please Fill The Fields")
    
    else:
        cur.execute(" select * from admin where name ='{}' and id ='{}'".format(admn_nme,admn_id ))
        flag = cur.fetchall()

        if(flag):
            adminWindow()
            print(" admin login success")

        else:
            warnMessage("Train Ticket Reservation","Please Enter Correct Admin Name & Admin ID  !!!")


def viewTrainArrival(tree):
    cur.execute("""select * from train""")
    rows = cur.fetchall()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert("", tk.END, values=row)
    print("available trains")


def passengerAdmin():

    passadwin = tk.Tk()
    passadwin.resizable(False,False)
    passadwin.title("Train Ticket Reservation")
    
    tree = ttk.Treeview(passadwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12"), show='headings')
    tree.column("c1", width=110,anchor='c')
    tree.heading("c1", text="Name")

    tree.column("c2", width=110,anchor='se')
    tree.heading("c2", text="Age")

    tree.column("c3", width=110,anchor='se')
    tree.heading("c3", text="Gender")

    tree.column("c4",width=110, anchor='se')
    tree.heading("c4", text="Phone Number")

    tree.column("c5",width=110, anchor='se')
    tree.heading("c5", text="Train Name")

    tree.column("c6",width=110, anchor='se')
    tree.heading("c6", text="Class")

    tree.column("c7",width=110, anchor='se')
    tree.heading("c7", text="From")

    tree.column("c8",width=110, anchor='se')
    tree.heading("c8", text="To")
    
    tree.column("c9",width=110, anchor='se')
    tree.heading("c9", text="Date")

    tree.column("c10",width=110, anchor='se')
    tree.heading("c10", text="Time")

    tree.column("c11",width=110, anchor='se')
    tree.heading("c11", text="Train Number")

    tree.column("c12",width=110, anchor='se')
    tree.heading("c12", text="Passenger ID")

    tree.pack()

    passadmntab(tree)

    print("passengers - admin")


def admin():
    trnadmnwin = tk.Tk()
    trnadmnwin.resizable(False,False)
    trnadmnwin.title("Train Ticket Reservation - Admin")

    trnadtree = ttk.Treeview(trnadmnwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    trnadtree.column("c1", width=110,anchor='c')
    trnadtree.heading("c1", text="From")

    trnadtree.column("c2", width=110,anchor='se')
    trnadtree.heading("c2", text="To")

    trnadtree.column("c3", width=110,anchor='se')
    trnadtree.heading("c3", text="Date")

    trnadtree.column("c4",width=110, anchor='se')
    trnadtree.heading("c4", text="Time")

    trnadtree.column("c5",width=110, anchor='se')
    trnadtree.heading("c5", text="Train_Name")

    trnadtree.column("c6",width=110, anchor='se')
    trnadtree.heading("c6", text="Pantry")

    trnadtree.column("c7",width=110, anchor='se')
    trnadtree.heading("c7", text="Train_no")

    trnadtree.grid(row=1,column=0,columnspan=4,pady=3)

    upbtn = tk.Button(trnadmnwin,text="Update",command=lambda:[inputTrain("Update")],height=2,width=16)
    inbtn =  tk.Button(trnadmnwin,text="Insert",command=lambda:[inputTrain("Insert")],height=2,width=16)
    delbtn =  tk.Button(trnadmnwin,text="Delete",command=deleteTrain,height=2,width=16)
    refbtn = tk.Button(trnadmnwin,text="Refresh",command=lambda:[viewTrainArrival(trnadtree)],height=2,width=16)
    
    upbtn.grid(row=0,column=0,pady=5)
    inbtn.grid(row=0,column=1,pady=5)
    delbtn.grid(row=0,column=2,pady=5)
    refbtn.grid(row=0,column=3,pady=5)

    print("Train - admin view")


def trainAvailable(): # Train Available
    
    trnavalwin = tk.Tk()
    trnavalwin.resizable(False,False)
    trnavalwin.title("Train Ticket Reservation")
    
    tree = ttk.Treeview(trnavalwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    
    tree.column("c1", width=110,anchor='c')
    tree.heading("c1", text="From")

    tree.column("c2", width=110,anchor='se')
    tree.heading("c2", text="To")

    tree.column("c3", width=110,anchor='se')
    tree.heading("c3", text="Date")

    tree.column("c4",width=110, anchor='se')
    tree.heading("c4", text="Time")

    tree.column("c5",width=110, anchor='se')
    tree.heading("c5", text="Train_Name")

    tree.column("c6",width=110, anchor='se')
    tree.heading("c6", text="Pantry")

    tree.column("c7",width=110, anchor='se')
    tree.heading("c7", text="Train_no")

    tree.pack()
    viewTrainArrival(tree)

    print("Train Available")


def deleteTrain():
    delwin = tk.Tk()
    delwin.resizable(False,False)
    delwin.title("Train Ticket Reservation - Admin")

    trnnol = Label(delwin,text="Train no :").grid(row = 0,column=0,padx=5,pady=5)
    trnno = Entry(delwin,width=37)
    trnno.grid(row = 0,column=1,padx=20,pady=5)

    arr = [trnno]

    submitbtn = tk.Button(delwin,text="Delete Train", command=lambda:[deleteTrain()])#,tcktbookdmsg()
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)
    
    print("delete - train")


def inputTrain(fn):

    inupwin = tk.Tk()
    inupwin.resizable(False,False)
    inupwin.title("Train Ticket Reservation - Admin")

    Froml = Label(inupwin,text="From :").grid(row = 0,column=0,padx=5,pady=5)
    frm = Entry(inupwin,width=37)
    frm.grid(row = 0,column=1,padx=20,pady=5)
    

    Tol = Label(inupwin,text="To :").grid(row = 1,column=0,padx=5,pady=5)
    to_ = Entry(inupwin,width=37)
    to_.grid(row = 1,column=1,padx=20,pady=5)

    Datel = Label(inupwin,text="Date :").grid(row = 2,column=0,padx=5,pady=5)
    dte = Entry(inupwin,width=37)
    dte.grid(row = 2,column=1,padx=20,pady=5)

    Timel = Label(inupwin,text="Time :").grid(row = 3,column=0,padx=5,pady=5)
    tme = Entry(inupwin,width=37)
    tme.grid(row = 3,column=1,padx=5,pady=5)

    Train_nol = Label(inupwin,text="Train name :").grid(row = 4,column=0,padx=5,pady=5)
    trn_no = Entry(inupwin,width=37)
    trn_no.grid(row = 4,column=1,padx=5,pady=5)

    Train_namel = Label(inupwin,text="pantry:").grid(row = 5,column=0,padx=5,pady=5)
    trn_nme = Entry(inupwin,width=37)
    trn_nme.grid(row = 5,column=1,padx=5,pady=5)

    Pantryl = Label(inupwin,text="Train_no :").grid(row = 6,column=0,padx=5,pady=5)
    pnt = Entry(inupwin,width=37)
    pnt.grid(row = 6,column=1,padx=20,pady=5)

    arr = [frm,to_,dte,tme,trn_nme,pnt,trn_no]

    txt = fn + " " + "Train"
    submitbtn = tk.Button(inupwin,text=txt, command=lambda:[inputTrain(fn)])
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

    print(fn + " - train - query")


def ticketCancel():

    tcwin = tk.Tk()
    tcwin.geometry("360x220")
    tcwin.title("Train Ticket Reservation - Train")

    P_id = Label(tcwin,text="Passenger name :")
    P_id.grid(row=0, column=0,padx=10,pady=20)
    pid = Entry(tcwin,width=37)
    pid.grid(row=0, column=1,padx=10,pady=20,ipady=2.2)
    
    Train_no = Label(tcwin,text="Train No :")
    Train_no.grid(row=1, column=0,padx=10,pady=20)
    trn_no = Entry(tcwin,width=37)
    trn_no.grid(row=1, column=1,padx=10,pady=20,ipady=2.21)

    tc = [pid,trn_no]

    cnclbtn = Button(tcwin,text = "Cancel Ticket", command= lambda:[cancelTicket(tc)])
    cnclbtn.grid(row=2,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

def ticketReservation():
    scndwin = tk.Tk()
    scndwin.resizable(False,False)
    scndwin.title("Train Ticket Reservation")

    Pidl = Label(scndwin,text="ID :").grid(row = 0,column=0,padx=5,pady=5)
    pid = Entry(scndwin,width=37)
    pid.grid(row = 0,column=1,padx=20,pady=5)
    

    Namel = Label(scndwin,text="Name :").grid(row = 1,column=0,padx=5,pady=5)
    name = Entry(scndwin,width=37)
    name.grid(row = 1,column=1,padx=20,pady=5)

    Agel = Label(scndwin,text="Age :").grid(row = 2,column=0,padx=5,pady=5)
    age = Entry(scndwin,width=37)
    age.grid(row = 2,column=1,padx=20,pady=5)

    Genderl = Label(scndwin,text="Gender :").grid(row = 3,column=0,padx=5,pady=5)
    gender = Entry(scndwin,width=37)
    gender.grid(row = 3,column=1,padx=5,pady=5)

    Phone_no = Label(scndwin,text="Phone no :").grid(row = 4,column=0,padx=5,pady=5)
    phn_no = Entry(scndwin,width=37)
    phn_no.grid(row = 4,column=1,padx=5,pady=5)

    Train_name = Label(scndwin,text="Train Name :").grid(row = 5,column=0,padx=5,pady=5)
    trn_nme = Entry(scndwin,width=37)
    trn_nme.grid(row = 5,column=1,padx=5,pady=5)

    Train_nol = Label(scndwin,text="Train no :").grid(row = 6,column=0,padx=5,pady=5)
    trn_no = Entry(scndwin,width=37)
    trn_no.grid(row = 6,column=1,padx=20,pady=5)
    
    Class_ = Label(scndwin,text="Class :").grid(row = 7,column=0,padx=5,pady=5)
    cls_ = Entry(scndwin,width=37)
    cls_.grid(row = 7,column=1,padx=5,pady=5)
    
    from_ = Label(scndwin,text="From :").grid(row = 8,column=0,padx=5,pady=5)
    frm = Entry(scndwin,width=37)
    frm.grid(row = 8,column=1,padx=5,pady=5)
    
    To_ = Label(scndwin,text="To :").grid(row = 9,column=0,padx=5,pady=5)
    to_ = Entry(scndwin,width=37)
    to_.grid(row = 9,column=1,padx=5,pady=5)
    
    Date = Label(scndwin,text="Date :").grid(row = 10,column=0,padx=5,pady=5)
    date = Entry(scndwin,width=37)
    date.grid(row = 10,column=1,padx=5,pady=5)
    
    Time_ = Label(scndwin,text="Time :").grid(row = 11,column=0,padx=5,pady=5)
    time_ = Entry(scndwin,width=37)
    time_.grid(row = 11,column=1,padx=5,pady=5)

    arr = [name,age,gender,phn_no,trn_nme,cls_,frm,to_,date,time_,pid,trn_no]


    submitbtn = tk.Button(scndwin,text="Book Ticket", command=lambda:[bookTicket(arr)])#,tcktbookdmsg()
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)


    print("ticket reserved")

def adminLog():
    adlogwin = tk.Tk()
    adlogwin.resizable(False,False)
    adlogwin.geometry("360x220")
    adlogwin.title("Train Ticket Reservation - Train")
    adlogwin.configure(bg='orange')

    Admin_name = Label(adlogwin,text="Admin Name :",bg='thistle3',width=20,font=("arial",10,"bold"))
    Admin_name.grid(row=0, column=0,padx=10,pady=20)
    admin_nme = Entry(adlogwin,width=37)
    admin_nme.grid(row=0, column=1,padx=10,pady=20,ipady=2.2)
    
    Admin_id = Label(adlogwin,text="Admin ID :",bg='thistle3',width=20,font=("arial",10,"bold"))
    Admin_id.grid(row=1, column=0,padx=10,pady=20)
    admin_id = Entry(adlogwin,width=37)
    admin_id.grid(row=1, column=1,padx=10,pady=20,ipady=2.21)

    admn = [admin_nme,admin_id]

    logbtn = Button(adlogwin,text = "Login", command= lambda:[adminLogin(admn)])
    logbtn.grid(row=2,column=0,columnspan=2,padx=10,pady=10,ipadx=100)
    logbtn.configure(bg='yellow')


    print("admin login")    

    
def adminWindow():
    adwin = tk.Tk()
    adwin.resizable(False,False)
    adwin.geometry("360x245")
    adwin.title("Train Ticket Reservation - Admin")
    adwin.configure(bg='purple')


    trnbtn = tk.Button(adwin,text="Train",command=admin,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
    passbtn =  tk.Button(adwin,text="Passengers",command=passengerAdmin,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))

    trnbtn.grid(row=0,column=1)
    passbtn.grid(row=1,column=2)

    trnbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
    passbtn.place(relx=0.5, rely=0.7, anchor=S)

def ticket(): 
    tcktwin = tk.Tk()
    tcktwin.resizable(False,False)
    tcktwin.title("Train Ticket Reservation")
    tcktwin.geometry("300x245")
    tcktwin.configure(bg='pink')

    trnavalbtn = tk.Button(tcktwin,text="Train Available",command=trainAvailable,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
    tcktresbtn =  tk.Button(tcktwin,text="Ticket Reservation",command=ticketReservation,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
    tcktcnclbtn =  tk.Button(tcktwin,text="Ticket Cancelation",command=ticketCancel,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))


    trnavalbtn.grid(row=0,column=1)
    tcktresbtn.grid(row=1,column=1)
    tcktcnclbtn.grid(row=2,column=1)

    trnavalbtn.place(relx=0.5, rely=0.05, anchor=N)
    tcktresbtn.place(relx=0.5, rely=0.37, anchor=N)
    tcktcnclbtn.place(relx=0.5, rely=0.70, anchor=N)

def adminSignup():
    def submit(na,id):
        cur.execute("insert into admin values (%s,%s)",(na,id))
        con.commit()
        infoMessage('Alert','Seat added succesfully')
        adsignwin.destroy()
    adsignwin = tk.Tk()
    adsignwin.resizable(False,False)
    adsignwin.geometry("360x220")
    adsignwin.title("Train Ticket Reservation - Admin")
    adsignwin.configure(bg='blue')

    name = Label(adsignwin,text="Name:",bg='thistle3',width=20,font=("arial",10,"bold"))
    name.grid(row=0, column=0,padx=10,pady=20)
    nme = Entry(adsignwin,width=37)
    nme.grid(row=0, column=1,padx=10,pady=20,ipady=2.2)

    id = Label(adsignwin,text='ID:',bg='thistle3',width=20,font=("arial",10,"bold"))
    id.grid(row=1,column=0)
    idEnt = Entry(adsignwin,width=37)
    idEnt.grid(row=1,column=1,padx=10,pady=20,ipady=2.21)

    Button(adsignwin,text='submit',command=lambda:submit(nme.get(),idEnt.get())).grid(row=2,column=1,padx=10,pady=10,ipadx=100)

root = tk.Tk()
root.geometry("1000x1000")
root.configure(bg='yellow')


root.title("Train Ticket Reservation")
root.geometry("300x245")
ss="RAILWAY MANAGEMENT SYSTEM"
sliderlabel=Label(root,text=ss,relief="solid",width=30,font=("SegoeScript",30,"bold"))
sliderlabel.place(x=450,y=10)

adminbtn = tk.Button(root,text="Admin Login",command=adminLog,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
tktresbtn =  tk.Button(root,text="Passengers",command=ticket,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
adminsign = tk.Button(root,text='Admin Signup',command=adminSignup,height=3,width=16,bg="deeppink",fg="white",font=("Segoe Script",12,"bold"))
from PIL import ImageTk, Image
frame = Frame(root, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("images.jpg"))
label = Label(frame, image = img)
label.pack()

con.commit()

adminbtn.place(relx=0.5, rely=0.05, anchor=N)
tktresbtn.place(relx=0.5, rely=0.37, anchor=N)
adminsign.place(relx=0.5, rely=0.70, anchor=N)

adminbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
tktresbtn.place(relx=0.5, rely=0.7, anchor=S)

mainloop()

con.close()


