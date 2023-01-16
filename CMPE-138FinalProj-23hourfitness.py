import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from dateutil.relativedelta import relativedelta
from cryptography.fernet import Fernet

import sqlite3

conn = sqlite3.connect('235fitness.db')
conn.isolation_level = None
logintype = 0


showPack, showCust = False, False
container = ''


class CMPEGymApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        global container
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('235fitness ')
        self.configure(bg='white')
        self.geometry('850x625')
        l1 = tk.Label(self, text='Welcome to 23.5fitness Centers', font=(
            "Times New Roman", 28, "bold", 'italic'), bg='white').pack()
        container = tk.Frame(self, bg='white')
        container.pack(side="top", fill="both", expand=True, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # must add all class names in here when making a new class
        for F in (ini, Login, Menu, Menu2, Menu3, Addmember,  Showmember, SearchMember, NonMember, AddPayment, AddManager, ShowClass, AddEmployee, AddGym, SearchGym, AddClass, AddEquipment, ShowEquipment, AddFacilities, ShowFacilities):

            print(F)
            f = str(F)
            if f == "<class '__main__.Showmember'>":
                if showPack or showCust:
                    print('Inside ShowPack')
                    frame = F(container, self)
                    print(frame)
                    self.frames[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                else:
                    print('Outside ShowPack')
            else:
                frame = F(container, self)
                print(frame)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ini)

    def show_pack(self):
        print('Inside ShowPack')
        frame = Showmember(container, self)
        print(frame)
        self.frames[Showmember] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_cust(self):
        print('Inside ShowCust')
        frame = Showmember(container, self)
        print(frame)
        self.frames[Showmember] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        global showPack
        cont1 = str(cont)
        if cont1 == "<class '__main__.Showmember'>":
            showPack = True
            print(showPack)
            self.show_pack()
        elif cont1 == "<class '__main__.Showmember'>":
            showCust = True
            print(showCust)
            self.show_cust()
        frame = self.frames[cont]
        frame.tkraise()

def decrypt(pw):
    with open('key.txt', 'r') as f:
        key =f.read()
        f = Fernet(key)
        res = str(f.decrypt(bytes(pw, encoding='utf-8')).decode('utf-8'))
        
        return res

def encrypt(pw):
    with open('key.txt', 'r') as f:
        key =f.read()
        f = Fernet(key)

        return str(f.encrypt(bytes(pw, encoding='utf-8')).decode('utf-8'))

class Login(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        label = tk.Label(self, text='Sign In Here!', font=(
            "Helvetica", 30, 'italic'), bg='lavender').pack(pady=10, padx=10)
        username = tk.Label(self, text='ID', font=("Times", 24)).pack(pady=20)
        self.ev1 = tk.StringVar(value='Enter UserID')
        e1 = tk.Entry(self, width=50, textvariable=self.ev1,
                      font=("Times", 20)).pack()
        password = tk.Label(self, text='Password',
                            font=("Times", 24)).pack(pady=20)
        self.ev2 = tk.StringVar(value='Enter Password')
        e2 = tk.Entry(self, width=50, textvariable=self.ev2,
                      font=("Times", 20))
        e2.pack()
        e2.config(show="*")
        b1 = tk.Button(self, text='Login', relief='raised', font=(
            "Times", 18), width=10, command=self.authenticate).pack(pady=50)

    def authenticate(self):
        global conn
        global logintype

        flag = 0
        cur = conn.cursor()
        if (logintype == 1):  # case for admin/manager
            query = '''select e_id,ma_password from manager'''
            appendinst(query)

        elif(logintype == 2):  # case for employee
            query = '''select e_id,password from employee'''
            appendinst(query)

        elif(logintype == 3):  # case for member
            query = '''select m_id , password from member'''
            appendinst(query)

        cur.execute(query)
        r = cur.fetchall()
        for row in r:
            if int(self.ev1.get()) == int(row[0]) and self.ev2.get() == decrypt(row[1]):
                print("Login Successful!")
                messagebox.showinfo(
                    'Login Successful', 'Welcome to 23. Fitness Management System!')
                flag = 1
                conn.commit()
                cur.close()
                if (logintype == 1):  # case for admin/manager
                    return self.controller.show_frame(Menu)

                elif(logintype == 2):  # case for employee
                    return self.controller.show_frame(Menu2)

                elif(logintype == 3):  # case for member
                    return self.controller.show_frame(Menu3)

        if flag == 0:
            print('Login to System has Failed!')
            messagebox.askretrycancel(
                'Login Failed', 'Error Authenticating, Please Try Again!')
        conn.commit()
        cur.close()


class Menu(tk.Frame):  # admin menu

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='lavender')
        label = tk.Label(self, text='23.5 Fitness ADMIN Menu', font=(
            "Helvetica", 30, "italic"), bg='white').pack(pady=24, padx=10)
        b1 = tk.Button(self, text='Add Member', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(Addmember)).pack(pady=4)
        b2 = tk.Button(self, text='Add Gym', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddGym)).pack(pady=4)

        b3 = tk.Button(self, text='Show All 23.5 members', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(Showmember)).pack(pady=4)
        b4 = tk.Button(self, text='Show All Gyms', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(SearchGym)).pack(pady=4)
        b13 = tk.Button(self, text='Show Equipment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowEquipment)).pack(pady=4)

        # b6 = tk.Button(self, text='Add Membership Type', relief='raised', font=(
        #     "Times", 18), width=20, command=lambda: controller.show_frame(NonMember)).pack(pady=4)
        b7 = tk.Button(self, text='Add Payment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddPayment)).pack(pady=4)
        b8 = tk.Button(self, text='Add Manager', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddManager)).pack(pady=4)
        b9 = tk.Button(self, text='Add Employee', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddManager)).pack(pady=4)
        b11 = tk.Button(self, text='Add Classes', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddClass)).pack(pady=4)
        b12 = tk.Button(self, text='Add Equipment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddEquipment)).pack(pady=4)
        b13 = tk.Button(self, text='Add Facility', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddFacilities)).pack(pady=4)
        b10 = tk.Button(self, text='Show Employees', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(SearchEmployee)).pack(pady=4)
        b5 = tk.Button(self, text='Search 23.5 Member', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(SearchMember)).pack(pady=4)
        b14 = tk.Button(self, text='Back to Login Page ', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ini)).pack(pady=4)
        b15 = tk.Button(self, text='Show Facility', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowFacilities)).pack(pady=4)
        b16 = tk.Button(self, text='Free Trial', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(NonMember)).pack(pady=4)


class Menu2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='lavender')
        label = tk.Label(self, text='23.5 Fitness Employee Menu', font=(
            "Helvetica", 30, "italic"), bg='white').pack(pady=24, padx=10)
        b1 = tk.Button(self, text='Add Member', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(Addmember)).pack(pady=4)
        b3 = tk.Button(self, text='Show All 23.5 members', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(Showmember)).pack(pady=4)
        b4 = tk.Button(self, text='Show All Gyms', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(SearchGym)).pack(pady=4)
        b5 = tk.Button(self, text='Search 23.5 Member', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(SearchMember)).pack(pady=4)
        b8 = tk.Button(self, text='Show Equipment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowEquipment)).pack(pady=4)
        b6 = tk.Button(self, text='Change Membership Type', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddSubscription)).pack(pady=4)
        b7 = tk.Button(self, text='Change Member Payment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddPayment)).pack(pady=4)
        b8 = tk.Button(self, text='Show Equipment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowEquipment)).pack(pady=4)
        b9 = tk.Button(self, text='Show Facility', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowFacilities)).pack(pady=4)
        b10 = tk.Button(self, text='Back to Login Page ', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ini)).pack(pady=4)  # go to original login page
        b11 = tk.Button(self, text='Show Facility', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(NonMember)).pack(pady=4)


class Menu3(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='lavender')
        label = tk.Label(self, text='23.5 Fitness Member Menu', font=(
            "Helvetica", 30, "italic"), bg='white').pack(pady=24, padx=10)

        b1 = tk.Button(self, text='Add Membership Type', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(NonMember)).pack(pady=4)
        b2 = tk.Button(self, text='Add Payment', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(AddPayment)).pack(pady=4)
        b2 = tk.Button(self, text='Add Class', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ShowClass)).pack(pady=4)
        b3 = tk.Button(self, text='Back to Login Page ', relief='raised', font=(
            "Times", 18), width=20, command=lambda: controller.show_frame(ini)).pack(pady=4)  # way to go back to first page


class Addmember(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add member', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.memberID = tk.StringVar(value='Enter member ID')
        memberID = tk.Entry(self, width=50, textvariable=self.memberID, font=(
            "Times", 20)).pack(pady=12)

        self.typeVar = tk.StringVar(value='Enter member Type')
        type = tk.Entry(self, width=50, textvariable=self.typeVar,
                        font=("Times", 20)).pack(pady=12)

        self.name = tk.StringVar(value='Enter member name')
        name = tk.Entry(self, width=50, textvariable=self.name,
                        font=("Times", 20)).pack(pady=12)

        self.stdate = tk.StringVar(value='Enter start date')
        strt = tk.Entry(self, width=50, textvariable=self.stdate,
                        font=("Times", 20)).pack(pady=12)

        self.endate = tk.StringVar(value='Enter end date')
        en = tk.Entry(self, width=50, textvariable=self.endate,
                      font=("Times", 20)).pack(pady=12)

        self.payVar = tk.StringVar(value='Enter payment method')
        pay = tk.Entry(self, width=50, textvariable=self.payVar,
                       font=("Times", 20)).pack(pady=12)

        self.emailvar = tk.StringVar(value='Enter e-mail')
        ema = tk.Entry(self, width=50, textvariable=self.emailvar,
                       font=("Times", 20)).pack(pady=12)

        self.phoneVar = tk.StringVar(value='Enter phone number')
        phone = tk.Entry(self, width=50, textvariable=self.phoneVar,
                         font=("Times", 20)).pack(pady=12)

        self.passvar = tk.StringVar(value='Enter password')
        pw = tk.Entry(self, width=50, textvariable=self.passvar,
                      font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addmember).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)
        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addmember(self):
        global conn
        cur = conn.cursor()
        if (not self.memberID.get().isdigit()):
            return messagebox.showwarning('Add member', 'Please enter valid member ID!')
        elif (self.passvar.get() == ""):
            return messagebox.showwarning('Add member', 'Please enter valid password!')

        else:
            rec = (int(self.memberID.get()), self.typeVar.get(), self.name.get(), self.stdate.get(), self.endate.get(
            ), int(self.payVar.get()), self.emailvar.get(), self.phoneVar.get(), encrypt(self.passvar.get()), "")
            q1 = '''select m_id from member'''
            appendinst(q1)
            cur.execute(q1)
            r = cur.fetchall()
            for row in r:
                if row[0] == int(self.memberID.get()):
                    return messagebox.showwarning('Add member', 'member ID already exists!')
            query = '''insert into member values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            appendinst(query)
            cur.execute(query, rec)
            self.text.set("New member Added!!")
            conn.commit()
            cur.close()


class Showmember(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        label = tk.Label(self, text='List of Members', font=(
            "Helvetica", 20, 'italic'), bg='white').pack(padx=10)

        list1 = tk.Listbox(self, height=8, width=160, selectmode='multiple', font=(
            "Times", 28), bd=6, relief='raised', bg='white', fg='#2C3335')
        list1.pack(padx=25, pady=16)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack()
        b3 = tk.Button(self, text='Delete', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.deletemember(list1)).pack(pady=8)
        self.view_command(list1)

    def __str__(self):
        return 'ShowMember'

    def showMember(self):
        global conn
        conn = sqlite3.connect('235fitness.db')
        cur = conn.cursor()
        query = '''select * from member'''
        cur.execute(query)
        r = cur.fetchall()
        print(r)
        conn.commit()
        cur.close()
        count = len(r)
        if count > 0:
            return r
        else:
            messagebox.showinfo("List of Members", "No members records found.")

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.showMember():
            list1.insert(tk.END, row)

    def deletemember(self, list1):
        sel = list1.curselection()
        cur = conn.cursor()
        q1 = '''select * from member'''
        cur.execute(q1)
        r = cur.fetchall()
        query = '''delete from member where m_ID = ?'''
        if len(sel) == 0:
            return messagebox.showwarning('Delete Member', 'No member is selected!')
        for i in range(len(sel)):
            cur.execute(query, (r[sel[i]][0],))
        conn.commit()
        cur.close()
        for index in sel[::-1]:
            list1.delete(index)


class SearchMember(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text='Search Member by Name', font=(
            "Helvetica", 30, "italic"), bg='white').pack(padx=10)
        self.custName = tk.StringVar(value='Enter member Name')
        memberName = tk.Entry(
            self, width=50, textvariable=self.custName, font=("Times", 20)).pack(pady=12)
        list1 = tk.Listbox(self, height=5, width=160, font=(
            "Times", 28), bd=6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b1 = tk.Button(self, text='Search', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.view_command(list1)).pack(pady=10)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=10)

    def searchMember(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from member where m_name = ?'''
        cur.execute(q1, (self.custName.get(),))
        r1 = cur.fetchall()
        if len(r1) == 0:
            return messagebox.showinfo("Search Member", "member not found!")
        elif len(r1) != 0:
            q2 = '''select * from member where m_name = ? AND m_type = 'member' '''
            cur.execute(q2, (self.custName.get(),))
            r2 = cur.fetchall()
            if len(r2) == 0:
                return messagebox.showinfo("Search Member,  Person found but is not a member!")
            else:
                messagebox.showinfo("Search member", "Member Found!")
                conn.commit()
                cur.close()
                return r2

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.searchMember():
            list1.insert(tk.END, row)


class NonMember(tk.Frame):  # fix

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        months = ['01 Month', '03 Months',
                  '06 Months', '12 Months', '24 Months']
        label = tk.Label(self, text='free Trial', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10, pady=15)
        self.nonMemID = tk.StringVar(value='Enter Non Memebr ID')
        subscriptionID = tk.Entry(
            self, width=50, textvariable=self.nonMemID, font=("Times", 20)).pack(pady=12)
        self.custName = tk.StringVar(value='Enter Non Member Name')
        memberName = tk.Entry(
            self, width=50, textvariable=self.custName, font=("Times", 20)).pack(pady=12)
        self.packID = tk.StringVar(value='Enter m_type')
        memberID = tk.Entry(self, width=50, textvariable=self.packID, font=(
            "Times", 20)).pack(pady=12)
        self.monthVar = tk.StringVar(value='Select No. of Months')
        month = ttk.Combobox(self, width=49, textvariable=self.monthVar, font=(
            "Times", 20), values=months).pack(pady=18)
        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.nonMember).pack(pady=8)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=8)
        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def nonMember(self):
        global conn
        cur = conn.cursor()
        # q1 = '''select * from member where m_name = ?'''
        # cur.execute(q1, (self.custName.get(),))
        # r1 = cur.fetchall()
        q2 = '''select * from member where m_id = ?'''

        if not self.nonMemID.get().isdigit():
            return messagebox.showwarning('Free Trial', 'Please enter valid non member ID!')
        # elif len(r1) == 0:
        #     return messagebox.showwarning('Free Trial', 'Non Member Not Found!')
        elif self.packID.get().isdigit():
            return messagebox.showwarning('Free Trial', 'Please enter valid member type!')
        elif self.monthVar.get() == 'Select No. of Months':
            return messagebox.showwarning('Free Trial', 'Please select an option from dropdown menu!')
        else:
            cur.execute(q2, (int(self.nonMemID.get()),))
            r2 = cur.fetchall()
            q1 = '''select m_id from member'''
            cur.execute(q1)
            r = cur.fetchall()
            for row in r:
                if row[0] == int(self.nonMemID.get()):
                    return messagebox.showwarning('Free Trial', 'Non Memebr ID already exists!')
            # if len(r2) == 0:
            #     return messagebox.showwarning('Free Trial', 'Non Member Not Found!')
            rec = (int(self.nonMemID.get()), self.packID.get(),
                   self.custName.get(), date.today(), date.today() + relativedelta(months=+(int(self.monthVar.get()[0:2]))))
            query = '''insert into member values(?, ?, ?, ?, ?, null, null, null, null, null)'''
            cur.execute(query, rec)
            self.text.set("Guest user Added!!")
            conn.commit()
            cur.close()


class AddPayment(tk.Frame):
    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add Payment', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10, pady=15)
        self.payID = tk.StringVar(value='Enter Payment ID')
        paymentID = tk.Entry(
            self, width=50, textvariable=self.payID, font=("Times", 20)).pack(pady=12)
        self.custID = tk.StringVar(value='Enter member ID')
        memberName = tk.Entry(
            self, width=50, textvariable=self.custID, font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addPayment).pack(pady=10)

        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=10)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=4, padx=16)

    def addPayment(self):
        global conn
        global logintype
        cur = conn.cursor()
        q = '''select payment from member where m_id = ?'''
        cur.execute(q, (self.custID.get(),))
        r = cur.fetchall()
        if (len(r) == 0):
            return messagebox.showwarning('Add Payment', 'memberID not found...')
        else:
            for row in r:
                if(not self.payID.get().isdigit()):
                    return messagebox.showwarning('Add Payment', 'Please enter valid payment method!')
                else:
                    if (int(self.payID.get()) == int(row[0])):
                        return messagebox.showwarning('Add Payment', 'Payment method already exists!')
                    else:
                        q1 = ''' UPDATE member SET payment = ? WHERE m_id = ?'''
                        cur.execute(q1, (self.payID.get(), self.custID.get(),))
                        self.text.set("Payment updated!")
                        conn.commit()
                        cur.close()


class AddManager(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='lavender')
        label = tk.Label(self, text='Add 23.5 Gym Manager', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        self.emID = tk.StringVar(value='Enter Employee ID')
        memberID = tk.Entry(self, width=50, textvariable=self.emID, font=(
            "Times", 20)).pack(pady=12)

        self.gymid = tk.StringVar(value='Enter GymID')
        gID = tk.Entry(self, width=50, textvariable=self.gymid,
                       font=("Times", 20)).pack(pady=12)

        self.pw = tk.StringVar(value='Enter New manager password')
        pwd = tk.Entry(self, width=50, textvariable=self.pw,
                       font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addmanager).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)
        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addmanager(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from employee where e_id = ?'''
        cur.execute(q1, (self.emID.get(),))
        r1 = cur.fetchall()

        qc = '''select e_id from manager'''
        cur.execute(qc,)
        rc = cur.fetchall()
        for row in rc:
            if(int(self.emID.get()) == row[0]):
                return messagebox.showwarning('Add Manager', 'Employee is already a manager')

        if not self.gymid.get().isdigit():
            return messagebox.showwarning('Add Manager', 'Please enter valid gym ID!')
        elif not self.emID.get().isdigit():
            return messagebox.showwarning('Add Manager', 'Please enter valid Employee ID')
        else:

            q2 = '''select ssn,gym_id from employee where e_id = ?'''
            cur.execute(q2, (self.emID.get(),))
            r2 = cur.fetchall()

            for row in r2:
                cur.execute("begin")
                try:
                    q3 = '''UPDATE gym SET mgr_ssn = ? where gym_id = ?'''
                    appendinst(q3)
                    cur.execute(q3, (row[0], row[1],))
                    self.text.set("Manager updated!")

                    q4 = '''insert into manager values(?, ?, ?)'''
                    appendinst(q4)
                    cur.execute(q4, (row[0], encrypt(self.pw.get()), self.emID.get(),))
                    self.text.set("Position updated!")
                    cur.execute("commit")
                except cur.Error:
                    print("failed!")
                    cur.execute("rollback") 
            cur.close()


class ini(tk.Frame):
    def __init__(self, parent, controller):
        openfile()
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='pink')
        b1 = tk.Button(self, text='Admin Login', relief='raised', font=(
            "Times", 18), width=10, command=lambda: [openfile(), logtype(1), controller.show_frame(Login)]).pack(pady=12)
        b2 = tk.Button(self, text='Employee Login', relief='raised', font=(
            "Times", 18), width=10, command=lambda: [openfile(), logtype(2), controller.show_frame(Login)]).pack(pady=12)
        b3 = tk.Button(self, text='Member Login', relief='raised', font=(
            "Times", 18), width=10, command=lambda: [openfile(), logtype(3), controller.show_frame(Login)]).pack(pady=12)


def logtype(typevar):
    global logintype
    logintype = typevar


class ShowClass(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        label = tk.Label(self, text='List of classes', font=(
            "Helvetica", 20, 'italic'), bg='white').pack(padx=10)

        self.custID = tk.StringVar(value='Enter member ID')
        memberName = tk.Entry(
            self, width=50, textvariable=self.custID, font=("Times", 20)).pack(pady=12)

        list1 = tk.Listbox(self, height=8, width=160, selectmode='multiple', font=(
            "Times", 28), bd=6, relief='raised', bg='white', fg='#2C3335')
        list1.pack(padx=25, pady=16)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack()
        b3 = tk.Button(self, text='Add Class', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.addClass(list1)).pack(pady=8)
        self.view_command(list1)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=4, padx=16)

    def __str__(self):
        return 'Showclass'

    def Showclass(self):
        global conn
        conn = sqlite3.connect('235fitness.db')
        cur = conn.cursor()
        query = '''select * from class'''
        cur.execute(query)
        r = cur.fetchall()
        print(r)
        conn.commit()
        cur.close()
        count = len(r)
        if count > 0:
            return r
        else:
            messagebox.showinfo("List of classes", "No classes found.")

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.Showclass():
            list1.insert(tk.END, row)

    def addClass(self, list1):
        sel = list1.curselection()
        cur = conn.cursor()
        q1 = '''select * from class'''
        appendinst(q1)
        cur.execute(q1)
        r = cur.fetchall()
        for row in r:
            print(row[3])
            q2 = ''' UPDATE member SET trainer_ssn = ? WHERE m_id = ?'''
            appendinst(q2)
            cur.execute(q2, (str(row[3]), self.custID.get(),))
            self.text.set("Trainer updated!")
            conn.commit()
            cur.close()


class AddEmployee(tk.Frame):  # fix should be able to update receptionist, manager, and trainer
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add class', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.clID = tk.StringVar(value='Enter class ID')
        classID = tk.Entry(self, width=50, textvariable=self.clID,
                           font=("Times", 20)).pack(pady=12)

        self.typeVar = tk.StringVar(value='Enter class Type')
        type = tk.Entry(self, width=50, textvariable=self.typeVar,
                        font=("Times", 20)).pack(pady=12)

        self.gymID = tk.StringVar(value='Enter Gym ID')
        gym = tk.Entry(self, width=50, textvariable=self.gymID,
                       font=("Times", 20)).pack(pady=12)

        self.trID = tk.StringVar(value='Enter ID of trainer')
        trainer = tk.Entry(self, width=50, textvariable=self.trID,
                           font=("Times", 20)).pack(pady=12)

        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)


# fix Should be able to also tell if person is a manager maybe when results found say they are a manager and the gym_ID they are the manager for
class SearchEmployee(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add class', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.clID = tk.StringVar(value='Enter class ID')
        classID = tk.Entry(self, width=50, textvariable=self.clID,
                           font=("Times", 20)).pack(pady=12)

        self.typeVar = tk.StringVar(value='Enter class Type')
        type = tk.Entry(self, width=50, textvariable=self.typeVar,
                        font=("Times", 20)).pack(pady=12)

        self.gymID = tk.StringVar(value='Enter Gym ID')
        gym = tk.Entry(self, width=50, textvariable=self.gymID,
                       font=("Times", 20)).pack(pady=12)

        self.trID = tk.StringVar(value='Enter ID of trainer')
        trainer = tk.Entry(self, width=50, textvariable=self.trID,
                           font=("Times", 20)).pack(pady=12)

        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)


class AddGym(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add Gym', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.gID = tk.StringVar(value='Enter Gym ID')
        gymID = tk.Entry(self, width=50, textvariable=self.gID,
                         font=("Times", 20)).pack(pady=12)

        self.addy = tk.StringVar(value='Enter address')
        address = tk.Entry(self, width=50, textvariable=self.addy,
                           font=("Times", 20)).pack(pady=12)

        self.phnum = tk.StringVar(value='Enter phone number')
        phonenumber = tk.Entry(
            self, width=50, textvariable=self.phnum, font=("Times", 20)).pack(pady=12)

        self.mID = tk.StringVar(value='Enter ID of manager')
        manage = tk.Entry(self, width=50, textvariable=self.mID,
                          font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addgym).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addgym(self):
        global conn
        cur = conn.cursor()
        if (not self.gID.get().isdigit()):
            return messagebox.showwarning('Add gym', 'Please enter valid Gym ID!')

        else:
            mssn = 0
            q1 = '''select gym_id from gym'''
            appendinst(q1)
            cur.execute(q1)
            r = cur.fetchall()

            q2 = '''select m_ssn,e.e_id from manager as m join employee as e on m.m_ssn = e.ssn'''
            appendinst(q2)
            cur.execute(q2)
            r2 = cur.fetchall()
            for row in r2:
                if (int(self.mID.get()) == row[1]):
                    mssn = row[0]
                    query2 = '''UPDATE gym SET mgr_ssn = ? WHERE gym_id = ?'''
                    appendinst(query2)
                    cur.execute(query2, (row[0], self.gID.get(),))
                    conn.commit()

            rec = (int(self.gID.get()), self.addy.get(), self.phnum.get(), mssn)

            for row in r:
                if row[0] == int(self.gID.get()):
                    return messagebox.showwarning('Add gym', 'gym ID already exists!')
            query = '''insert into gym values(?, ?, ?, ?)'''
            appendinst(query)
            cur.execute(query, rec)
            conn.commit()

            query3 = '''UPDATE employee SET gym_id = ? WHERE e_id = ?'''
            appendinst(query3)
            cur.execute(query3, (self.gID.get(), self.mID.get(),))
            conn.commit()

            self.text.set("New gym Added!!")
            conn.commit()
            cur.close()


class SearchGym(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        label = tk.Label(self, text='List of Gym locations', font=(
            "Helvetica", 20, 'italic'), bg='white').pack(padx=10)

        list1 = tk.Listbox(self, height=8, width=160, selectmode='multiple', font=(
            "Times", 28), bd=6, relief='raised', bg='white', fg='#2C3335')
        list1.pack(padx=25, pady=16)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack()
        b3 = tk.Button(self, text='Delete', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.deletegym(list1)).pack(pady=8)
        self.view_command(list1)

    def __str__(self):
        return 'Showgym'

    def showgym(self):
        global conn
        conn = sqlite3.connect('235fitness.db')
        cur = conn.cursor()
        query = '''select * from gym'''
        appendinst(query)
        cur.execute(query)
        r = cur.fetchall()
        print(r)
        conn.commit()
        cur.close()
        count = len(r)
        if count > 0:
            return r
        else:
            messagebox.showinfo("List of Gyms", "No Gyms records found.")

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.showgym():
            list1.insert(tk.END, row)

    def deletegym(self, list1):
        sel = list1.curselection()
        cur = conn.cursor()
        q1 = '''select * from gym'''
        cur.execute(q1)
        r = cur.fetchall()
        query = '''delete from gym where gym_id = ?'''
        appendinst(query)
        if len(sel) == 0:
            return messagebox.showwarning('Delete gym', 'No gym location is selected!')
        for i in range(len(sel)):
            cur.execute(query, (r[sel[i]][0],))
        conn.commit()
        cur.close()
        for index in sel[::-1]:
            list1.delete(index)


class AddClass(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add class', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.clID = tk.StringVar(value='Enter class ID')
        classID = tk.Entry(self, width=50, textvariable=self.clID,
                           font=("Times", 20)).pack(pady=12)

        self.typeVar = tk.StringVar(value='Enter class Type')
        type = tk.Entry(self, width=50, textvariable=self.typeVar,
                        font=("Times", 20)).pack(pady=12)

        self.gymID = tk.StringVar(value='Enter Gym ID')
        gym = tk.Entry(self, width=50, textvariable=self.gymID,
                       font=("Times", 20)).pack(pady=12)

        self.trID = tk.StringVar(value='Enter ID of trainer')
        trainer = tk.Entry(self, width=50, textvariable=self.trID,
                           font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addclass).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addclass(self):
        global conn
        cur = conn.cursor()
        if (not self.clID.get().isdigit()):
            return messagebox.showwarning('Add class', 'Please enter valid class ID!')

        else:
            trainerssn = 0
            q1 = '''select cl_id from class'''
            appendinst(q1)
            cur.execute(q1)
            r = cur.fetchall()

            q2 = '''select t_ssn,e_id from trainer as t join employee as e on t.t_ssn = e.ssn'''
            appendinst(q2)
            cur.execute(q2)
            r2 = cur.fetchall()
            for row in r2:
                if (int(self.trID.get()) == row[1]):
                    trainerssn = row[0]
                else:
                    return messagebox.showwarning('Add class', 'employee ID is invalid!')

            rec = (int(self.clID.get()), self.typeVar.get(),
                   self.gymID.get(), 0, trainerssn)

            for row in r:
                if row[0] == int(self.clID.get()):
                    return messagebox.showwarning('Add class', 'class ID already exists!')
            query = '''insert into class values(?, ?, ?, ?, ?)'''
            appendinst(query)
            cur.execute(query, rec)
            self.text.set("New class Added!!")
            conn.commit()
            cur.close()

# class AddFacilities(tk.Frame):
# class showFacilities(tk.Frame):


class AddFacilities(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add Facility', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.gID = tk.StringVar(value='Enter Gym ID')
        gymID = tk.Entry(self, width=50, textvariable=self.gID,
                         font=("Times", 20)).pack(pady=12)

        self.fcn = tk.StringVar(value='Enter Facility name')
        fc_n = tk.Entry(self, width=50, textvariable=self.fcn,
                        font=("Times", 20)).pack(pady=12)

        self.fcid = tk.StringVar(value='Enter Facility ID')
        fc_id = tk.Entry(self, width=50, textvariable=self.fcid,
                         font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addfc).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addfc(self):
        global conn
        cur = conn.cursor()
        if (not self.gID.get().isdigit()):
            return messagebox.showwarning('Add gym', 'Please enter valid Gym ID!')

        else:
            q1 = '''select gym_id from gym'''
            appendinst(q1)
            cur.execute(q1)
            r = cur.fetchall()
            check = 0

            for i in range(len(r)):
                for row in r:
                    try:
                        if (int(self.gID.get()) == row[i]):
                            rec = (int(self.fcid.get()),
                                   self.fcn.get(), int(self.gID.get()))
                            check = 1
                    except IndexError:
                        pass

            if (not check):
                return messagebox.showwarning('Add Facility', 'GymID is invalid!')

            q2 = '''select fc_id from Facility'''
            appendinst(q2)
            cur.execute(q2)
            r2 = cur.fetchall()
            for row in r2:
                if row[0] == int(self.fcid.get()):
                    return messagebox.showwarning('Add Facility', 'Facility ID already exists!')
            query = '''insert into Facility values(?, ?, ?)'''
            appendinst(query)
            cur.execute(query, rec)
            self.text.set("New Facility Added!!")
            conn.commit()
            cur.close()


class ShowFacilities(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')

        label = tk.Label(self, text='Search Facility by Gym', font=(
            "Helvetica", 30, "italic"), bg='white').pack(padx=10)
        self.gid = tk.StringVar(value='Enter Gym ID')
        g_id = tk.Entry(self, width=50, textvariable=self.gid,
                        font=("Times", 20)).pack(pady=12)
        list1 = tk.Listbox(self, height=5, width=160, font=(
            "Times", 28), bd=6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b1 = tk.Button(self, text='Search', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.view_command(list1)).pack(pady=10)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=10)
        b3 = tk.Button(self, text='Delete', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.deletefacility(list1)).pack(pady=10)

    def searchFacility(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from gym where gym_id = ?'''
        appendinst(q1)
        cur.execute(q1, (self.gid.get(),))
        r1 = cur.fetchall()
        if len(r1) == 0:
            return messagebox.showinfo("Search Facility", "Gym not found!")
        elif len(r1) != 0:
            q2 = '''select * from Facility where gym_id = ? '''
            appendinst(q2)
            cur.execute(q2, (self.gid.get(),))
            r2 = cur.fetchall()

            messagebox.showinfo("Search Facility", "Facility Found!")
            conn.commit()
            cur.close()
            return r2

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.searchFacility():
            list1.insert(tk.END, row)

    def deletefacilities(self, list1):
        sel = list1.curselection()
        cur = conn.cursor()
        q1 = '''select * from Facility'''
        appendinst(q1)
        cur.execute(q1)
        r = cur.fetchall()
        query = '''delete from Facility where fc_id = ?'''
        appendinst(query)
        if len(sel) == 0:
            return messagebox.showwarning('Delete Facility', 'No facility has been selected!')
        for i in range(len(sel)):
            cur.execute(query, (r[sel[i]][0],))
        conn.commit()
        cur.close()
        for index in sel[::-1]:
            list1.delete(index)


class AddEquipment(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        label = tk.Label(self, text='Add Equipment', font=(
            "Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)

        self.gID = tk.StringVar(value='Enter Gym ID')
        gymID = tk.Entry(self, width=50, textvariable=self.gID,
                         font=("Times", 20)).pack(pady=12)

        self.eqn = tk.StringVar(value='Enter Equipment name')
        eq_n = tk.Entry(self, width=50, textvariable=self.eqn,
                        font=("Times", 20)).pack(pady=12)

        self.eqid = tk.StringVar(value='Enter Equipment ID')
        eq_id = tk.Entry(self, width=50, textvariable=self.eqid,
                         font=("Times", 20)).pack(pady=12)

        b1 = tk.Button(self, text='Submit', relief='raised', font=(
            "Times", 18), width=10, command=self.addeq).pack(pady=12)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=12)

        self.text = tk.StringVar(value='')
        success = tk.Label(self, text='', font=("Helvetica", 10, "italic"),
                           bg='#4834DF', textvariable=self.text).pack(pady=6, padx=10)

    def addeq(self):
        global conn
        cur = conn.cursor()
        if (not self.gID.get().isdigit()):
            return messagebox.showwarning('Add gym', 'Please enter valid Gym ID!')

        else:
            q1 = '''select gym_id from gym'''
            appendinst(q1)
            cur.execute(q1)
            r = cur.fetchall()
            check = 0

            for i in range(len(r)):
                for row in r:
                    try:
                        if (int(self.gID.get()) == row[i]):
                            rec = (int(self.eqid.get()),
                                   self.eqn.get(), int(self.gID.get()))
                            check = 1
                    except IndexError:
                        pass

            if (not check):
                return messagebox.showwarning('Add Equipment', 'GymID is invalid!')

            q2 = '''select eq_id from equipment'''
            appendinst(q2)
            cur.execute(q2)
            r2 = cur.fetchall()
            for row in r2:
                if row[0] == int(self.eqid.get()):
                    return messagebox.showwarning('Add Equipment', 'equipment ID already exists!')
            query = '''insert into equipment values(?, ?, ?)'''
            appendinst(query)
            cur.execute(query, rec)
            self.text.set("New Equipment Added!!")
            conn.commit()
            cur.close()


class ShowEquipment(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')

        label = tk.Label(self, text='Search Equipment by Gym', font=(
            "Helvetica", 30, "italic"), bg='white').pack(padx=10)
        self.gid = tk.StringVar(value='Enter Gym ID')
        g_id = tk.Entry(self, width=50, textvariable=self.gid,
                        font=("Times", 20)).pack(pady=12)
        list1 = tk.Listbox(self, height=5, width=160, font=(
            "Times", 28), bd=6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b1 = tk.Button(self, text='Search', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.view_command(list1)).pack(pady=10)
        b2 = tk.Button(self, text='Menu', relief='raised', font=(
            "Times", 18), width=10, command=lambda: changemenu(self)).pack(pady=10)
        b3 = tk.Button(self, text='Delete', relief='raised', font=(
            "Times", 18), width=10, command=lambda: self.deleteequipment(list1)).pack(pady=10)

    def searchEquipment(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from gym where gym_id = ?'''
        appendinst(q1)
        cur.execute(q1, (self.gid.get(),))
        r1 = cur.fetchall()
        if len(r1) == 0:
            return messagebox.showinfo("Search Equipment", "Gym not found!")
        elif len(r1) != 0:
            q2 = '''select * from equipment where gym_id = ? '''
            appendinst(q2)
            cur.execute(q2, (self.gid.get(),))
            r2 = cur.fetchall()

            messagebox.showinfo("Search Equipment", "Equipment Found!")
            conn.commit()
            cur.close()
            return r2

    def view_command(self, list1):
        list1.delete(0, tk.END)
        for row in self.searchEquipment():
            list1.insert(tk.END, row)

    def deleteequipment(self, list1):
        sel = list1.curselection()
        cur = conn.cursor()
        q1 = '''select * from equipment'''
        appendinst(q1)
        cur.execute(q1)
        r = cur.fetchall()
        query = '''delete from equipment where eq_id = ?'''
        appendinst(query)
        if len(sel) == 0:
            return messagebox.showwarning('Delete equipment', 'No equipment has been selected!')
        for i in range(len(sel)):
            print(r[i][0])
            cur.execute(query, (r[sel[i]][0],))
        conn.commit()
        cur.close()
        for index in sel[::-1]:
            list1.delete(index)


def changemenu(self):

    global logintype

    if (logintype == 1):  # case for admin/manager
        return self.controller.show_frame(Menu)

    elif(logintype == 2):  # case for employee
        return self.controller.show_frame(Menu2)

    elif(logintype == 3):  # case for member
        return self.controller.show_frame(Menu3)


def openfile():
    with open('output.txt', 'w') as f:
        f.write('CMPE-138 Fall 2022 Final Project \n')


def appendinst(L):
    file1 = open("output.txt", "a")
    file1.writelines(L+"\n")
    file1.close()


app = CMPEGymApplication()
app.mainloop()
conn.close()