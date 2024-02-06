username = input("User ID? ")
Login = ["Passwords"]
credentials = ["email : (enter your email) password : (enter your password)"]
files = ["Press windows key + 3"]


(user) = "nael"
(passwords) = "Amaz0n123!"
(securitypin) = "0770"

#User

if username == "nael":
    password = input("Password? ")
else:
    print(" Sorry, you may not have access to this database.")

#Password     
if password in passwords:
    security = input("Security Pin ?")
else:
    print("Wrong Password")
    password = input("Password: ")
#PIN
if security in securitypin:
    print("Hello ->" , username)
    print("Here are your credentials" , credentials)
    print("To view your files," , files)
else:
    print("Wrong Pin, please try again!")
    security = input("What is the Security Pin?")
exit()