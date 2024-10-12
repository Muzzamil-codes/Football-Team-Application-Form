from tkinter import messagebox
import time
from tkinter import *
from PIL import Image, ImageTk
import socket


HEADER = 69
PORT = 4069  # 16688
DISCONNECT = "!disconnected"
SERVER = "127.0.0.1"  # 18.221.148.103
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

root = Tk()
root.title("Virtual Record")
# root.iconbitmap("icon.ico")
root.geometry("600x490")
root.config(bg="#121212")

bg_image = (Image.open("background.png"))
bg_f_image = ImageTk.PhotoImage(bg_image)

bg_frame = Frame(root, width=410, height=390, bg="#ffffff")
bg_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

image_lable = Label(bg_frame, width=410, height=390, image=bg_f_image)
image_lable.place(relx=0.5, rely=0.5, anchor=CENTER)

frame = Frame(bg_frame, width=400, height=380, bg="#181818")
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

image = (Image.open("logo.png"))
re_image = image.resize((80, 80))
f_image = ImageTk.PhotoImage(re_image)


Label_1 = Label(frame, text="Enter your name.",
                fg="#ffffff", bg="#181818")
Label_1.place(relx=0.5, rely=0.28, anchor=S)

input_word = Entry(frame, bg="#121212", bd=0, fg="#ffffff")
input_word.config(insertbackground='white')
input_word.place(relx=0.5, rely=0.35, anchor=S, width=200)

Label_2 = Label(frame, text="Enter the player number you want (it should be under 100)",
                fg="#ffffff", bg="#181818")
Label_2.place(relx=0.5, rely=0.47, anchor=S)

input_number = Entry(frame, bg="#121212", bd=0, fg="#ffffff")
input_number.config(insertbackground='white')
input_number.place(relx=0.5, rely=0.55, anchor=S, width=150)

Label_3 = Label(frame, text="Select your official team.",
                fg="#ffffff", bg="#181818")
Label_3.place(relx=0.5, rely=0.65, anchor=S)


# Team_Button = Button(frame, bd=0, bg="#121212", text=text_button,
#                     width=19, height=2, command=Team_button, activebackground="#121212", fg="#828282")
#Team_Button.place(relx=0.5, rely=0.81, anchor=N)

#################################################server process##########################################


def send(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

##########################################################################################################


Team = IntVar()
Team.set("1")

Position = StringVar()
Position.set("GK")


def Send_data():
    global Team_
    try:
        Player_name = input_word.get()
        Player_number = str(input_number.get())
    except ValueError:
        messagebox.showwarning(
            "Invalid Entry", "Please Enter valid data.")
    # send(Team_name)

    try:
        Player_number = int(Player_number)
        if Player_number >= 100:
            messagebox.showerror(
                "Invalid Entry", "You can't enter number above 100!")
        else:
            if Team.get() == 1:
                Team_ = "Team FCB"
            else:
                Team_ = "Team SFC"

            message = f"{Player_name}, {Player_number}, {Team_}, {Position.get()}"

            send(message)

            server_message = client.recv(2048)
            server_message = server_message.decode("utf-8")

            messagebox.showinfo("Message from the Server", str(server_message))
    except ValueError:
        messagebox.showerror(
            "Invalid Entry", "Enter only numbers please!")


Team_FCB = Radiobutton(frame, text=" FCB ", variable=Team, value=1,
                       activebackground="#181818", activeforeground="#ffffff")
Team_FCB.place(relx=0.47, rely=0.7, anchor=E)

Team_SFC = Radiobutton(frame, text=" SFC ", variable=Team, value=2,
                       activebackground="#181818", activeforeground="#ffffff")
Team_SFC.place(relx=0.67, rely=0.7, anchor=E)

Label_4 = Label(frame, text="Select your Positon.",
                fg="#ffffff", bg="#181818")
Label_4.place(relx=0.5, rely=0.82, anchor=S)

Goal_Keeper = Radiobutton(frame, text=" Goal Keeper ", variable=Position, value="GK",
                          activebackground="#181818", activeforeground="#ffffff")
Goal_Keeper.place(relx=0.34, rely=0.9, anchor=E)

Defender = Radiobutton(frame, text=" Defender ", variable=Position, value="DF",
                       activebackground="#181818", activeforeground="#ffffff")
Defender.place(relx=0.53, rely=0.9, anchor=E)

Mid_fielder = Radiobutton(frame, text=" Mid fielder ", variable=Position, value="MF",
                          activebackground="#181818", activeforeground="#ffffff")
Mid_fielder.place(relx=0.75, rely=0.9, anchor=E)

Striker = Radiobutton(frame, text=" Striker ", variable=Position, value="ST",
                      activebackground="#181818", activeforeground="#ffffff")
Striker.place(relx=0.91, rely=0.9, anchor=E)

button = Button(frame, bd=0, bg="#181818",
                image=f_image, width=80, command=Send_data, height=80, activebackground="#181818")
button.place(relx=0.5, rely=0.24, anchor=S)


def on_closing():
    if messagebox.askokcancel("Quit?", "Do you want to close the app?"):
        send(DISCONNECT)
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
