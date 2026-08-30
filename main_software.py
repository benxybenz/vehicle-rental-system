import json

class Vehicle:
    def __init__(self,vehicle_id,brand,model,manufacturing_year,rental_price,availabilty_status,type_of_vehicle):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.manufacturing_year = manufacturing_year
        self.rental_price = rental_price
        self.availabilty_status = availabilty_status
        self.type_of_vehicle = type_of_vehicle


    def display_vehicle(self):
        print("========================================")
        print(f"Vehicle_id = {self.vehicle_id}")
        print(f"Brand = {self.brand}")
        print(f"Model = {self.model}")
        print(f"Manufacturing year = {self.manufacturing_year}")
        print(f"Rental price = {self.rental_price}")
        print(f"Avilability status = {self.availabilty_status}")
        print(f"Type = {self.type_of_vehicle}")
        print("================================================")

    def to_dict(self):
        vehicle_dictonary = {"Vehicle_id":self.vehicle_id,
                            "Brand":self.brand,
                            "Model":self.model,
                            "Manufacturing year":self.manufacturing_year,
                            "Rental price":self.rental_price,
                            "Avilability status":self.availabilty_status,
                            "Type":self.type_of_vehicle
        }
        return vehicle_dictonary




class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle,no_of_doors,fuel_type):
        super().__init__(vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle)
        self.no_of_doors = no_of_doors
        self.fuel_type = fuel_type

    def to_dict(self):
        vehicle_dictonary = super().to_dict()
        vehicle_dictonary["No of doors"] = self.no_of_doors
        vehicle_dictonary["Fuel type"] = self.fuel_type
        return vehicle_dictonary


class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle,engine_capacity):
        super().__init__(vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle)
        self.engine_capacity = engine_capacity


    def to_dict(self):
        vehicle_dictonary =super().to_dict()
        vehicle_dictonary["engine capacity"] = self.engine_capacity
        return vehicle_dictonary



class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle,load_capacity):
        super().__init__(vehicle_id, brand, model, manufacturing_year, rental_price, availabilty_status, type_of_vehicle)
        self.load_capacity = load_capacity

    def to_dict(self):
        vehicle_dictonary =  super().to_dict()
        vehicle_dictonary["load_capacity"] = self.load_capacity
        return vehicle_dictonary



# this stores all the data of the shop which vehicle is taken by whom how many remain 
class Rental_system:

    bike_count = 0
    car_count = 0 
    truck_count = 0 
    customer_count = 0
    rental_count = 0

    def __init__(self,data_base_of_customers = None,data_base_of_vehicles = None,data_base_of_rentals = None):
        if data_base_of_customers is None:
            self.data_base_of_customers = []
        else :
            self.data_base_of_customers = data_base_of_customers
        if data_base_of_vehicles is None:
            self.data_base_of_vehicles = []
        else:
            self.data_base_of_vehicles = data_base_of_vehicles
        if data_base_of_rentals is None:
            self.data_base_of_rentals = []
        else:
            self.data_base_of_rentals = data_base_of_rentals


    def to_dict(self):
        vehicle_list = []
        customer_list = []
        rental_list = []
        for vehicle in self.data_base_of_vehicles:
            vehicle_list.append(vehicle.to_dict())
        for customer in self.data_base_of_customers:
            customer_list.append(customer.to_dict())
        for rental in self.data_base_of_rentals:
            rental_list.append(rental.to_dict())
        all_data = {"vehicles":vehicle_list, "customers":customer_list,"rentals":rental_list }
        return all_data


    def vehicle_from_dict(self,vehicle_dictonary):
        if vehicle_dictonary["Type"] == "Car" :
            car = Car(vehicle_dictonary["Vehicle_id"],vehicle_dictonary["Brand"],vehicle_dictonary["Model"],vehicle_dictonary["Manufacturing year"],vehicle_dictonary["Rental price"],vehicle_dictonary["Avilability status"],vehicle_dictonary["Type"],vehicle_dictonary["No of doors"],vehicle_dictonary["Fuel type"])
            return car
        elif vehicle_dictonary["Type"] == "Bike" or vehicle_dictonary["Type"] == "Motorcycle":
            bike = Motorcycle(vehicle_dictonary["Vehicle_id"],vehicle_dictonary["Brand"],vehicle_dictonary["Model"],vehicle_dictonary["Manufacturing year"],vehicle_dictonary["Rental price"],vehicle_dictonary["Avilability status"],vehicle_dictonary["Type"],vehicle_dictonary["engine capacity"])
            return bike 
        elif vehicle_dictonary["Type"] == "Truck":
            truck = Truck(vehicle_dictonary["Vehicle_id"],vehicle_dictonary["Brand"],vehicle_dictonary["Model"],vehicle_dictonary["Manufacturing year"],vehicle_dictonary["Rental price"],vehicle_dictonary["Avilability status"],vehicle_dictonary["Type"],vehicle_dictonary["load_capacity"])
            return truck

    def customer_from_dict(self,customer_dictonary):
            customer = Customer(customer_dictonary["customer id"],customer_dictonary["name"],customer_dictonary["phone number"],customer_dictonary["address"])
            return customer

    def rental_from_dict(self,rental_dictonary):
        vehicle = self.vehicle_from_dict(rental_dictonary["rented vehicle details "])
        customer = self.customer_from_dict(rental_dictonary["rental customer details"])
        rental = Rental(rental_dictonary["rental id"],rental_dictonary["rental days"],vehicle,customer)
        return rental


    def load_data(self):
        try:
            with open ("Vehicle_rent.json","r") as f:
                whole_loaded_data = json.load(f)

                for vehicle_dict in whole_loaded_data["vehicles"]:
                    new_vehicle = self.vehicle_from_dict(vehicle_dict)
                    self.data_base_of_vehicles.append(new_vehicle)

                for customer_dict in whole_loaded_data["customers"]:
                    new_customer = self.customer_from_dict(customer_dict)
                    self.data_base_of_customers.append(new_customer)

                for rental_dict in whole_loaded_data["rentals"]:
                    new_rental = self.rental_from_dict(rental_dict)
                    self.data_base_of_rentals.append(new_rental)
        except FileNotFoundError:
            print("No such file exists ")
   
    
    def unique_vehicle_id_generator(self,type):
            if type in ["Bike","Motorcycle"]:
                Rental_system.bike_count += 1 
                b_id = "B" + str(Rental_system.bike_count)
                return b_id
            elif type in ["Car"]:
                Rental_system.car_count += 1 
                c_id = "C"+ str(Rental_system.car_count)
                return c_id 
            elif type in ["Truck"]: 
                Rental_system.truck_count += 1 
                t_id = "T"+ str(Rental_system.truck_count)
                return t_id 


    def type_identifer(self,vehicle_data):
        if vehicle_data["type"] in ["Bike","Motorcycle"]:
            engine_capacity = input("Enter the engine capacity = ")
            one_motorcycle = Motorcycle(
            vehicle_data["vehicle_id"],
            vehicle_data["brand"],
            vehicle_data["model"],
            vehicle_data["manufacturing_year"],
            vehicle_data["rental_price"],
            vehicle_data["avilability_status"],
            vehicle_data["type"],
            engine_capacity
            )
            return one_motorcycle

        elif vehicle_data["type"] in ["Car"]:
            no_of_doors = input("Enter the number of doors = ")
            fuel_type = input("Enter the fuel type = ")
            one_car = Car(
                            vehicle_data["vehicle_id"],
                            vehicle_data["brand"],
                            vehicle_data["model"],
                            vehicle_data["manufacturing_year"],
                            vehicle_data["rental_price"],
                            vehicle_data["avilability_status"],
                            vehicle_data["type"],
                            no_of_doors,
                            fuel_type
                        )
            return one_car
        
        elif vehicle_data["type"] in ["Truck"]:
            load_cap = input("Enter the load cap = ")
            one_truck = Truck(vehicle_data["vehicle_id"],
                                        vehicle_data["brand"],
                                        vehicle_data["model"],
                                        vehicle_data["manufacturing_year"],
                                        vehicle_data["rental_price"],
                                        vehicle_data["avilability_status"],
                                        vehicle_data["type"],
                                        load_cap
                                        )
            return one_truck
        

    def add_vehicle(self):
        vehicle_data = {  "brand":"",
                          "model":"",
                          "manufacturing_year":"",
                          "rental_price":"",
                          "avilability_status":"Avilable",
                          "type":"",
                          "vehicle_id":""

        }
        vehicle_data["brand"] = input("Enter brand name = ").capitalize()
        brand = vehicle_data["brand"]
        brand = self.brand_validator(brand)
        vehicle_data["brand"] = brand
        vehicle_data["model"] = input("Enter model name = ").capitalize()
        model = vehicle_data["model"]
        model = self.model_name_validator(model)
        vehicle_data["model"] = model
        vehicle_data["manufacturing_year"] = input("Enter manufacturing year = ")
        manu_year = vehicle_data["manufacturing_year"]
        manu_year = self.manufacturing_year_validator(manu_year)
        vehicle_data["manufacturing_year"] = manu_year
        vehicle_data["rental_price"] = input("Enter rental price = ")
        rental_price = vehicle_data["rental_price"]
        rental_price = self.rental_price_validator(rental_price)
        vehicle_data["rental_price"] = rental_price
        vehicle_data["type"] = input("Enter type = ").capitalize().strip()
        type = vehicle_data["type"]
        type = self.type_validator(type)
        vehicle_data["type"] = type
        vehicle_id = self.unique_vehicle_id_generator(type)
        vehicle_data["vehicle_id"] = vehicle_id
        one_vehicle = self.type_identifer(vehicle_data)
        self.data_base_of_vehicles.append(one_vehicle)
        print(f"{vehicle_data['brand']} of model {vehicle_data['model']}  {vehicle_data['type']} with id  {vehicle_data["vehicle_id"]} has been sucesfully added to our database ! ")
        return one_vehicle


    def brand_validator(self,brand):
        while True:
            is_empty = False 
            correct_data = False 
            valid_brand = False 
            if brand == "":
                is_empty = True
            if  brand.isalpha() : 
                correct_data = True
            if len(brand) > 2 : 
                valid_brand = True 
            if is_empty :
                print("No brand name given ")
                brand = input("Enter a brand name = ").capitalize()
                continue
            if  not correct_data:
                print("Input correct data ")
                brand = input("Enter the brand name again = ").capitalize()
                continue
            if not valid_brand:
                print("Input a valid brand name ")
                brand = input("Enter a valid brand name ").capitalize()
                continue
            if not is_empty and correct_data and valid_brand : 
                return brand



    def model_name_validator(self,model):
        while True:
            is_empty = False

            if model ==  "":
                is_empty = True 
                print("No model name given ") 
                model = input("Enter a model name = ").capitalize()

            if not is_empty:
                return model 
            

    def manufacturing_year_validator(self,manu_year):
        while True : 
            if manu_year == "":
                print("No manufacturing year given ")
                manu_year = input("Enter manufacturing year again = ")
                continue

            if not manu_year.isdigit() :
                print("Invalid input ")
                manu_year = input("Enter correct format manufacturing year =  ")
                continue 

            if  int(manu_year) <= 0 :
                print("Invalid input")
                manu_year = input("Enter the manufacturing year again = ")
                continue

            if len(manu_year) < 4: 
                print("Invalid input ")
                manu_year = input("Enter the manuffacturing year again ")
                continue 
            if int(manu_year) < 2000:
                print("We do not have manufacturing year less than 2000")
                manu_year = input("Enter manufacturing year again = ")
                continue

            if int(manu_year) > 2026 :
                print("The latest manufacturing model that we have is 2026")
                manu_year = input("Enter the manufacturing year again = ")
                continue

            return manu_year
  

    
                

    def rental_price_validator(self,rental_price):
        while True :
            if rental_price == "":
                print("Rental price cannot be empty ")
                rental_price = input("Enter the rental price again = ")
                continue
            if  not rental_price.isdigit():
                print("The input you wrote is not digit ")
                rental_price = input("Enter rental price again = ")
                continue
            if int(rental_price) <=0:
                print("Rental price cannot be negative or zero ")
                rental_price = input("Enter rental price again = ")
                continue
            return rental_price


            

    def type_validator(self,type):
        while True :
            correct_type = False 
            is_empty = False 
            is_string = True 

            if type == "":
                print("Empty input ")
                type = input("Enter the type of vehicle again = ").capitalize()
                continue
            if not type.isalpha():
                print("Enter correct input format ")
                type = input("Enter the type of vehicle again = ").capitalize()
                continue

            if type in ["Bike","Motorcycle","Car","Truck"]:
                correct_type = True 

            if  not correct_type:
                print("The type of vehicle chosen is not rented by us ")
                type = input("Enter the type of vehicle again = ").capitalize()
                continue

            if not is_empty and is_string and correct_type:
                return type 



    def view_all_vehicle(self):
        count = 1 
        for vehicle in self.data_base_of_vehicles:
            print("===========================================")
            print(f"{count}. Vehicle")
            print(f"vehicle_id = {vehicle.vehicle_id}")
            print(f" brand = {vehicle.brand}")
            print(f" model = {vehicle.model}")
            print(f" manufacturing_year = {vehicle.manufacturing_year}")
            print(f"rental price = {vehicle.rental_price}")
            print(f"type = {vehicle.type_of_vehicle}")
            print(f"avilability status = {vehicle.availabilty_status}")
            print("==============================================")
            count +=1 
            

    def register_a_new_customer(self):
        print("=============== New Customer ==========================")
        customer_data = {"customer_name":"",
                         "phone_number":"",
                         "address":""
        }
        customer_data["customer_name"] = input("Enter your name = ").capitalize()
        name = customer_data["customer_name"]
        name = self.name_validator(name)
        customer_data["address"] = input("Enter address = ").strip().capitalize()
        address = customer_data["address"]
        address = self.address_validator(address)
        customer_data["phone_number"] = input("Enter phone number = ")
        phone_number = customer_data["phone_number"]
        phone_number = self.phone_number_validator(phone_number)
        register = self.register_validator(phone_number)
        if not register:
            print("User already exists Try loggin in !")
            self.login_a_customer()
                        
        if register:
            customer_id = self.unique_customer_id()
            one_customer = Customer(customer_id,name,phone_number,address)
            self.data_base_of_customers.append(one_customer)
            print(f"You have  been sucessfully registerd {name}!")
            print(f"Your customer id is = {customer_id}")


    def register_validator(self,phone_number):
        duplicate = False 
        for account in self.data_base_of_customers:
            if phone_number == account.phone_number:
                duplicate = True 

        if duplicate :
            return False 

        if not duplicate:
            return True 
        

    def login_a_customer(self):
        print("=============== Old customer ========================")
        id = input("Enter your customer id = ")
        id = self.customer_id_validator(id)
        name = input("Enter your name = ").capitalize()
        name = self.name_validator(name)
        address = input("Enter your address = ").strip().capitalize()
        address = self.address_validator(address)
        number = input("Enter phone number = ")
        number = self.phone_number_validator(number)
        self.login_validator(id,name,address,number)
    

    def login_validator(self,id,name,address,number):
        while True :
            id_found = False 
            name_found = False 
            address_found = False 
            number_found = False 

            for account in self.data_base_of_customers:
                if id == account.customer_id:
                    id_found = True 

                if name == account.full_name:
                    name_found = True 

                if number == account.phone_number:
                    number_found = True 

                if address == account.address:
                    address_found = True 

            if id_found and name_found and address_found and number_found:
                print("Sucessfully logged in !")
                return 

            if not id_found :
                print("No such user has been registered with that customer id  ")
                id = input("Enter your customer id again = ")
                id = self.customer_id_validator(id)
                continue

            if not name_found:
                print("No such user has been registered with that name ")
                name = input("Enter your name again = ").capitalize()
                name = self.name_validator(name)
                continue

            if not address_found:
                print("No such user has registered with such address ")
                address = input("Enter your address again = ").strip().capitalize()
                address = self.address_validator(address)
                continue

            if not number_found:
                print("No such user has registered with such phone number ")
                number = input("Enter your number again = ")
                number = self.phone_number_validator(number)
                continue
                

        
    def unique_customer_id(self):
        Rental_system.customer_count += 1  
        return Rental_system.customer_count

    def name_validator(self,name):
        while True :
            if name == "":
                print("No name input ")
                name = input("Enter your name again = ")
                continue

            if not name.isalpha():
                print("Invalid input ")
                name = input("Enter your name again = ")
                continue
            
            if len(name)<3:
                print("Not enough characters")
                name = input("Enter your name again = ")
                continue

            return name 

    def phone_number_validator(self,phone_number):
        while True :
            is_empty = True 
            is_digit = False 
            starts_with_correct_format = False 
            has_correct_amount_of_numbers = False 
            if phone_number != "":
                is_empty = False 
            if phone_number.isdigit():
                is_digit = True 
            if phone_number.startswith("9"):
                starts_with_correct_format = True 
            if len(phone_number) == 10 :
                has_correct_amount_of_numbers = True 
            if not is_empty and is_digit and starts_with_correct_format and has_correct_amount_of_numbers:
                return phone_number
            print("Invalid number ")
            phone_number = input("Enter the phone number again = ")

        

    def address_validator(self,address):
        while True :
            if address == "":
                print("Adress cannot be empty")
                address = input("Enter address again = ").strip()
                continue

            if  not address.isalpha():
                print("Invalid input ")
                address = input("Enter your address again =").strip()
                continue

            if len(address) < 3 :
                print("Too short address ")
                address = input("Enter your address again = ").strip()
                continue

            return address



    def view_only_avilable_vehicles(self):
        print("============= All THE AVILABLE VEHICLES  =====================")
        for vehicle in self.data_base_of_vehicles:
            if vehicle.availabilty_status == "Avilable":
                vehicle.display_vehicle()
        print("===============================================================")

    def view_rented_vehicles_only(self):
        print("======== ALL THE RENTED VEHICLES ============================== ")         
        for vehicle in self.data_base_of_vehicles:
            if vehicle.availabilty_status == "Rented":
                vehicle.display_vehicle()
        print("================================================================")

    def search_a_vehicle(self):
        type_of_vehicle_to_search = input("Enter the type of vehicle to search = ")
        type_of_vehicle_to_search = self.type_validator(type_of_vehicle_to_search)
        brand_of_vehicle_to_search = input("Enter the brand of vehicle to search =  ")
        brand_of_vehicle_to_search = self.brand_validator(brand_of_vehicle_to_search)
        manufacturing_year_to_search = input("Enter the manfucaturing year of the vehicle = ")
        manufacturing_year_to_search = self.manufacturing_year_validator(manufacturing_year_to_search)
        model_to_search = input("Enter the model of vehicle to search = ")
        model_to_search = self.model_name_validator(model_to_search)
        vehicle_exists = False
        found_vehicle = None
        for vehicle in self.data_base_of_vehicles:
            if vehicle.type_of_vehicle == type_of_vehicle_to_search and vehicle.brand == brand_of_vehicle_to_search and vehicle.model == model_to_search and vehicle.manufacturing_year == manufacturing_year_to_search:
                    vehicle_exists = True
                    found_vehicle = vehicle
        if  vehicle_exists:
            print("Vehicle has been sucessfully found ")
            found_vehicle.display_vehicle()
        elif not vehicle_exists:
            print("No such vehicle has been found ")



    def unique_rental_id(self):
        temp = Rental_system.rental_count + 1 
        new_value = "R" + str(temp)
        return new_value

    def customer_id_validator(self,customer_id):
        while True :
            correct_input = True 
            if customer_id == "" or not customer_id.isdigit():
                correct_input = False 
            if not correct_input:
                print("invalid input ")
                customer_id = input("Enter your customer id again = ")
                continue
            if correct_input:
                return int(customer_id)
    

    
    def rent_a_vehicle(self):
        self.view_only_avilable_vehicles()
        customer_id = input("Enter your customer ID = ")
        customer_id = self.customer_id_validator(customer_id)
        customer = None

        for existing_customer in self.data_base_of_customers:
            if existing_customer.customer_id == customer_id:
                customer = existing_customer
                break

        if customer is None:
            print("No customer with that ID exists.")
            return


        # 3. Get vehicle search information
        vehicle_type = input(
        "Enter the type of vehicle that you want to rent = ").capitalize().strip()
        vehicle_type = self.type_validator(vehicle_type)

        brand = input(
        "Enter the brand of vehicle that you want to rent = ").capitalize()
        brand = self.brand_validator(brand)

        manufacturing_year = input(
        "Enter the manufacturing year = ")
        manufacturing_year = self.manufacturing_year_validator(
        manufacturing_year)

        model = input(
        "Enter the model of vehicle that you want to rent = ").capitalize()
        model = self.model_name_validator(model)

        # 4. FIND the existing vehicle object
        one_vehicle = None

        for vehicle in self.data_base_of_vehicles:

            if (
            vehicle.type_of_vehicle == vehicle_type
            and vehicle.brand == brand
            and vehicle.manufacturing_year == manufacturing_year
            and vehicle.model == model
            and vehicle.availabilty_status == "Avilable"):
                one_vehicle = vehicle
                break

        # 5. If no matching vehicle was found
        if one_vehicle is None:
            print("No available vehicle matching your requirements was found.")
            return

        # 6. Ask how many days
        days_to_rent = input("Enter the amount of days to rent = ")
        days_to_rent = self.days_validator(days_to_rent)

        # 7. Get rental price FROM THE ACTUAL VEHICLE OBJECT
        rental_price = one_vehicle.rental_price

        # 8. Create rental
        rental_id = self.unique_rental_id()

        one_rented_vehicle = Rental(
        rental_id,
        days_to_rent,
        one_vehicle,
        customer
        )

        # 9. Store rental
        self.data_base_of_rentals.append(one_rented_vehicle)

        # 10. Change the actual vehicle object's status
        one_vehicle.availabilty_status = "Rented"

        # 11. Calculate cost
        rental_cost = self.calculate_rental_cost(
        one_vehicle,
        days_to_rent)

        print("==============================================")
        print(f"Rental ID = {one_rented_vehicle.rental_id}")
        print(f"Vehicle ID = {one_vehicle.vehicle_id}")
        print(f"Vehicle = {one_vehicle.brand} {one_vehicle.model}")
        print(f"Rental days = {days_to_rent}")
        print(f"Rental price per day = {rental_price}")
        print(f"Total rental cost = {rental_cost}")
        print("Vehicle successfully rented!")
        print("==============================================")



    def days_validator(self,days_to_rent):
        while True :
            if days_to_rent == "":
                print("Empty input ")
                days_to_rent = input("Enter days to rent again = ")
                continue

            if not days_to_rent.isdigit():
                print("invalid input ")
                days_to_rent = input("Enter days to rent again = ")
                continue

            if int(days_to_rent) <= 0:
                print("Wrong input ")
                days_to_rent = input("Enter the days to rent again = ")
                continue

            return days_to_rent


    def view_rental_info(self):
        for rental in self.data_base_of_rentals:
            print(rental.display_rental())

    def calculate_rental_cost(self,one_vehicle,days_to_rent):
        if one_vehicle.type_of_vehicle  in ["Bike","Motorcycle"] :
            rental_cost = int(one_vehicle.rental_price) * int(days_to_rent)
        elif one_vehicle.type_of_vehicle in ["Car"]:
            rental_cost = int(one_vehicle.rental_price) * int(days_to_rent)
        elif one_vehicle.type_of_vehicle in ["Truck"] :
            rental_cost = int(one_vehicle.rental_price) * int(days_to_rent)
        print(f"The rental cost will be {rental_cost}")
        return rental_cost

    def rental_id_validator(self,rental_id):
        while True:
            if rental_id == "" or not rental_id.startswith("R") or not rental_id.isalnum() or len(rental_id) <= 1     :
                print("Invald Rental id ")
                rental_id = input("Enter your Rental Id again = ").capitalize()
                continue
            return rental_id



    def return_a_vehicle(self):

        rental_id = input("Enter your rental ID = ").capitalize()
        rental_id = self.rental_id_validator(rental_id)

        one_rented_vehicle = None

        # Find the existing Rental object
        for rental in self.data_base_of_rentals:
            if rental.rental_id == rental_id:
                one_rented_vehicle = rental
                break

        # Rental doesn't exist
        if one_rented_vehicle is None:
            print("No such rental was found.")
            return

        # 1. Display rental details FIRST
        one_rented_vehicle.display_rental()

        # 2. Get the actual Vehicle object
        vehicle = one_rented_vehicle.rented_vehicle_details

        # 3. Return the vehicle
        vehicle.availabilty_status = "Avilable"

        print(f"{vehicle.brand} {vehicle.model} has been successfully returned.")
       
    def view_all_customer(self):
        for customer in self.data_base_of_customers:
            print(customer.display_customer())

    def search_a_customer(self):
        name_of_customer_to_search = input("Enter the name of customer to search = ")
        name_of_customer_to_search = self.name_validator(name_of_customer_to_search)
        address_of_customer_to_search = input("Enter the address of customer to search = ")
        address_of_customer_to_search = self.address_validator(address_of_customer_to_search)
        while True :
            customer_exists = False 
            customer_data = None 
            for customer in self.data_base_of_customers:
                if customer.full_name == name_of_customer_to_search and customer.address == address_of_customer_to_search:
                    customer_exists = True 
                    customer_data = customer

            if  customer_exists :
                print("Customer has been sucesfully found ")
                customer_data.display_customer()
                return

            if not customer_exists:
                print("No such customer has been registered ")
                name_of_customer_to_search = input("Enter the name of customer to search = ")
                name_of_customer_to_search = self.name_validator(name_of_customer_to_search)
                address_of_customer_to_search = input("Enter the address of customer to search = ")
                address_of_customer_to_search = self.address_validator(address_of_customer_to_search)
                continue 
                
        
# stores infromation of the rented vehicle 
class Rental:
    def __init__(self,rental_id,rental_days,rented_vehicle_details = None,renting_customer_details = None):
        self.rental_id = rental_id
        self.rental_days = rental_days

        if rented_vehicle_details == None:
            self.rented_vehicle_details = []
        else :
            self.rented_vehicle_details = rented_vehicle_details
        if renting_customer_details == None:
            self.renting_customer_details = []
        else :
            self.renting_customer_details = renting_customer_details
        
    def display_rental(self):
        print("========================================")
        print(f"rental id = {self.rental_id}")
        self.renting_customer_details.display_customer()
        self.rented_vehicle_details.display_vehicle()
        print(f"rental days = {self.rental_days}")
        print("=======================================")

    def to_dict(self):
        rental_dictonary = {"rental id":self.rental_id,
                            "rental customer details":self.renting_customer_details.to_dict(),
                            "rented vehicle details ":self.rented_vehicle_details.to_dict(),
                            "rental days":self.rental_days
        }

        return rental_dictonary



# this stores all the info of customer only contact details location etc 
class Customer:
    def __init__(self,customer_id,full_name,phone_number,address):
        self.customer_id = customer_id
        self.full_name = full_name
        self.phone_number = phone_number
        self.address = address


    def display_customer(self):
        print("=======================================================")
        print(f"Customer id = {self.customer_id}")
        print(f"name = {self.full_name}")
        print(f"phone number = {self.phone_number}")
        print(f"address = {self.address}")
        print("=======================================================")

    def to_dict(self):
        customer_dictonary = {"customer id":self.customer_id,
                              "name":self.full_name,
                              "phone number":self.phone_number,
                              "address":self.address
        }
        return customer_dictonary

        
    


#---------------------------MENU----------------------------------------#
main_menu_list = ["1) Admin ", "2) Customer ", "3) Exit "]
admin_menu_list = ["1) Add vehicle","2) Search vehcile ","3) Display all vehicle ", "4) Search customer ", "5) Display all customers","6) Display aviailable vehicles","7) Display rented vehicles","8) Display all rentals ","9) Back"]
customer_menu_list = ["1) Rent a vehicle ", "2) Return a vehicle ", "3) Back "]
customer_login_or_register = ["1) Register (New customer) ", "2) Login (Already Registerd)", "3) Exit "]


def login_or_register():
    print("=========================================")
    for options in customer_login_or_register:
        print(options)
    print("========================================")



def login_or_register_identfier(choice,rental_system):
    if choice in ["1", "Register"]:
        rental_system.register_a_new_customer()
    elif choice in ["2","Login"]:
        rental_system.login_a_customer()


def choice_validator(choice):
    while True :
        is_empty = False 
        picked_correct_option = False 

        if choice == "":
            is_empty = True 

        if choice == "1" or choice == "2" or choice == "Register" or choice =="Login" or choice == "3" or choice == "Exit":
            picked_correct_option = True 

        if  not is_empty and picked_correct_option:
            return choice

        if is_empty:
            print("Empty input given")
            choice = input("Enter correct choice = ").capitalize()
            continue

        if not picked_correct_option:
            print("Invalid choice")
            choice = input("Enter correct choice = ").capitalize()
            continue




def name_of_customer_validator(name_of_customer):
    while True :
        if name_of_customer == "" or not name_of_customer.isalpha() or len(name_of_customer) <2 :
            print("Invalid input ")
            name_of_customer = input("Enter name again = ")
            continue
        return name_of_customer


def password_of_customer_validator(password_of_customer):
    while True :
        if password_of_customer == "" or not password_of_customer.isalnum() or len(password_of_customer) <=7:
            print("Invalid password it must be at least 8 characters and contain number and alphabet")
            password_of_customer = input("Enter password again = ")
            continue
        return password_of_customer


def name_of_admin_validator(name_of_admin):
    while True:
        names_of_admin = ["Ram"]
        is_empty = True
        is_alphabet = False 
        enough_characters = False 
        in_names_of_admin = False 
        if name_of_admin != "":
            is_empty = False
        if name_of_admin.isalpha():
            is_alphabet = True 
        if len(name_of_admin) > 2:
            enough_characters = True 
        if name_of_admin in names_of_admin:
            in_names_of_admin = True 

        if not is_empty and is_alphabet and enough_characters and in_names_of_admin :
            print("Verified admin name")
            return name_of_admin
        
        if is_empty :
            print("No name given")
            name_of_admin = input("Enter the name of admin again = ").capitalize()
            continue

        if not is_alphabet:
            print("Invalid name of admin")
            name_of_admin = input("Enter the name of admin again = ").capitalize()
            continue

        if not enough_characters:
            print("Not enough characters")
            name_of_admin = input("Enter the name of admin again = ").capitalize()
            continue

        if name_of_admin != "Ram" :
            print("No such admin name exists!")
            name_of_admin = input("Enter then name of admin again = ").capitalize()
            continue

        
            
def password_of_admin_validator(password_of_admin):
    while True:
        is_empty = True 
        correct_password = False 
        if password_of_admin != "":
            is_empty = False 
        if password_of_admin == "Ram@1234":
            correct_password = True
        if not is_empty and correct_password:
            print("Password has been verified ")
            return password_of_admin
        if  is_empty:
            print("password cannot be empty")
            password_of_admin = input("Enter password again = ")
            continue
        if not correct_password:
            print("Incorrect password!")
            password_of_admin = input("Enter password again = ")
        

def customer_menu():
    print("==================   CUSTOMER MENU    =======================")
    for customer_menu in customer_menu_list:
        print(customer_menu)
    print("=============================================================")



def admin_menu():
    print("==============================================")
    print("                 Admin menu                     ")
    for menu in admin_menu_list:
        print(menu)
    print("===============================================")



def customer_menu_identifier(customer_menu_task,rental_system):
    if customer_menu_task in ["1" ,"Rent a vehicle"]:
        rental_system.rent_a_vehicle()
    if customer_menu_task in ["2" ,"Return a vehicle"]:
        rental_system.return_a_vehicle()


def admin_menu_identifier(admin_menu_task,rental_system):
    if admin_menu_task in ["1","Add vehicle"]:
        rental_system.add_vehicle()
    if admin_menu_task in ["2", "Search vehicle"]:
        rental_system.search_a_vehicle()
    if admin_menu_task in ["3","Display all vheicle"]:
        rental_system.view_all_vehicle()
    if admin_menu_task in ["4", "Search customer"]:
        rental_system.search_a_customer()
    if admin_menu_task in ["5","Display all customers"]:
        rental_system.view_all_customer()
    if admin_menu_task in ["6","Display avilabe vehicles"]:
        rental_system.view_only_avilable_vehicles()
    if admin_menu_task in ["7","Display rented vehicles"]:
        rental_system.view_rented_vehicles_only()
    if admin_menu_task in ["8","Display all rentals"]:
        rental_system.view_rental_info()
   

def main_menu_identfier(main_menu_task,rental_system):
    if main_menu_task in ["Admin", "1"]:
        print("=========================ADMIN=================================")
        name_of_admin = input("Enter admin name = ").capitalize()
        name_of_admin = name_of_admin_validator(name_of_admin)
        password_of_admin = input("Enter the password of admin = ")
        password_of_admin = password_of_admin_validator(password_of_admin)
        while True :
            admin_menu()
            admin_menu__task = input("Enter task = ").capitalize()
            admin_menu_identifier(admin_menu__task,rental_system)
            if admin_menu__task in ["9","Back"]:
                print("Logged out of admin account Mr.Ram")
                break


    if main_menu_task in ["Customer","2"]:
        print("============================ CUSTOMER =======================================")
        login_or_register()
        choice = input("Enter your choice = ").capitalize()
        choice = choice_validator(choice)
        login_or_register_identfier(choice,rental_system)
        while True:
            customer_menu()
            customer_menu_task = input("Enter task = ").capitalize()
            customer_menu_identifier(customer_menu_task,rental_system)
            if customer_menu_task in ["3", "Exit"]:
                print(f"Logged out !")
                break 


def main_menu():
    print("===========================================")
    print("        VEHICLE RENTAL SYSTEM ")
    for menu in main_menu_list:
        print(menu)
    print("===========================================")


def save_in_file():
    with open ("Vehicle_rent.json","w") as f:
        json.dump(rental_system.to_dict(),f)


rental_system = Rental_system()
rental_system.load_data()

while True :
    
    main_menu()
    main_menu_task = input("Enter your role  = ").capitalize()
    main_menu_identfier(main_menu_task,rental_system)
    if main_menu_task in ["Exit","3"]:
        save_in_file()
        print("Have a great day !")
        break 



