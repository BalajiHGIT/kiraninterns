balance = 10000

while True:
    print("\n===== BANKING CONSOLE APPLICATION =====")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print(f"Current Balance: ₹{balance:.2f}")

    elif choice == "2":
        try:
            amount = float(input("Enter deposit amount: ₹"))

            if amount > 0:
                balance += amount
                print(f"Deposit Successful!")
                print(f"Updated Balance: ₹{balance:.2f}")
            else:
                print("Error: Deposit amount must be greater than 0.")

        except ValueError:
            print("Error: Please enter a valid amount.")

    elif choice == "3":
        try:
            amount = float(input("Enter withdrawal amount: ₹"))

            if amount <= 0:
                print("Error: Withdrawal amount must be greater than 0.")
            elif amount <= balance:
                balance -= amount
                print("Withdrawal Successful!")
                print(f"Updated Balance: ₹{balance:.2f}")
            else:
                print("Error: Insufficient balance.")

        except ValueError:
            print("Error: Please enter a valid amount.")

    elif choice == "4":
        print("Thank you for using our Banking Application!")
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Please select 1, 2, 3, or 4.")
