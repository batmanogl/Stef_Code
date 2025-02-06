import random

def name_selection (name_gives, name_takes):
    person_gives_gift = random.choice(name_gives)
    person_takes_gift = random.choice(name_takes)
    if person_gives_gift == person_takes_gift and len(name_takes) != 1:
        new_person_takes = create_new_name_selection_list(list_b, person_takes_gift)
        person_takes_gift = random.choice(new_person_takes)
        name_gives.remove(person_gives_gift)
        name_takes.remove(person_takes_gift)
    elif person_gives_gift == person_takes_gift and len(name_takes) == 1:
        return None
    else:
        name_gives.remove(person_gives_gift)
        name_takes.remove(person_takes_gift)
    return person_gives_gift, person_takes_gift


def create_new_name_selection_list(name_takes, name_to_exclude):
    return [item for item in name_takes if item != name_to_exclude]

list_a = ["Bill", "Yiannis", "George", "Stefanos", "Panagiotis", "Stelios", "Apostolos"]
list_b = ["George", "Stefanos", "Bill", "Apostolos", "Panagiotis", "Stelios", "Yiannis"]

print ("This is a Python script for secret santa :-)\n")
i=0
while list_a:
    result = name_selection(list_a, list_b)
    if result is not None:
        person_who_will_give_gift, person_who_will_take_gift = result
        print (person_who_will_give_gift, "will give Christmas gift to", person_who_will_take_gift)
        i=i+1
    else:
        print("\nYou are really unlucky. The process is not completed. Run again the Python script")
        break

if i==7:
    print("\nThe secret santa Python script is completed successfully ! MERRY CHRISTMAS!")
