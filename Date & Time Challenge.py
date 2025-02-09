import calendar

Playing = True
while Playing == True:
    

    run_program = input("Type 'yes' if you want to count how many times appear a specific day of month in a specific year, otherwise type 'exit': ")

    print('''
'''
)

    if run_program == "yes":

        try:
            year = int(input("Write the year that you want to count: "))
            month = int(input("Specify the number of the month (i.e 1 for January, 2 for February, etc): "))
            num_day = int(input("Write me the number of the day, that you want to count (0 is Monday & 6 is Sunday): "))

            if num_day == 0:
                day = calendar.MONDAY
            elif num_day == 1:
                day = calendar.TUESDAY
            elif num_day == 2:
                day = calendar.WEDNESDAY
            elif num_day == 3:
                day = calendar.THURSDAY
            elif num_day == 4:
                day = calendar.FRIDAY        
            elif num_day == 5:
                day = calendar.SATURDAY
            elif num_day == 6:
                day = calendar.SUNDAY
            else:
                print("Invalid Input")

            num_days = 0
            for i in range(1, calendar.monthrange(year, month)[1]): ## We put the [1], because calendar.monthrange(year, month) is a tuple with 2 elements and we want the 2nd element. The step of the range is by default 1.   
                if calendar.weekday(year, month, i) == day:
                    num_days = num_days + 1

            print(f"The day you choose appears {num_days} times in month {month} of year {year}")

            print('''
'''
) 

        except ValueError:
            print('''
String characters are not valid'''
                  )
        except NameError:
            print ('''
Invalid Input'''
                   )


    elif run_program == "exit":
        Playing = False
        print("Ok, Nice to meet you!")
        break
    else:
        print("Invalid Input. TRY AGAIN !")


