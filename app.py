import streamlit as st

class Vehicle:
    total_rented_count = 0  # Class variable to keep track of total vehicles rented

    def __init__(self, vehicle_id, brand, model, year, rental_rate_per_day):
        self.vehicle_id = vehicle_id
        self.brand = brand 
        self.model = model
        self.year = year
        self.rental_rate_per_day = rental_rate_per_day
        self.is_avaliable = True

    def display_info(self):
        if self.is_avaliable:
            avaliablity = "Available"
        else:
            avaliablity = "Not Available"
        return f"Vehicle ID: {self.vehicle_id}\nBrand: {self.brand}\nModel: {self.model}\nYear: {self.year}\nRental Rate per Day: {self.rental_rate_per_day}\nStatus: {avaliablity}"

    def rent_vehical(self):
        if self.is_avaliable:
            self.is_avaliable = False
            Vehicle.total_rented_count += 1
            return True
        return False

    def return_vehicle(self):
        self.is_avaliable = True

    def calculate_rental_cost(self, days):
        return self.rental_rate_per_day * int(days)

    @classmethod
    def get_total_rented_count(cls):
        return cls.total_rented_count


class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, rental_rate_per_day, seats, fuel_type):
        super().__init__(vehicle_id, brand, model, year, rental_rate_per_day)
        self.seats = seats
        self.fuel_type = fuel_type

    def display_info(self):
        base_info = super().display_info()
        return f"Car: {base_info}\nSeats: {self.seats}\nFuel Type: {self.fuel_type}"


class Bike(Vehicle): 
    def __init__(self, vehicle_id, brand, model, year, rental_rate_per_day, engine_cc, helmet_required):
        super().__init__(vehicle_id, brand, model, year, rental_rate_per_day)
        self.engine_cc = engine_cc
        self.helmet_required = helmet_required

    def display_info(self):
        base_info = super().display_info()
        return f"Bike: {base_info}\nEngine CC: {self.engine_cc}\nHelmet Required: {self.helmet_required}"


class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.__email = email  # Private attribute
        self.rented_vehicles = []  # List to keep track of rented vehicles

    def get_email(self):
        return self.__email

    def set_email(self, updated_email):
        self.__email = updated_email

    def rent_vehicle(self, vehicle, days=1):
        if vehicle.is_avaliable and vehicle.rent_vehical():
            self.rented_vehicles.append(vehicle)
            return True
        return False

    def return_vehicle(self, vehicle_id):
        for vehicle_item in self.rented_vehicles:
            if vehicle_item.vehicle_id == vehicle_id:
                vehicle_item.return_vehicle()
                self.rented_vehicles.remove(vehicle_item)
                return True
        return False


class RentalSystem:
    def __init__(self):
        self.vehicles = {}
        self.customers = {}

    def add_vehicle(self, vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer

    def search_avaliable_vehicle(self):
        return [veh for veh in self.vehicles.values() if veh.is_avaliable]

    def show_all_vehicles(self):
        return [veh for veh in self.vehicles.values() if not veh.is_avaliable]


## STREAMLIT USER INTERFACE

st.title('Green Wheels Vehicle Rental System')

# Initialize central rental system instance in session state
if 'branch_system' not in st.session_state:
    branch = RentalSystem()

    # Sample vehicles and customers
    sample_car = Car(vehicle_id='V001', brand="Maruti", model="Swift Dzire", year=2022, rental_rate_per_day=1500, seats=5, fuel_type="Petrol")
    sample_bike = Bike(vehicle_id='V002', brand="Royal Enfield", model="Himalaya", year=2022, rental_rate_per_day=800, engine_cc=350, helmet_required=True)

    branch.add_vehicle(sample_car)
    branch.add_vehicle(sample_bike)

    sample_customer = Customer(customer_id='C101', name="Gaurav Gupta", email="gaurav@gmail.com")
    branch.add_customer(sample_customer)

    st.session_state.branch_system = branch

branch_system = st.session_state.branch_system

# Sidebar for navigation
menu_options = [
    '1.Add Vehicle', 
    '2.Add Customer', 
    '3.Rent Vehicle', 
    '4.Return a Vehicle', 
    '5.Show available Vehicles', 
    '6.Show Rented Vehicles', 
    '7.show total rentals', 
    '8.Calculate Rental Cost'
]

selected_action = st.sidebar.selectbox('Select Action', menu_options)

# Option 1: Add Vehicle
if selected_action == '1.Add Vehicle':
    st.subheader('Add Vehicle')
    vehicle_category = st.radio('Vehicle Category', ['Car', 'Bike'], horizontal=True)

    vehicle_id = st.text_input('Vehicle ID (eg: V001)')
    brand_name = st.text_input('Brand (eg: Toyota,TVs)')
    model_name = st.text_input('Model (eg: Creta,Appache)')
    manufacture_year = st.number_input('Manufacture Year', min_value=2000, max_value=2026)
    daily_rate = st.number_input('Rental Rate per Day', min_value=100, max_value=1000, step=50)

    if vehicle_category == 'Car':
        seat_capacity = st.number_input('Seats', min_value=2, max_value=10, value=5)
        fuel_choice = st.selectbox('Fuel Type', ['Petrol', 'Diesel', 'Electric'])

        if st.button('Register Car'):
            if vehicle_id and brand_name and model_name:
                new_car = Car(vehicle_id, brand_name, model_name, manufacture_year, daily_rate, seat_capacity, fuel_choice)
                branch_system.add_vehicle(new_car)
                st.success(f'Car {vehicle_id} added successfully.')
            else:
                st.warning('Please fill in Vehicle Id, Brand, and Model.')

    else:
        engine_cc = st.number_input('Enter (CC)', min_value=50, max_value=1500, value=150)
        helmet_rule = st.checkbox('Helmet Compulsory', value=True)

        if st.button('Register Bike'):
            if vehicle_id and brand_name and model_name:
                new_bike = Bike(vehicle_id, brand_name, model_name, manufacture_year, daily_rate, engine_cc, helmet_rule)
                branch_system.add_vehicle(new_bike)
                st.success(f'Bike {vehicle_id} added Successfully.')
            else:
                st.warning('Please fill in Vehicle_id, Brand and Model.')

# Option 2: Add Customer
elif selected_action == '2.Add Customer':
    st.subheader('Register New Customer')
    customer_id = st.text_input('Customer Id(eg: C102)')
    customer_name = st.text_input('Full Name')
    customer_mail = st.text_input('Email Address')

    if st.button("Register Customer"):
        if customer_id and customer_name and customer_mail:
            new_customer_obj = Customer(customer_id, customer_name, customer_mail)
            branch_system.add_customer(new_customer_obj)
            st.success(f'Customer {customer_name} registered Successfully.')
        else:
            st.warning('Please Enter all Details')

# Option 3: Rent Vehicle
elif selected_action == '3.Rent Vehicle':
    st.subheader('Issue Vehicle Rent')
    available_fleet = branch_system.search_avaliable_vehicle()
    registered_customer = list(branch_system.customers.values())

    if available_fleet and registered_customer:
        vehicle_selector_map = {f"{v.vehicle_id} - {v.brand} {v.model}": v for v in available_fleet}
        customer_selector_map = {f"{c.customer_id} - {c.name}": c for c in registered_customer}

        selected_vehicle_label = st.selectbox('Select Avaliable Vehicle', list(vehicle_selector_map.keys()))
        select_customer_label = st.selectbox('Select Customer', list(customer_selector_map.keys()))

        if st.button('Confirm Rentel Booking'):
            chosen_customer = customer_selector_map[select_customer_label]
            chosen_vehicle = vehicle_selector_map[selected_vehicle_label]

            if chosen_customer.rent_vehicle(chosen_vehicle):
                st.success(f"{chosen_vehicle.brand} {chosen_vehicle.model} successfully rented to {chosen_customer.name}!")
            else:
                st.error("Booking failed: Vehicle is not avaliable.")
    else:
        st.warning('No vehicle avaliable for rent or no customer registered.')

# Option 4: Return a Vehicle
elif selected_action == '4.Return a Vehicle':
    st.subheader('Return Rented Vehicle')
    customer_with_rental = [cust for cust in branch_system.customers.values() if len(cust.rented_vehicles) > 0]

    if customer_with_rental:
        returning_customer_map = {f'{cust.customer_id}-{cust.name}': cust for cust in customer_with_rental}
        selected_ret_cust_label = st.selectbox('Select Customer', list(returning_customer_map.keys()))
        returning_cust_obj = returning_customer_map[selected_ret_cust_label]

        rented_vehicles_map = {f"{v.vehicle_id} - {v.brand} {v.model}": v.vehicle_id for v in returning_cust_obj.rented_vehicles}
        selected_ret_veh_label = st.selectbox("Select Vehicle to Return", list(rented_vehicles_map.keys()))

        if st.button("Process Return"):
            target_vehicle_id = rented_vehicles_map[selected_ret_veh_label]
            if returning_cust_obj.return_vehicle(target_vehicle_id):
                st.success(f"Vehicle {target_vehicle_id} returned back to available fleet!")
            else:
                st.error("Failed to return vehicle.")
    else:
        st.info('No vehicle are currently out on rent.')

# Option 5: Show available Vehicles
elif selected_action == '5.Show available Vehicles':
    st.subheader('Avaliable Vehicle Fleet')
    available_fleet = branch_system.search_avaliable_vehicle()

    if available_fleet:
        for vehicle_item in available_fleet:
            st.write(vehicle_item.display_info())
    else:
        st.info('No vehicle currently avaliable')

# Option 6: Show Rented Vehicles
elif selected_action == '6.Show Rented Vehicles':
    st.subheader("Currently Rented Vehicles")
    rented_fleet = branch_system.show_all_vehicles()
    if rented_fleet:
        for vehicle_item in rented_fleet:
            st.write(vehicle_item.display_info())
    else:
        st.info("All vehicles are currently available (None rented).")

# Option 7: Show total rentals
elif selected_action == '7.show total rentals':
    st.subheader("System Rental Statistics")
    st.write(f"Total vehicle rentals tracked across fleet: **{Vehicle.get_total_rented_count()}**")

# Option 8: Calculate Rental Cost
elif selected_action == '8.Calculate Rental Cost':
    st.subheader("Rental Cost Estimation")
    if branch_system.vehicles:
        all_vehicles_map = {f"{v.vehicle_id} - {v.brand} {v.model} (Rs. {v.rental_rate_per_day}/day)": v for v in branch_system.vehicles.values()}
        selected_calc_label = st.selectbox("Select Vehicle", list(all_vehicles_map.keys()))
        rental_duration = st.number_input("Rental Days", min_value=1, value=2)

        if st.button("Calculate Cost"):
            estimated_cost = all_vehicles_map[selected_calc_label].calculate_rental_cost(rental_duration)
            st.success(f"Total Estimated Rent for {rental_duration} day(s): Rs. {estimated_cost:,.2f}")
    else:
        st.info("No vehicles registered in the system.")
