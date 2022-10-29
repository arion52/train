from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import mysql.connector

global db

myCon = mysql.connector.connect(host="localhost", user="root", password="Root.123")

myCur = myCon.cursor()

myCur.execute("create database if not exists train")
myCur.execute("use train")


# create tables
def warnMessage(msg1, msg2):
    messagebox.showwarning(msg1, msg2)


def infoMessage(msg1, msg2):
    messagebox.showinfo(msg1, msg2)




def inpTrain(fn, arrival):
    arr = [str(x.get()) for x in arrival]
    mi = min(arr)

    if mi in ["", " "]:
        warnMessage("Train Ticket Reservation - Admin", "Please Fill All The Fields !!!")

        print(fn + " - train - query")

    elif fn == "Insert":
        myCur.execute("insert into train(name,Number,fromPlace,toPlace) values (%s,%s,%s,%s,%s,%s,%s)",arr)
        print(arrival)
        for x in arrival:
            x.delete(0, END)
        txtm = "Train " + fn + "ed"
        infoMessage("Train Ticket Reservation - Admin", txtm)
        print(fn + " - train - query")
        myCon.commit()

    else:
        myCur.execute("select * from train where trn_no ='" + arr[-1] + "'")
        if flag := myCur.fetchall():
            myCur.execute(
                "update train set name=%s,fromPlace=%s,toPlace=%s where Number =%s",arr)
            print(arrival)
            for x in arrival:
                x.delete(0, END)
            txtm = "Train " + fn + "ed"
            infoMessage("Train Ticket Reservation - Admin", txtm)
            print(fn + " - train - query")
            myCon.commit()
        else:
            warnMessage("Train Ticket Reservation - Admin", "Invalid Train Number")
            print(fn + " - train - query - warning - inv tn")


def deleteTrain(arrival):
    arr = [str(x.get()) for x in arrival]
    mi = min(arr)

    if mi not in ["", " "]:

        myCur.execute("select * from train where Number ='" + arr[1] + "'")
        if flag := myCur.fetchall():
            myCur.execute("delete from train where trn_no =%s", arr)

            for x in arrival:
                x.delete(0, END)

            infoMessage("Train Ticket Reservation - Admin", "Train Deleted")

            print("Deleted - train - query")
            myCon.commit()
        else:
            warnMessage("Train Ticket Reservation - Admin", "Invalid Train Number")
            print("Delete - train - query - warning - inv tn")
    else:
        warnMessage("Train Ticket Reservation - Admin", "Please Enter Train No")

        print("Delete - train - query")



def adminLogin(ad):
    adminName = str(ad[0].get())
    adminId = str(ad[1].get())

    if not adminName or adminName == " " or not adminId or adminId == " ":
        warnMessage("Train Ticket Reservation", "Please Fill The Fields")

    else:
        myCur.execute("select * from admin where name ='" + adminName + "' and id ='" + adminId + "'")
        if flag := myCur.fetchall():
            adminWindow()
            print("admin login success")

        else:
            warnMessage("Train Ticket Reservation", "Please Enter Correct Admin Name & Admin ID  !!!")


def viewTrainArrival(tree):
    myCur.execute("select * from trains")
    rows = myCur.fetchall()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert("", tk.END, values=row)
    print("avail train")


def passengerAdmin():
    def passAdminTab(tree):
        myCur.execute("select * from passengers")
        rows = myCur.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

        print("passengers - ad - view")

    passAdWin = tk.Tk()
    passAdWin.resizable(False, False)
    passAdWin.title("Train Ticket Reservation")
    col = ['c'+str(x) for x in range(1,10)]
    tree = ttk.Treeview(passAdWin, columns=col, show='headings')
    tree.heading("c1", text="Name")
    tree.heading("c2", text="Age")
    tree.heading("c3", text="Train Name")
    tree.heading("c4", text="Train Number")
    tree.heading("c5", text="Date")
    tree.heading("c6", text="Time")
    tree.heading("c7", text="From")
    tree.heading("c8", text="To")
    tree.heading("c9", text="Phone")
    tree.pack()
    passAdminTab(tree)
    print("passengers - ad")


def admin():
    trnadmnwin = tk.Tk()
    trnadmnwin.resizable(False, False)
    trnadmnwin.title("Train Ticket Reservation - Admin")
    col = ['c'+str(x) for x in range(1,5)]
    trnadtree = ttk.Treeview(trnadmnwin, columns=col, show='headings')
    trnadtree.heading("c1", text="Name")
    trnadtree.heading("c2", text="Number")
    trnadtree.heading("c3", text="From")
    trnadtree.heading("c4", text="To")
    trnadtree.grid(row=1, column=0, columnspan=4, pady=3)
    upbtn = tk.Button(trnadmnwin, text="Update", command=lambda: [inputTrain("Update")], height=2, width=16)
    inbtn = tk.Button(trnadmnwin, text="Insert", command=lambda: [inputTrain("Insert")], height=2, width=16)
    delbtn = tk.Button(trnadmnwin, text="Delete", command=deleteTrain, height=2, width=16)
    refbtn = tk.Button(trnadmnwin, text="Refresh", command=lambda: [viewTrainArrival(trnadtree)], height=2, width=16)

    upbtn.grid(row=0, column=0, pady=5)
    inbtn.grid(row=0, column=1, pady=5)
    delbtn.grid(row=0, column=2, pady=5)
    refbtn.grid(row=0, column=3, pady=5)

    print("Train - ad view")


def trainAvailable():  # Train Available

    def submit(tree):
        myCur.execute("select * from trains")
        rows = myCur.fetchall()

        for i in tree.get_children():
            tree.delete(i)

        for row in rows:
            tree.insert('',"end", values=row)
            
    tk = Tk()
    tk.title("Train Ticket Reservation")
    col = ['c'+str(x) for x in range(1,5)]
    tree = ttk.Treeview(tk,columns=col, show='headings')
    tree.heading("c1", text="Name")
    tree.heading("c2", text="Number")
    tree.heading("c3", text="From")
    tree.heading("c4", text="To")
    tree.pack()
    submit(tree)
    tk.mainloop()


def deleteTrain():
    delwin = tk.Tk()
    delwin.resizable(False, False)
    delwin.title("Train Ticket Reservation - Admin")

    trnnol = Label(delwin, text="Train no :").grid(row=0, column=0, padx=5, pady=5)
    trnno = Entry(delwin, width=37)
    trnno.grid(row=0, column=1, padx=20, pady=5)

    arr = [trnno]

    submitbtn = tk.Button(delwin, text="Delete Train", command=lambda: [deleteTrain(arr)])  # ,tcktbookdmsg()
    submitbtn.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    print("delete - train")


def inputTrain(fn):  # sourcery skip: extract-duplicate-method
    inupwin = tk.Tk()
    inupwin.resizable(False, False)
    inupwin.title("Train Ticket Reservation - Admin")

    Label(inupwin, text="From :").grid(row=0, column=0, padx=5, pady=5)
    frm = Entry(inupwin, width=37)
    frm.grid(row=0, column=1, padx=20, pady=5)

    Label(inupwin, text="To :").grid(row=1, column=0, padx=5, pady=5)
    to_ = Entry(inupwin, width=37)
    to_.grid(row=1, column=1, padx=20, pady=5)

    Label(inupwin, text="Date :").grid(row=2, column=0, padx=5, pady=5)
    dte = Entry(inupwin, width=37)
    dte.grid(row=2, column=1, padx=20, pady=5)

    Label(inupwin, text="Time :").grid(row=3, column=0, padx=5, pady=5)
    tme = Entry(inupwin, width=37)
    tme.grid(row=3, column=1, padx=5, pady=5)

    Label(inupwin, text="Train no :").grid(row=4, column=0, padx=5, pady=5)
    trn_no = Entry(inupwin, width=37)
    trn_no.grid(row=4, column=1, padx=5, pady=5)

    Label(inupwin, text="Train Name :").grid(row=5, column=0, padx=5, pady=5)
    trn_nme = Entry(inupwin, width=37)
    trn_nme.grid(row=5, column=1, padx=5, pady=5)

    Label(inupwin, text="Pantry :").grid(row=6, column=0, padx=5, pady=5)
    pnt = Entry(inupwin, width=37)
    pnt.grid(row=6, column=1, padx=20, pady=5)

    arr = [frm, to_, dte, tme, trn_nme, pnt, trn_no]

    txt = fn + " " + "Train"
    submitbtn = tk.Button(inupwin, text=txt, command=lambda: [inpTrain(fn, arr)])
    submitbtn.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    print(fn + " - train - query")


def ticketCancel():
    def cancelTicket(arrival):
        arr = [str(x.get()) for x in arrival]
        mi = min(arr)

        if mi not in ["", " "]:

            myCur.execute("select * from passengers where pid ='" + arr[0] + "' and trn_no ='" + arr[1] + "'")
            flag = myCur.fetchall()

            if flag:
                myCur.execute("delete from passengers where pid =%s", arr[0])

                for x in arrival:
                    x.delete(0, END)

                infoMessage("Train Ticket Reservation", "Train Ticket Cancelled")

                print("Deleted - train - ticket - query")
                myCon.commit()
            else:
                warnMessage("Train Ticket Reservation - Admin", "Invalid Passenger ID (or) Train Number")
                print("Delete - train - query - warning - inv tn")
        else:
            warnMessage("Train Ticket Reservation", "Please Fill The Fields")

            print("Delete - train - Ticket - query")

    tcwin = tk.Tk()
    tcwin.geometry("360x220")
    tcwin.title("Train Ticket Reservation - Train")

    P_id = Label(tcwin, text="Passenger ID :")
    P_id.grid(row=0, column=0, padx=10, pady=20)
    pid = Entry(tcwin, width=37)
    pid.grid(row=0, column=1, padx=10, pady=20, ipady=2.2)

    Train_no = Label(tcwin, text="Train No :")
    Train_no.grid(row=1, column=0, padx=10, pady=20)
    trn_no = Entry(tcwin, width=37)
    trn_no.grid(row=1, column=1, padx=10, pady=20, ipady=2.21)

    tc = [pid, trn_no]

    cnclbtn = Button(tcwin, text="Cancel Ticket", command=lambda: [cancelTicket(tc)])
    cnclbtn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=100)


def ticketReservation():
    def bookTicket(arrival):
        arr = [str(x.get()) for x in arrival]
        mi = min(arr)

        if mi not in ["", ""]:
            myCur.execute("select * from train where trn_no ='" + arr[-1] + "'")
            flag = myCur.fetchall()

            if flag:

                myCur.execute(
                    "insert into passengers(name,age,gender,phNo,trainName,class,from,to,date,time,paid,trainNo) values ("
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", arr)

                print(arrival)
                for x in arrival:
                    x.delete(0, END)
                infoMessage("Train Ticket Reservation", "Ticket Booked")
                print("ticket booked")
                myCon.commit()

            else:
                warnMessage("Train Ticket Reservation - Admin", "Invalid Train Number")

        else:
            warnMessage("Train Ticket Reservation", "Please Fill All The Fields !!!")
            print("ticket not booked")

    scndwin = tk.Tk()
    scndwin.resizable(False, False)
    scndwin.title("Train Ticket Reservation")

    Label(scndwin, text="ID :").grid(row=0, column=0, padx=5, pady=5)
    pid = Entry(scndwin, width=37)
    pid.grid(row=0, column=1, padx=20, pady=5)

    Label(scndwin, text="Name :").grid(row=1, column=0, padx=5, pady=5)
    name = Entry(scndwin, width=37)
    name.grid(row=1, column=1, padx=20, pady=5)

    Label(scndwin, text="Age :").grid(row=2, column=0, padx=5, pady=5)
    age = Entry(scndwin, width=37)
    age.grid(row=2, column=1, padx=20, pady=5)

    Label(scndwin, text="Gender :").grid(row=3, column=0, padx=5, pady=5)
    gender = Entry(scndwin, width=37)
    gender.grid(row=3, column=1, padx=5, pady=5)

    Label(scndwin, text="Phone no :").grid(row=4, column=0, padx=5, pady=5)
    phn_no = Entry(scndwin, width=37)
    phn_no.grid(row=4, column=1, padx=5, pady=5)

    Label(scndwin, text="Train Name :").grid(row=5, column=0, padx=5, pady=5)
    trn_nme = Entry(scndwin, width=37)
    trn_nme.grid(row=5, column=1, padx=5, pady=5)

    Label(scndwin, text="Train no :").grid(row=6, column=0, padx=5, pady=5)
    trn_no = Entry(scndwin, width=37)
    trn_no.grid(row=6, column=1, padx=20, pady=5)

    Label(scndwin, text="Class :").grid(row=7, column=0, padx=5, pady=5)
    clas = Entry(scndwin, width=37)
    clas.grid(row=7, column=1, padx=5, pady=5)

    Label(scndwin, text="From :").grid(row=8, column=0, padx=5, pady=5)
    frm = Entry(scndwin, width=37)
    frm.grid(row=8, column=1, padx=5, pady=5)

    Label(scndwin, text="To :").grid(row=9, column=0, padx=5, pady=5)
    To = Entry(scndwin, width=37)
    To.grid(row=9, column=1, padx=5, pady=5)

    Label(scndwin, text="Date :").grid(row=10, column=0, padx=5, pady=5)
    date = Entry(scndwin, width=37)
    date.grid(row=10, column=1, padx=5, pady=5)

    Label(scndwin, text="Time :").grid(row=11, column=0, padx=5, pady=5)
    time_ = Entry(scndwin, width=37)
    time_.grid(row=11, column=1, padx=5, pady=5)

    arr = [name, age, gender, phn_no, trn_nme, clas, frm, To, date, time_, pid, trn_no]

    submitBtn = tk.Button(scndwin, text="Book Ticket", command=lambda: [bookTicket(arr)])  # ,tcktbookdmsg()
    submitBtn.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    print("ticket reserved")


def adminLog():
    adlogwin = tk.Tk()
    adlogwin.resizable(False, False)
    adlogwin.geometry("360x220")
    adlogwin.title("Train Ticket Reservation - Train")

    Admin_name = Label(adlogwin, text="Admin Name :")
    Admin_name.grid(row=0, column=0, padx=10, pady=20)
    admin_nme = Entry(adlogwin, width=37)
    admin_nme.grid(row=0, column=1, padx=10, pady=20, ipady=2.2)

    Admin_id = Label(adlogwin, text="Admin ID :")
    Admin_id.grid(row=1, column=0, padx=10, pady=20)
    admin_id = Entry(adlogwin, width=37)
    admin_id.grid(row=1, column=1, padx=10, pady=20, ipady=2.21)

    Admin = [admin_nme, admin_id]

    logbtn = Button(adlogwin, text="Login", command=lambda: [adminLogin(Admin)])
    logbtn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    print("ad login")


def adminWindow():
    adwin = tk.Tk()
    adwin.resizable(False, False)
    adwin.geometry("360x245")
    adwin.title("Train Ticket Reservation - Admin")

    trnbtn = tk.Button(adwin, text="Train", command=admin, height=3, width=16)
    passbtn = tk.Button(adwin, text="Passengers", command=passengerAdmin, height=3, width=16)

    trnbtn.grid(row=0, column=1)
    passbtn.grid(row=1, column=2)

    trnbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
    passbtn.place(relx=0.5, rely=0.7, anchor=S)


def ticket():
    ticketWin = tk.Tk()
    ticketWin.resizable(False, False)
    ticketWin.title("Train Ticket Reservation")
    ticketWin.geometry("300x245")

    trnavalbtn = tk.Button(ticketWin, text="Train Available", command=trainAvailable, height=3, width=16)
    tcktresbtn = tk.Button(ticketWin, text="Ticket Reservation", command=ticketReservation, height=3, width=16)
    tcktcnclbtn = tk.Button(ticketWin, text="Ticket Cancelation", command=ticketCancel, height=3, width=16)

    trnavalbtn.grid(row=0, column=1)
    tcktresbtn.grid(row=1, column=1)
    tcktcnclbtn.grid(row=2, column=1)

    trnavalbtn.place(relx=0.5, rely=0.05, anchor=N)
    tcktresbtn.place(relx=0.5, rely=0.37, anchor=N)
    tcktcnclbtn.place(relx=0.5, rely=0.70, anchor=N)


def adminSignup():
    def submit(na, Id):
        myCur.execute("insert into admin values (%s,%s)", (na, Id))
        myCon.commit()
        infoMessage('Alert', 'Seat added successfully')
        adminSignWin.destroy()

    adminSignWin = tk.Tk()
    adminSignWin.resizable(False, False)
    adminSignWin.geometry("360x220")
    adminSignWin.title("Train Ticket Reservation - Admin")

    name = Label(adminSignWin, text="Name:")
    name.grid(row=0, column=0, padx=10, pady=20)
    nme = Entry(adminSignWin, width=37)
    nme.grid(row=0, column=1, padx=10, pady=20, ipady=2.2)

    id = Label(adminSignWin, text='ID:')
    id.grid(row=1, column=0)
    idEnt = Entry(adminSignWin, width=37)
    idEnt.grid(row=1, column=1, padx=10, pady=20, ipady=2.21)

    Button(adminSignWin, text='submit', command=lambda: submit(nme.get(), idEnt.get())).grid(row=2, column=1, padx=10,
                                                                                             pady=10, ipadx=100)


def trainSearch():
    def searchh():
        print("im in")
        m = int(Num.get())
        print(m)
        myCur.execute("select * from trains where Number={}".format(m))
        k = myCur.fetchall()
        print(type(k),k[0][0],k[0][1],k[0][2],k[0][3])
        if k == []:
            messagebox.showwarning("No train","Train with number {} not found".format(k))
        else:
            messagebox.showinfo("{} Train found".format(len(k)),"Name: {}, Number:{}, from:{}, to:{}".format(k[0][0],k[0][1],k[0][2],k[0][3]))
    
    tk = Tk()
    Label(tk, text="Enter Train Number").grid(row=0, column=0)
    Num = Entry(tk)
    Num.grid(row=0, column=1)
    Button(tk, text="submit", command=searchh).grid(row=1, column=0)
    tk.mainloop()


root = tk.Tk()
root.resizable(False, False)

root.title("Train Ticket Reservation")
root.geometry("300x245")

adminbtn = tk.Button(root, text="Admin Login", command=adminLog, height=3, width=16)
tktresbtn = tk.Button(root, text="Passengers", command=ticket, height=3, width=16)
adminsign = tk.Button(root, text='Admin Signup', command=adminSignup, height=3, width=16)

myCon.commit()

adminbtn.place(relx=0.5, rely=0.05, anchor=N)
tktresbtn.place(relx=0.5, rely=0.37, anchor=N)
adminsign.place(relx=0.5, rely=0.70, anchor=N)

adminbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
tktresbtn.place(relx=0.5, rely=0.7, anchor=S)

root.mainloop()

myCon.close()

