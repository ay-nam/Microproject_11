from tkinter import *
from tkinter import messagebox
import mysql.connector

# Establish a connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="data"
)

cursor = db.cursor()

# Create a table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), phone VARCHAR(20), address VARCHAR(255))")

root = Tk()
root.geometry('800x600')
root.config(bg='#EBEBEB')
root.title('Contact Book')
root.resizable(0, 0)

contactlist = []

Name = StringVar()
Number = StringVar()
Address = StringVar()


frame = Frame(root)
frame.pack(side=RIGHT)

scroll = Scrollbar(frame, orient=VERTICAL)
select = Listbox(frame, yscrollcommand=scroll.set, font='Helvetica 16 ', fg='black',bg='white', width=20, height=10,borderwidth=3, relief="groove")
scroll.config(command=select.yview)
scroll.pack(side=RIGHT, fill=Y)
select.pack(side=LEFT, fill=BOTH, expand=1)


def Selected():
    if len(select.curselection()) == 0:
        messagebox.showerror("Error", "Please Select the Name")
    else:
        return int(select.curselection()[0])


def EntryReset():
    name_label_entry.delete(0, END)
    contact_label_entry.delete(0, END)
    address_label_entry.delete(0,END)


def AddContact():
    if Name.get() != "" and Number.get() != "" and Address.get() != "":
        query = "INSERT INTO contacts (name, phone, address) VALUES (%s, %s, %s)"
        values = (Name.get(), Number.get(), Address.get())

        cursor.execute(query, values)
        db.commit()

        Select_set()  
        EntryReset()
        messagebox.showinfo("Confirmation", "Successfully Add New Contact")
    else:
        messagebox.showerror("Error", "Please fill in all the information")


def UpdateDetail():
    selected_index = Selected()
    if selected_index is not None and Name.get() and Number.get() and Address.get():
        contact_id = contactlist[selected_index][0]  # Fixed index
        query = "UPDATE contacts SET name=%s, phone=%s, address=%s WHERE id=%s"
        values = (Name.get(), Number.get(), Address.get(), contact_id)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Confirmation", "Successfully Update Contact")
        EntryReset()
        Select_set()
    elif not (Name.get()) and not (Number.get()) and not (Address.get()) and not (len(select.curselection()) == 0):
        messagebox.showerror("Error", "Please fill in all the information")
    else:
        if len(select.curselection()) == 0:
            messagebox.showerror("Error", "Please Select the Name and \n press Load button")
        else:
            message1 = """To Load the all information of \n
                          selected row press Load button\n.
                          """
            messagebox.showerror("Error", message1)

def Delete_Entry():
    selected_index = Selected()
    if selected_index is not None:
        result = messagebox.askyesno('Confirmation', 'You Want to Delete Contact\n Which you selected')
        if result:
            contact_id = contactlist[selected_index][0]  # Fixed index
            cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
            db.commit()
            Select_set()
    else:
        messagebox.showerror("Error", 'Please select the Contact')


def VIEW():
    selected_index = Selected()
    if selected_index is not None:
        selected_id = contactlist[selected_index][0]  # Fixed index
        cursor.execute("SELECT name, phone,address FROM contacts WHERE id=%s", (selected_id,))
        result = cursor.fetchone()

        if result:
            NAME, PHONE,ADDRESS = result
            Name.set(NAME)
            Number.set(PHONE)
            Address.set(ADDRESS)


def EXIT():
    cursor.close()
    db.close()
    root.destroy()


def Select_set():
    cursor.execute("SELECT id, name FROM contacts ORDER BY name")
    result = cursor.fetchall()

    select.delete(0, END)
    contactlist.clear()

    for row in result:
        contact_id, name = row
        select.insert(END, name)
        contactlist.append([contact_id, name])  # Fixed order

Select_set()

name_label = Label(root, text='Name', font='Helvetica 18 bold', bg='#EBEBEB').place(x=50, y=20)
name_label_entry = Entry(root, textvariable=Name, width=30)
name_label_entry.place(x=200, y=20)

contact_label = Label(root, text='Contact No.', font='Helvetica 18 bold', bg='#EBEBEB').place(x=50, y=70)
contact_label_entry = Entry(root, textvariable=Number, width=30)
contact_label_entry.place(x=200, y=70)

address_label = Label(root, text='Address', font='Helvetica 18 bold', bg='#EBEBEB').place(x=50, y=120)
address_label_entry = Entry(root, textvariable=Address,width=30)
address_label_entry.place(x=200, y=120)

Button(root, text=" ADD", font='Helvetica 16 bold', fg='white',bg='#AA1111', command=AddContact, padx=20).place(x=50, y=190)
Button(root, text="EDIT", font='Helvetica 16 bold',  fg='white',bg='#AA1111', command=UpdateDetail, padx=20).place(x=50, y=250)
Button(root, text="DELETE", font='Helvetica 16 bold',  fg='white',bg='#AA1111', command=Delete_Entry, padx=20).place(x=50, y=310)
Button(root, text="VIEW", font='Helvetica 16 bold',  fg='white',bg='#AA1111', command=VIEW).place(x=50, y=370)
Button(root, text="RESET", font='Helvetica 16 bold',  fg='white',bg='#AA1111', command=EntryReset).place(x=50, y=430)
Button(root, text="EXIT", font='Helvetica 20 bold',bg='#AA1111', command=EXIT).place(x=250, y=500)

root.mainloop()    
