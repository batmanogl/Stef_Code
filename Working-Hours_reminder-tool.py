from datetime import datetime

date_time = datetime.now().strftime('%H:%M:%S %d-%B-%Y')
print(date_time)

time = datetime.now().strftime('%H:%M')

if time == "08:59":
    print("Welcome Stef, It is Check-in time !")
elif time == "16:59":
    print("GoodBye Stef, It is Check-out time !")
elif "09:00" <= time <= "16:58":
    print("Stef, you are already in working hours !")
else:
    print("Out of working hours, better to rest :-) ")

