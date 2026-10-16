num = int(input("Enter a number: "))

if num % 3 == 0 and num % 5 == 0:
    print("FIZZBUZZ")
elif num % 3 == 0:
    print("FIZZ")
elif num % 5 == 0:
    print("BUZZ")
else:
    print("OM PHAT SWAHA")
