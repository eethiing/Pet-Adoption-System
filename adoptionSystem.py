### CURRENT ONE 
import tkinter as tk
import xml.etree.ElementTree as ET
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox, ttk

# XML file data
pet_xml = "pet.xml"
adopter_contacts_xml = 'adopter_contacts.xml'

def parse_pets_xml():
    tree = ET.parse(pet_xml)
    return tree, tree.getroot()

def check_entries(entries):
    return all(entry.get().strip() for entry in entries)

tree, pets = parse_pets_xml()
current_pet_index = 0
### ADOPTER'S CONTENTS

# add_contact function for user 
def add_contact():
    contact_tree = ET.parse(adopter_contacts_xml)
    contact_root = contact_tree.getroot()  
    a_name = adopter_name_input.get()
    a_email = adopter_email_input.get()
    a_num = adopter_number_input.get()

    if not check_entries([adopter_name_input,adopter_email_input, adopter_number_input]):
        messagebox.showwarning('Incomplete Form', "Please ensure that all fields are complete before submitting.")
        return
    else:
        # double confirm 
        confirm = messagebox.askyesno("Confirm Details", f"Are these details correct?\n\nName: {a_name}\nEmail: {a_email}\nContact No.: {a_num}")

        if confirm :
            # save details
            sub_element = ET.SubElement(contact_root, 'adopter')
            id_data = ET.SubElement(sub_element, 'id')
            id_data.text = str(current_pet_index+1)
            contact_details = ET.SubElement(sub_element, 'contact')
            adop_name = ET.SubElement(contact_details, 'name')
            adop_name.text = a_name
            adop_num = ET.SubElement(contact_details, 'contact_num')
            adop_num.text = a_num
            adop_email = ET.SubElement(contact_details, 'email')
            adop_email.text = a_email

            contact_tree.write(adopter_contacts_xml, encoding="utf-8")
            messagebox.showinfo("Details Saved", "Your details have been saved.")
            win_contact.destroy()
        else:
            messagebox.showinfo("Details Not Saved", "Please review your details and try again.")

# GUI for user to add contacts
def adopter_contacts_gui() :
    global win_contact, adopter_number_input, adopter_email_input, adopter_name_input
    win_contact = tk.Tk()
    win_contact.title('Contact Details')

    adopter_name = tk.Label(win_contact, text='Name : ')
    adopter_name_input = tk.Entry(win_contact)
    adopter_email = tk.Label(win_contact, text='Email : ')
    adopter_email_input = tk.Entry(win_contact)
    adopter_number = tk.Label(win_contact, text='Contact No. : ')
    adopter_number_input = tk.Entry(win_contact)

    adopter_name.pack()
    adopter_name_input.pack()
    adopter_email.pack()
    adopter_email_input.pack()
    adopter_number.pack()
    adopter_number_input.pack()
    btn_save_contact = tk.Button(win_contact, text='Done', command=add_contact).pack()

# show the pet image 
def display_image(image_path):
    img = Image.open(image_path)
    img = img.resize((200,200))
    return ImageTk.PhotoImage(img)

# obtain the pet data to be displayed 
def get_pet_data(pet_index):
    pet = pets[pet_index]
    id_var.set(f"ID: {pet.find('id').text}")
    name_var.set(f"Name: {pet.find('name').text}")
    type_var.set(f"Type: {pet.find('type').text}")
    age_var.set(f"Age: {pet.find('age').text}")
    gender_var.set(f"Gender: {pet.find('gender').text}")
    desc_var.set(f"Description: {pet.find('description').text}")
    
    img_pet_path = pet.find('image').text
    if img_pet_path is not None:
        pet_img = display_image(img_pet_path)
        img_label.config(image=pet_img)
        img_label.image = pet_img

# function to increase the pet index when next button is clicked
def next_pet():
    global current_pet_index
    current_pet_index += 1
    if current_pet_index >= len(pets):
        current_pet_index = 0
    get_pet_data(current_pet_index)

# main GUI for user 
def load_pets():
    global id_var, name_var, type_var,  age_var, gender_var, root, desc_var, img_label, win
    # destroy the previous window 
    root.destroy()
    win = tk.Tk()
    win.title("Pet Adoption System")

    id_var = tk.StringVar()
    name_var = tk.StringVar()
    type_var = tk.StringVar()
    age_var = tk.StringVar()
    gender_var = tk.StringVar()
    desc_var = tk.StringVar()

    img_label = tk.Label(win)
    id_label = tk.Label(win, textvariable=id_var)
    name_label = tk.Label(win, textvariable=name_var)
    type_label = tk.Label(win, textvariable=type_var)
    age_label = tk.Label(win, textvariable=age_var)
    gender_label = tk.Label(win, textvariable=gender_var)
    desc_label = tk.Label(win, textvariable=desc_var)

    img_label.pack(pady=10)
    id_label.pack(pady=5)
    name_label.pack(pady=5)
    type_label.pack(pady=5)
    age_label.pack(pady=5)
    gender_label.pack(pady=5)
    desc_label.pack(pady=5)

    next_button = tk.Button(win, text="Next", command=next_pet)
    next_button.pack(pady=10)

    contact_button = tk.Button(win, text="Contact", command=adopter_contacts_gui)
    contact_button.pack(pady=10)

    get_pet_data(0)

    win.mainloop()

####################################### RESCUER'S CONTENT ########################################

# see all the pets details
def view_pets():
    root.destroy()
    contact_tree = ET.parse(adopter_contacts_xml)
    contact_root = contact_tree.getroot() 

    global win_view, table

    win_view = tk.Tk()
    win_view.title('Pet Details')

    # create a table 
    table = ttk.Treeview(win_view, columns=("ID", "Name", "Type", "Age", "Gender","Description","Contacts"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Type", text="Type")
    table.heading("Age", text="Age")
    table.heading("Gender", text="Gender")
    table.heading("Description", text="Description")
    table.heading("Contacts", text="Contacts")
    table.pack()        
    
    btn_delete = tk.Button(win_view, text='Delete Pet', command = delete_win).pack()
    btn_update = tk.Button(win_view, text='Update Pet', command = update_win).pack()

    for pet in pets.findall('pet'):
        p_id = pet.find('id').text
        p_name = pet.find('name').text
        p_type = pet.find('type').text
        p_age = pet.find('age').text
        p_gender = pet.find('gender').text
        p_desc = pet.find('description').text

        # get contact data
        adopter_list = []
        for adopter in contact_root.findall('adopter'):
            if adopter.find('id').text == p_id:
                adop_name = adopter.find('./contact/name').text
                adop_num = adopter.find('./contact/contact_num').text
                adop_email = adopter.find('./contact/email').text
                adopter_list.append(f"{adop_name}, {adop_num}, {adop_email}")
        contacts = ' | '.join(adopter_list) if adopter_list else "No contacts available"
        table.insert('', 'end', text=p_id, values=(p_id, p_name, p_type, p_age, p_gender, p_desc, adopter_list))

    win_view.mainloop()

# update GUI
def update_win():
    global win_update, edit_select_id, edit_upload_status, pet_id_edit,edit_id_input, edit_name_input, edit_type_input, edit_age_input, edit_gender_input, edit_desc_input, edit_pass_input, edit_img_input
    win_update = tk.Tk()
    win_update.title('Update Pet Details')

    # get the pet id that is selected from the table
    edit_select_id = table.selection()[0]
    pet_id_edit = table.item(edit_select_id)['values'][0]

    # labels, entry for GUI
    edit_id = tk.Label(win_update, text="ID : ")
    edit_id_input = tk.Entry(win_update)
    edit_name_l2 = tk.Label(win_update, text="Name : ")
    edit_name_input = tk.Entry(win_update)
    edit_type_l2 = tk.Label(win_update, text="Type : ")
    edit_type_input = tk.Entry(win_update)
    edit_age_l2 = tk.Label(win_update, text="Age: ")
    edit_age_input = tk.Entry(win_update)
    edit_gender_l2 = tk.Label(win_update, text="Gender : ")
    edit_gender_input = tk.Entry(win_update)
    edit_desc_l2 = tk.Label(win_update, text="Description : ")
    edit_desc_input = tk.Entry(win_update)
    edit_pass_l2 = tk.Label(win_update, text="Password : ")
    edit_pass_input = tk.Entry(win_update, show='*')
    edit_img_label = tk.Label(win_update, text="Image : ")
    edit_img = tk.StringVar()
    edit_img_input = tk.Entry(win_update, textvariable=edit_img)
    edit_upload_status = tk.Label(win_update, text='') 

    # display the GUI
    edit_id.pack()
    edit_id_input.pack()
    edit_name_l2.pack()
    edit_name_input.pack()
    edit_type_l2.pack()
    edit_type_input.pack()
    edit_age_l2.pack()
    edit_age_input.pack()
    edit_gender_l2.pack()
    edit_gender_input.pack()
    edit_desc_l2.pack()
    edit_desc_input.pack()
    edit_pass_l2.pack()
    edit_pass_input.pack()
    edit_img_label.pack()
    edit_img_input.pack()
    btn_upload = tk.Button(win_update, text='Upload', command = edit_image).pack()
    edit_upload_status.pack()
    btn_add = tk.Button(win_update, text='Update', command = update_pass_win).pack()  

    # filled the entries with the original data
    for pet in pets.findall('pet'):
        if pet.find('id').text == str(pet_id_edit):
            edit_id_input.insert(0,pet.find('id').text)
            edit_name_input.insert(0,pet.find('name').text)
            edit_type_input.insert(0,pet.find('type').text)
            edit_age_input.insert(0,pet.find('age').text)
            edit_gender_input.insert(0,pet.find('gender').text)
            edit_desc_input.insert(0,pet.find('description').text)
            edit_pass_input.insert(0,pet.find('password').text)
            edit_img_input.insert(0,pet.find('image').text)
            break
        
    # disable the entry so that user would not be able to edit
    edit_id_input.config(state='disabled')
    edit_pass_input.config(state='disabled')
    edit_img_input.config(state='disabled')

    win_update.mainloop()

# for rescuer to reupload image
def edit_image():
    img_file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if img_file :
        img.set(img_file)
        edit_upload_status.config(text='Image Successfully Uploaded.')

# update function
def update_pets():
    edit_id = edit_id_input.get()
    edit_name = edit_name_input.get()
    edit_type = edit_type_input.get()
    edit_age = edit_age_input.get()
    edit_gender = edit_gender_input.get()
    edit_desc = edit_desc_input.get()
    edit_pass = edit_pass_input.get()
    edit_img = edit_img_input.get()
    pet_update = pets[(int(edit_id)-1)]

    if not check_entries([edit_name_input, edit_type_input, edit_age_input, edit_gender_input, edit_desc_input]):
        messagebox.showwarning('Incomplete Form', "Please ensure that all fields are complete before submitting.")
        return
    else:
        if update_pet_pass_input.get() == pet_update.find('password').text:
            win_update_pass.destroy()
            for pet in pets.findall('pet'):
                if pet.find('id').text == str(pet_id_edit):
                    pet.find('id').text = edit_id
                    pet.find('name').text = edit_name
                    pet.find('type').text = edit_type
                    pet.find('age').text = edit_age
                    pet.find('gender').text = edit_gender
                    pet.find('description').text = edit_desc
                    pet.find('password').text = edit_pass
                    pet.find('image').text = edit_img
                    tree.write(pet_xml)
            table.item(edit_select_id, values=(edit_id, edit_name, edit_type, edit_age, edit_gender, edit_desc, edit_pass, edit_img))
            win_update.destroy()
            messagebox.showinfo('Updated Successfully', 'The pet details have been updated successfully.')
        else :
            win_update_pass.destroy()
            messagebox.showinfo('Update Unsucessful', 'The password inserted is wrong.')

# get password to update GUI
def update_pass_win():
    global win_update_pass, update_pet_pass_input
    win_update_pass = tk.Tk()
    win_update_pass.title('Update Pet Details')

    pet_pass = tk.Label(win_update_pass, text="Password : ")
    update_pet_pass_input = tk.Entry(win_update_pass, show='*')

    pet_pass.pack()
    update_pet_pass_input.pack()
    btn_done = tk.Button(win_update_pass, text="Update", command=update_pets).pack()

    win_update_pass.mainloop()

# get password to delete GUI
def delete_win():
    global win_del, pet_pass_input
    win_del = tk.Tk()
    win_del.title('Delete Pet')

    pet_pass = tk.Label(win_del, text="Password : ")
    pet_pass_input = tk.Entry(win_del, show='*')

    pet_pass.pack()
    pet_pass_input.pack()
    btn_done = tk.Button(win_del, text="Delete", command=delete_func).pack()

    win_del.mainloop()

# delete function
def delete_func():
    # check for password
    user_select_id = table.selection()[0]
    pet_id_xml = table.item(user_select_id)['values'][0]-1
    pet_id_table = table.item(user_select_id)['values'][0]
    pet_delete = pets[pet_id_xml]
    if pet_pass_input.get() == pet_delete.find('password').text :
        # double confirm 
        confirm = messagebox.askyesno("Confirm Details", f"Are you sure that you wish delete?")
        if confirm :
            win_del.destroy()
            for pet in pets.findall('pet'):
                if pet.find('id').text == str(pet_id_table):
                    pets.remove(pet)
                    tree.write(pet_xml)
                    break
            table.delete(user_select_id)
            messagebox.showinfo("Delete Successful", "The pet details have been deleted.")
        else : 
            win_del.destroy()
            messagebox.showinfo("Delete Unsuccessful", "Please select the again.")
    else :
        win_del.destroy()
        messagebox.showinfo("Delete Unsuccessful", "The password inserted is wrong. Please try again.") 

# function to add pets
def add_pets():
    # to get the latest id and auto increment
    latest_id = 0
    for pet in pets.findall('pet'):
        id = int(pet.find('id').text)
        if id > latest_id:
            latest_id = id
    
    new_id = latest_id+1

    p_name = name_input.get()
    p_type = type_input.get()
    p_age = age_input.get()
    p_gender = gender_input.get()
    p_desc = desc_input.get()
    p_pass = pass_input.get()
    if not check_entries([name_input,type_input, age_input, gender_input, desc_input, pass_input]):
        messagebox.showwarning('Incomplete Form', "Please ensure that all fields are complete before submitting.")
        return
    else : 
    # double confirm 
        confirm = messagebox.askyesno("Confirm Details", f"Are these details correct?\n\nName : {p_name}\nType : {p_type}\nAge : {p_age}\nGender : {p_gender}\nDescription : {p_desc}")

        if confirm :
            # save details
            # add data to XML, tree-->tree, root --> pets
            sub_element = ET.SubElement(pets, 'pet')
            id_data = ET.SubElement(sub_element, 'id')
            id_data.text = str(new_id)
            name_data = ET.SubElement(sub_element, 'name')
            name_data.text = p_name
            type_data = ET.SubElement(sub_element, 'type')
            type_data.text = p_type
            age_data = ET.SubElement(sub_element, 'age')
            age_data.text = p_age
            gender_data = ET.SubElement(sub_element, 'gender')
            gender_data.text = p_gender
            desc_data = ET.SubElement(sub_element, 'description')
            desc_data.text = p_desc
            pass_data = ET.SubElement(sub_element, 'password')
            pass_data.text = p_pass
            img_data = ET.SubElement(sub_element, 'image')
            img_data.text = img.get()

            tree.write(pet_xml, encoding="utf-8")
            messagebox.showinfo("Details Saved", "The pet details have been saved.")
            win2.destroy()
        else:
            messagebox.showinfo("Details Not Saved", "Please review your details and try again.")

# upload image when adding the pet for the first time 
def upload_image():
    img_file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if img_file :
        img.set(img_file)
        upload_status.config(text='Image Successfully Uploaded.')
    
# add pets GUI
def post_ads():
    global win2, name_input, type_input, age_input, gender_input, desc_input, add_status, img, upload_status, pass_input
    win2 = tk.Tk()
    win2.title('Insert Pet Details')
    ## insert one entry to upload image

    name_l2 = tk.Label(win2, text="Name : ")
    name_input = tk.Entry(win2)
    type_l2 = tk.Label(win2, text="Type : ")
    type_input = tk.Entry(win2)
    age_l2 = tk.Label(win2, text="Age: ")
    age_input = tk.Entry(win2)
    gender_l2 = tk.Label(win2, text="Gender : ")
    gender_input = tk.Entry(win2)
    desc_l2 = tk.Label(win2, text="Description : ")
    desc_input = tk.Entry(win2)
    pass_l2 = tk.Label(win2, text="Password : ")
    pass_input = tk.Entry(win2, show='*')
    img_label = tk.Label(win2, text="Image : ")
    img = tk.StringVar()
    img_input = tk.Entry(win2, textvariable=img, state="readonly")
    upload_status = tk.Label(win2, text='') 
    add_status = tk.Label(win2, text='') 

    name_l2.pack()
    name_input.pack()
    type_l2.pack()
    type_input.pack()
    age_l2.pack()
    age_input.pack()
    gender_l2.pack()
    gender_input.pack()
    desc_l2.pack()
    desc_input.pack()
    pass_l2.pack()
    pass_input.pack()
    img_label.pack()
    img_input.pack()
    btn_upload = tk.Button(win2, text='Upload', command = upload_image).pack()
    upload_status.pack()
    add_status.pack()
    btn_add = tk.Button(win2, text='Add Pet', command = add_pets).pack()

    win2.mainloop()


# MAIN PAGE
root = tk.Tk()
root.geometry("300x300")
label = tk.Label(root, text='Welcome to Pet Adoption System!').pack()
btn1 = tk.Button(root, text='I want to adopt!', command = load_pets).pack()
btn2 = tk.Button(root, text='I want to post adoption ads!', command = post_ads).pack()
btn2 = tk.Button(root, text='I want to view/update/delete adoption ads!', command = view_pets).pack()
root.mainloop()
