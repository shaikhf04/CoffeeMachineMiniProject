import sys
from data.menu import bill, instock, blackCoffee, latte, cappuccino
from data.resource import resource
from exception.stock_exception import OutOfStockError

# Function to make coffee
'''
    1. check stock
    2. if available deduct used ingrediants
    3. update stock 
    4. do payment
    5. done
'''
#work on this to make common function based on coffee item passed
def checkStockAvailability():
    canMake = True   
        #check for stock availability
    for required_item, required_quantity in blackCoffee.items():
        instock_quantity = instock.get(required_item,0) 
        print(f"{required_item}: Required {required_quantity}, In Stock {instock_quantity}")
        if  required_quantity > instock_quantity:
            canMake = False
            print(f"Stock not enough to make your {required_item}.\n Need: {required_quantity} and Stock: {instock_quantity} ") 
            raise OutOfStockError(f"Not enough {required_item} in stock to make your order.")
    return canMake

def makePayment():
    print("\nYour total bill is: $", bill["Black Coffee"])
    confirmPayment = input("Confirm payment? (Y/N): ")
    if confirmPayment.lower() != 'y':
        print("Payment not confirmed, order cancelled!")
    else:
        print("Payment confirmed, preparing your order!")

def makeBlackCoffee():
    #check stock availability before making coffee 
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in blackCoffee.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        print("Updated stock")
        for item, quantity in instock.items():
            print(f"{item}: {quantity}")

def makeLatte():
        #check stock availability before making coffee 
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in latte.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        print("Updated stock")
        for item, quantity in instock.items():
            print(f"{item}: {quantity}")

def makeCappuccino():
    #check stock availability before making coffee 
    if checkStockAvailability() == False :
        print("Not enough stock to make your order, please try again later!")
    else:
        for required_item, required_quantity in cappuccino.items():
            if(instock[required_item] >= required_quantity):
                instock[required_item] -= required_quantity
        print("Updated stock")
        for item, quantity in instock.items():
            print(f"{item}: {quantity}")

def showMenu():
    print("\nWelcome to the Coffee Bot\nChoose from 1-3 to order:\nType 'exit' to cancel:")
    print("----- Menu -----")
    for order_id, (item, price) in enumerate(bill.items(), start=1):
        print(f"{order_id}. {item} - ${price:.2f}")
    print("----------------")
    return input("\n> ")

    
def main():
    choice = None
    count = 0

    while choice != "exit":

        choice = showMenu()
        try:
            if choice == "1":
                makeBlackCoffee()
                #makePayment()
                count += 1
            elif choice == "2":
                makeLatte()
                count += 1
            elif choice == "3":
                makeCappuccino()
                count += 1
            elif choice == "exit":
                print("You did not place any order, Thank you and visit again!")
            else:
                print("Oops! Incorrect choice. Please try again.")
        except OutOfStockError as e:
            print(f"Order could not be completed: {e}")
    sys.exit(0)

    print("You've ordered", count, "item(s). Enjoy your coffee!")

#Function call to run project
main()
