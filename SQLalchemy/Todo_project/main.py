import sys
import os
from database import Item, User, Session

def main():
    function = input("Do you want to register or login?: ").lower()
    if function not in ["register", "login"]:
        print('Please type "register" or "login"')
        sys.exit(1)
    if function == 'register': 
        register_user()
    if function == 'login': 
        logged_in_user = login_user()
        if logged_in_user:
            user_menu(logged_in_user)

def user_menu(user):
    while True:
        print(f"{os.linesep}What do you want to do today?")
        print("1: View todo items")
        print("2: Create new todo item")
        print("3: Remove item")
        print("4: Exit" + os.linesep)
        selection = input()
        if selection == "1": 
            showItems(user)
        if selection == "2": 
            createItem(user)
        if selection == "3": 
            removeItem(user)
        if selection == "4": 
            sys.exit("Goodbye")

def register_user():
    username = input("Type your username: ")
    password = input("Type your password: ")
    with Session() as session:
        existing_user = session.query(User).filter_by(userName = username).first()
        if existing_user:
            print("Account already exists.")
        else:
            new_user = User(userName=username, passWord = password)
            session.add(new_user)
            session.commit()
            print("User registered successfully.")
            return new_user

def login_user():
    username = input("Type your username: ")
    password = input("Type your password: ")
    with Session() as session:
        user = session.query(User).filter_by(userName = username, passWord = password).first()
        if user:
            print("Welcome to the system.")
            return user
        else:
            print("Wrong username or password.")
            return None

def showItems(user):
    print("Your todo lists")
    print("___")
    with Session() as session:
        items = session.query(Item).filter(Item.user_id == user.id)
        for item in items:
            itemId = item.itemId
            itemName = item.name
            description = item.description
            added_time = item.added_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Item ID: {itemId}")
            print(f"Name: {itemName}")
            print(f"Description: {description}")
            print(f"Added Time: {added_time}")
            print("___" + os.linesep)


def createItem(user):
    print("Name for the item:")
    itemName = input()
    description = input("Description (optional): ")
    with Session() as session:
        newItem = Item(name=itemName, description=description, user_id=user.id)
        session.add(newItem)
        session.commit()

def removeItem(user):
    with Session() as session:
        itemAmount = session.query(Item).filter(Item.user_id == user.id).count()
        if itemAmount < 1:
            print("You should add some items first.")
            return
        print("Give ID to remove:")
        itemId = int(input())
        removableItem = session.query(Item).filter(Item.itemId == itemId, Item.user_id == user.id)
        if removableItem.count() > 0:
            session.delete(removableItem.one())
            session.commit()
        else:
           print("Invalid ID!")

print("Welcome to TOD-O List O-maker version 5123.524")
main()
