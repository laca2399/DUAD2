from data_handler import User, Address, Car, session

# Create new user
new_user = User(name="Roberto")
new_user.create_user() 

# Create address for user
new_address = Address(street="27 LCL", city="Desamparados", user_id=new_user.id)
new_address.create_address()  

# Create new car
new_car = Car(branch="Toyota", model="Rav4", user_id=new_user.id)
new_car.create_car()  

# View all users
all_users = User.get_all()  #
print(all_users)

# Update car
new_car.update_car(new_branch="Honda", new_model="Civic")  
