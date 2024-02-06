user = input('Create Username: ')
password = input('Create Password: ')
store_user =[""]
store_pass=[""]
store_user.append(user)
store_pass.append(password)

if user in store_user:
    print("That user already exsist")

while 1 == 1:
    userguess=""
    passwordguess=""
    key=""
    print("Welcome,",user, "you can now log into the database")
    print(store_user)
    print(store_pass)
exit()