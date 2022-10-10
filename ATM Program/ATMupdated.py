import os.path                                                                      # lbr read & write files
import csv                                                                          # import & export format for CSV files
from datetime import datetime                                                       # lbr to set time and date 

file = 'history.txt'                                                                # define the file 
masterlist, master_rec = ([] for i in range(2))                                     # create an array master list to retrieve any existing transaction history
error_msg1 = 'Unable to dispense full amount requested at this time'                # declare errors
error_msg2 = 'Unable to process your withdrawal at this time'
error_msg3 = 'You have been charged an overdraft fee of $5.'

# GET NEW RECORD TRANSACTION
def get_record(x,y,z):
    record, overdraft = ([] for i in range(2))
    now = datetime.now()                                                            # get current date & time
    date = now.strftime('%Y-%m-%d')                                                 # format date 
    time = now.strftime('%H:%M:%S')                                                 # format time

    balance, over, amount = x, y, z

    if over == 0:
        record.extend((date, time, amount, balance))
        master_rec.append(record)
        with open(file, 'a+', newline='') as data:
            writer = csv.writer(data)
            writer.writerows(master_rec)
        transc_history()
                
    elif over == -5:
        record.extend((date, time, amount, balance))
        overdraft.extend((date, time, over, balance+over))
        master_rec.append(record)
        master_rec.append(overdraft)
        with open(file, 'a+', newline='') as data:
            writer = csv.writer(data)
            writer.writerows(master_rec)

# GET CURRENT BALANCE (IF ANY) FROM FILE
def current_balance(): 
    if os.path.getsize(file) == 0:                                                  # check if 'transaction history' file has any records
        return 50000                                                                  # set balance to 500
    else:
        n = float(masterlist[-1][-1])*100
        return n

# RETRIEVE EXISTING TRANSACTION HISTORY (IF ANY)
def transc_history():
    with open(file, 'r') as data:                                                   # opens record file for trasaction history 
        reader = csv.reader(data)                                                   # read data in the file 
        for row in reader:                                                          # iterate over the reader append rows to masterlist array
            masterlist.append(row)
  

# MAIN FUNCTION WITH FIVE ATM COMMANDS
def main():
    acc_balance = int(current_balance())                                            # retrieve ATM balance
    atm_balance = int(10000*100)
    print()                                                    # set ATM balance to $10,000
    print("**********\t\tBoston Regional ATM\t\t**********\n")
    print("Type 'help' to display the command list\n")                              # display ATM menu by typing 'help'
    command = input('>>> ').lower()

    while command != 'end':
        if command == 'help':                                                       # display options available for ATM
            print("\nwithdraw <value>\t\t\t-Withdraw money from account-\n") 
            print("deposit <value>\t\t\t\t-Deposit money to account-\n")
            print("balance\t\t\t\t\t-Print account balance-\n")
            print("history\t\t\t\t\t-Print transaction history-\n")
            print("end\t\t\t\t\t-Finish ATM transactions-\n")
            command = input('>>> ').lower()

        # WITHDRAW FROM ACCOUNT
        elif 'withdraw' in command:  

            if command == 'withdraw':
                print('\nAmount not specified. Please try again.\n')                # errors when not input int amount (Any integer)
                command = input('>>> ').lower()                                     # take any int value after typing withdraw
            else:
                brk = command.split()                                               # split command 
                amount = abs(int(float(brk[-1])*100))                                    # set amount to be use in operation 

                if acc_balance <= 0:
                    print('Your account is overdrawn')
                    command = input('>>> ').lower()
                else:
                    if amount <= acc_balance:                                       # if the user account is less than ATM balance 
                        acc_balance -= amount                                       # subtract amount from ATM balance
                        print('\nAmount dispensed: $', amount/100,'\n')             # print the amount dispensed
                        print('Current balance: $', acc_balance/100, '\n')          # display user's negative balance              
                        acc_over = 0                                                # initialize overwithdraw subtracting 5 from ATM balance
                        get_record(acc_balance/100, acc_over, (amount/100)*-1)
                        command = input('>>> ').lower()

                    elif amount > acc_balance:                                    
                        acc_balance -= amount                                       # subtract the amount from ATM if its less than the ATM balance 
                        acc_over = -5
                        print('\nAmount dispensed: $', amount/100)
                        print(error_msg3 +' Current balance:', acc_balance/100, '\n')
                        get_record(acc_balance/100, acc_over, (amount/100)*-1)
                        command = input('>>> ').lower()
                    
                    elif amount > atm_balance:                                      # display error when the amount is greater than atm _reserve
                        print('\n'+error_msg1+'\n')                     
                        print('Please try a different amount\n')
                        command = input('>>> ').lower()                             # input amount to withdraw 

                    else:
                        print('\nAmount not valid. Please try again.\n')            # error if any int is input
                        command = input('>>> ').lower()
                    
        # DEPOSIT TO ACCOUNT
        elif 'deposit' in command:
            if command == 'deposit':
                print('\nAmount not specified. Please try again.\n')                # enter int values 
                command = input('>>> ').lower()                              
            else:
                brk = command.split()                                               # separate the values
                amount = abs(int(float(brk[-1])*100))
                acc_balance += amount                                               # add amount to acc_balance 
                acc_over =0                                      
                print('\nCurrent balance: $', acc_balance/100,'\n')                     # display acc_balance 
                get_record(acc_balance/100, acc_over, amount/100)
                print()
                command = input('>>> ').lower()

        # CHECK ACCOUNT BALANCE
        elif command == 'balance':
            print('\nCurrent balance: $', acc_balance/100,'\n')
            command = input('>>> ').lower()

        # DISPLAY ACCOUNT TRANSACTION HISTORY
        elif command == 'history':                                                  # Move this to a funtion 
            print("\n\t\t\tACCOUNT TRANSACTION HISTORY\n")      
            print("Date\t\t\tTime\t\t\tAmount\t\tBalance\n")    
            for transaction in masterlist:                                          # iterate over the masterlist
                transaction_printable = f"{transaction[0]}\t\t{transaction[1]}\t\t{transaction[2]}\t\t{transaction[3]}"     # check for all the value in the masterlist and add spaces
                print(transaction_printable)
            print()   
            command = input('>>> ').lower()                         
        else:
            print("\nCommand not valid. Type 'help' to dispay the command list\n")
            command = input('>>> ')


transc_history()
main()
print("\n**********\t\tThanks for using Boston Regional ATM\t\t**********\n")

#print('\nprinting masterlist')
#for transaction in masterlist:                                         
#                transaction_printable = f"{transaction[0]}\t\t{transaction[1]}\t\t{transaction[2]}\t\t{transaction[3]}"
#                print(transaction_printable)





