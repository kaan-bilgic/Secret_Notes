from tkinter import *
from PIL import Image, ImageTk
from cryptography.fernet import Fernet,InvalidToken
import base64, hashlib
from tkinter import messagebox

window = Tk()
window.title("Secret Notes")
window.geometry("400x650")
window.configure(background="light gray")

my_font = ("Arial", 13, "normal")

def encrypt():

    title_entry_get = title_entry.get()
    secret_text_get = secret_text.get("1.0", "end-1c")  # son satırdaki fazladan boşluğu almaz
    masterkey_entry_get = masterkey_entry.get()

    if masterkey_entry_get == "" or secret_text_get == "" or title_entry_get == "":
        messagebox.showerror("ERROR","Please enter all the required information!!")
        return

    try:
        hash_object = hashlib.sha256(masterkey_entry_get.encode("utf-8"))
        fernet_key = base64.urlsafe_b64encode(hash_object.digest())

        f = Fernet(fernet_key)

        metin_byte = secret_text_get.encode("utf-8")
        encrypted_data = f.encrypt(metin_byte)

        dosya_yolu = f"C:/Users/Kaan BİLGİÇ/OneDrive/Desktop/Secret_Notes/mysecret.txt"

        with open(dosya_yolu, "a", encoding="utf-8") as file:
            file.write(f"\n{title_entry_get}\n")                  # kullanıcın girdiği başlığı yazıyoruz
            file.write(f"{encrypted_data.decode("utf-8")}\n")   # kullanıcın girdiği text'in şifrelenmiş halini yazıyoruz

        title_entry.delete(0, END)
        secret_text.delete(1.0, END)
        masterkey_entry.delete(0, END)

        messagebox.showinfo("SUCCESS","Note encrypted and saved successfully!!")

    except InvalidToken:
        messagebox.showerror("ERROR","An error occured during encryption!!")

def decrypt():

    secret_text_get = secret_text.get("1.0", "end-1c")
    masterkey_entry_get = masterkey_entry.get()

    if masterkey_entry_get == "" or secret_text_get == "":
        messagebox.showerror("ERROR", "Please enter all the required information!!")
        return

    try:
        hash_object = hashlib.sha256(masterkey_entry_get.encode("utf-8"))
        fernet_key = base64.urlsafe_b64encode(hash_object.digest())

        f = Fernet(fernet_key)

        encrypted_byte = secret_text_get.encode("utf-8")
        decrypted_byte = f.decrypt(encrypted_byte)

        decrypted_text = decrypted_byte.decode("utf-8")

        secret_text.delete(1.0, END)
        secret_text.insert(1.0, decrypted_text)

        messagebox.showinfo("","Successfully decrypted!!")

    except InvalidToken:
        messagebox.showerror("ERROR","Invalid master key or corrupted text!!")

# logo_lable
top_secret_pil = Image.open('top_secret.png')      # önce resmi açıyoruz
top_secret_pil = top_secret_pil.resize((100,100))  # istersek yeniden boyutlandırıyoruz
top_secret_tk = ImageTk.PhotoImage(top_secret_pil) # sonra Tk'ya dönüştürüyoruz
logo_label = Label(image=top_secret_tk)            # sonra resmi bir label'a atıyoruz
logo_label.pack(pady=(50,10))                      # ve son olarak label'ı gösteriyoruz

'''
x = PhotoImage(file="top_secret.png")
x_label = Label(image=x)
x_label.pack()              --> böyle de oluşturulabilir
'''

# label1
title_label = Label(text="Enter your title", font= my_font, bg="light gray", fg="black")
title_label.pack(pady=(30,5))

# entry1
title_entry = Entry(width=40)
title_entry.pack(pady=(5,5))

# label2
secret_label = Label(text="Enter your secret", font= my_font, bg="light gray", fg="black")
secret_label.pack(pady=(5,5))

# text
secret_text = Text(width=30 , height=10, font= my_font, bg="white", fg="black")
secret_text.pack(pady=(5,5))

# label3
masterkey_lable = Label (text= "Enter master key", font= my_font, bg="light gray", fg="black")
masterkey_lable.pack(pady=(5,5))

# entry2
masterkey_entry = Entry(width=40)
masterkey_entry.pack(pady=(5,5))

# button1
encrypt_button = Button (text= "Save & Encrypt", font=my_font, bg="white", fg="black", command=encrypt)
encrypt_button.pack(pady=(5,5))
encrypt_button.pack(pady=(5,5))

# button2
decrypt_button = Button (text= "Decrypt", font=my_font, bg="white", fg="black", command=decrypt)
decrypt_button.pack(pady=(5,5))


window.mainloop()











