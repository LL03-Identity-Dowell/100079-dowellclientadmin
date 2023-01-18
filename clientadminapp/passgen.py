import string
import random


## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
characters1 = list(string.ascii_letters + string.digits)
def generate_random_password(num):
	## length of password from the user
	length = num

	## shuffling the characters
	random.shuffle(characters)

	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	rr="".join(password)
	return rr
def generate_random_password1(num):
	## length of password from the user
	length = num

	## shuffling the characters
	random.shuffle(characters1)

	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters1))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	rr="".join(password)
	return rr

## invoking the function