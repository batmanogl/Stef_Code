# Palindrome Game

def is_palindrome(newstr):
    newstr = newstr.lower()
    newstr = newstr.replace(" ","")
    if newstr == newstr [::-1]:
        return "Yes, this is a palindrome"
    return "This is not a Palindrome"

Playing = True
while Playing == True:
    print('''
'''
          )
    print ("Welcome in Palindrome game. Spaces are not take into consideration. ")
    print ("Write 'exit' if you want to stop the game")
    newstr = input ("Give me your input, and I will check if it is a palindrome: ")
    if newstr == "exit":
        Playing = False
        print("Ok, Nice to meet you!")
        break
    print(is_palindrome(newstr))
