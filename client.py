import socket
from threading import Thread
from tkinter import*

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")


class GUI:
    def __init__(self):
        self.window=Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)

        self.applabel=Label(self.login,text ="Chatroom", justify=CENTER,font="Helvetica 14 bold")
        self.applabel.place(relx=0.4,rely=0.07,relheight=0.15)


        self.labelname=Label(self.login,text= "name: ", font="Helvetica 14",)
        self.labelname.place(relx=0.1,rely=0.2,relheight=0.2)

        self.entryname=Entry(self.login,font="Helvetica 14")
        self.entryname.place(relx=0.35,rely=0.3,relheight=0.12,relwidth=0.4)
        self.entryname.focus()

        self.go= Button(self.login,text="CONTINUE",font="Helvetica 14 bold" ,command=lambda:self.goTochatScreen(self.entryname.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.window.mainloop()

    def goTochatScreen(self,name):
        self.login.destroy()
        self.chatLayout(name)
        receive_thread = Thread(target=self.receive)
        receive_thread.start()



    def chatLayout(self,name):
        self.name=name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False,height=False)

        self.window.configure(width=470,height=550,bg="darkblue")

        self.labelHead= Label(self.window,bg="red", fg="white", text=self.name,font="Helvetica 14 bold",pady=5)
        self.labelHead.place(relwidth=1)

        self.line= Label(self.window,width=450,bg="green")
        self.line.place(relwidth=1,rely=0.07,relheight=0.01)

        self.textCons=Text(self.window,width=20,height=2,bg="cyan",fg="white",font="Helvetica 14", padx=5,pady=5)
        self.textCons.place(relheight=0.74,relwidth=1,rely=0.08)

        self.labelButton=Label(self.window,bg="pink",height=80)
        self.labelButton.place(relwidth=1,rely=0.80)

        self.entryMsg= Entry(self.labelButton,bg="yellow",fg="black",font="Helvetica 14")
        self.entryMsg.place(relwidth=0.7,relheight=0.06,rely=0.008,relx=0.001)

        self.send= Button(self.labelButton,text="send",font="Helvetica 14 bold", bg="green",command=lambda:self.sendbutton(self.entryMsg.get()))
        self.send.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)

        self.scrollBar=Scrollbar(self.textCons)
        self.scrollBar.place(relheight=1,relx=0.95)

        self.scrollBar.config(command=self.textCons.yview)
        self.textCons.config(cursor="arrow")

        self.textCons.config(state=DISABLED)






    def sendbutton(self,message):
         self.textCons.config(state=DISABLED)
         self.message=message
         self.entryMsg.delete(0,END)
         send=Thread(target=self.write)
         send.start()

    

    def showMsg(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)







    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    print(message)
                    self.showMsg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        while True:
            message = (f"{self.name}:{self.message}")
            client.send(message.encode('utf-8'))
            self.showMsg(message) 
            break

# creating mygui chatroom by using GUI class
mygui=GUI()







