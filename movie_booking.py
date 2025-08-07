import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import time


# DatabaseHandler class to handle all database operations
class DatabaseHandler:
    def __init__(self):
        try:
            # Create a connection to the database and set up the cursor
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='movie_booking'
            )
            self.cursor = self.connection.cursor()

            self.user = {}  # Instance variable to store user data
            self.mobile_numbers = []  # Instance variable to store mobile numbers
            self.movie_dict = {}
            self.city_dict={}
            self.theater_dict={}

        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def fetch_user_data(self):
        try:
            self.user.clear()  
            self.mobile_numbers.clear()  
            self.cursor.execute("SELECT user_id, password, mobile_no, role FROM users")  
            data = self.cursor.fetchall()  
            for i in data:
                self.user[i[0]] = {"password": i[1], "role": i[3]}
                self.mobile_numbers.append(i[2])
        except mysql.connector.Error as e:
            print(f"Error fetching user data: {e}")

    def fetch_movieshow_data(self):
        try:
            self.movie_dict.clear()  
            self.cursor.execute("SELECT entry_key,city,theater_name,movie_name FROM movieshowtimes") 
            data = self.cursor.fetchall() 
            
            for i in data:
                entry_key = i[0]  
                city_fetch_name=i[1]
                theater_fetch_name=i[2]
                movie_fetch_name = i[3] 

                split_key = entry_key.split('-')
                
                if len(split_key) > 1:
                    city_fetch_id=split_key[0]
                    self.city_dict[city_fetch_id]=city_fetch_name
                    
                    theater_fetch_id=split_key[1]
                    self.theater_dict[theater_fetch_id]=theater_fetch_name

                    movie_fetch_id = split_key[2]
                    self.movie_dict[movie_fetch_id] = movie_fetch_name


        except mysql.connector.Error as e:
            print(f"Error fetching movie show data: {e}")

    def insert_user(self, user_id, name, password, mobile_no):
        try:
            query = "INSERT INTO users (user_id, name, password, mobile_no, role) VALUES (%s, %s, %s, %s, %s)"

            role = 'admin' if user_id == 'admin91' else 'user'
            self.cursor.execute(query, (user_id, name, password, mobile_no, role))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error inserting user data: {e}")
            self.connection.rollback()

    def close_connection(self):
        try:
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as e:
            print(f"Error closing the connection: {e}")

# Validation class validates all cases
class Validation(DatabaseHandler):

    def get_valid_mobile_no(self):
        while True:
            try:
                mobile_no = input("\nEnter your mobile number (+91): ")
                if mobile_no.isdigit() and len(mobile_no) == 10 and mobile_no[0] in '789':
                    return mobile_no
                print("\nInvalid mobile number. Please enter a valid 10-digit number starting with 7, 8, or 9.")
            except Exception as e:
                print(f"Error validating mobile number: {e}")

    def create_password(self):
        while True:
            try:
                password = input("\nCreate a pin (Enter 6 digits pin): ")
                if password.isdigit() and len(password) == 6:
                    return password
                else:
                    print("\nPlease enter 6 digit pin only.")
            except Exception as e:
                print(f"Error creating password: {e}")

    def get_unique_user_id(self,name,mobile_no):
        try:
            user_id = name[:5] + mobile_no[:2]
            while user_id in self.user:
                numeric_part = int(user_id[-2:]) + 1
                if numeric_part > 99:
                    numeric_part = 10
                user_id = name[:5] + f"{numeric_part:02d}"

            return user_id
        except Exception as e:
            print(f"Failed to generate unique user ID: {e}")


    def select_city(self):
        while True:
            try:
                cities = {'AMD': 'Ahmedabad', 'SRT': 'Surat', 'VAD': 'Vadodara'}

                print("╔════════════╦═════════════════╗")
                print("║ City Code  ║ City Name       ║")
                print("╠════════════╬═════════════════╣")
                
                for short_form, full_name in cities.items():
                    print(f"║ {short_form:<10} ║ {full_name:<15} ║")
                print("╚════════════╩═════════════════╝")
                
                city_key = input("\nEnter the city code of the city: ").upper()

                if city_key in cities:
                    city_value = cities[city_key]
                    print(f"\nYou selected: {city_value}")
                    return city_key, city_value
                else:
                    print("\nInvalid input. Please enter a valid city short form from the options above.\n")

            except Exception as e:
                print(f"An unexpected error occurred while selecting city: {e}")
        
    def select_theater(self):
        while True:
            try:
                theaters = {'TH01': 'PVR', 'TH02': 'Inox', 'TH03': 'Rajhans'}

                print("╔════════════╦════════════════╗")
                print("║ Theater ID ║ Theater Name   ║")
                print("╠════════════╬════════════════╣")
                
                for theater_id, theater_name in theaters.items():
                    print(f"║ {theater_id:<10} ║ {theater_name:<14} ║")            
                print("╚════════════╩════════════════╝") 
                theater_key = input("\nEnter the theater ID of the theater: ").upper()

                if theater_key in theaters:
                    theater_value=theaters[theater_key]
                    print(f"\nYou selected: {theater_value}")
                    return theater_key,theater_value
                else:
                    print("\nInvalid input. Please enter a valid theater ID from the options above.\n")

            except Exception as e:
                print(f"An unexpected error occurred while selecting theater: {e}")

    def select_movie_name(self):
        while True:
            try:
                movie_name = input("\nEnter the movie name: ").strip()

                movie_id = None
                for m_id, m_name in self.movie_dict.items():
                    if m_name.lower() == movie_name.lower():
                        movie_id = m_id
                        break 
                if movie_id:
                    return movie_id, movie_name

                movie_ids = [m_id for m_id in self.movie_dict.keys()]
                if movie_ids:
                    last_id = sorted(movie_ids)[-1]  
                    new_id_num = int(last_id[1:]) + 1 
                else:
                    new_id_num = 1
                movie_id = f'M{new_id_num:02d}'  
                    
                return movie_id,movie_name
            except Exception as e:
                print(f"\nAn unexpected error occurred while entering movie name: {e}. Please try again.")

    def select_genre(self):
        while True:
            genre = input("\nEnter the genre of the movie (use commas to separate multiple genres): ")
            if all(c.isalpha() or c == ',' or c ==' ' for c in genre):
                return genre
            else:
                print("\nInvalid input. Please enter a valid genre (alphabetic characters or commas).")

    def select_movie_duration(self):
        while True:
            movie_duration = input("\nEnter the movie duration (HH:MM:SS): ")
            parts = movie_duration.split(':')
            if len(parts) == 3 and all(part.isdigit() for part in parts):
                hours, minutes, seconds = parts
                if 0 <= int(hours) < 5 and 0 <= int(minutes) < 60 and 0 <= int(seconds) < 60:
                    return movie_duration
                else:
                    print("\nInvalid time. Please enter a valid movie duration (HH:MM:SS) with hours less than 5.")
            else:
                print("\nInvalid time format. Please use HH:MM:SS.")

    def select_movie_price(self):
        while True:
            try:
                movie_price = input("\nEnter the price of the movie ticket: ")
                movie_price = float(movie_price)
                if movie_price > 0:
                    return movie_price
                else:
                    print("\nInvalid input. Please enter a positive value for the movie price.")
            except ValueError:
                print("\nInvalid input. Please enter a valid number for the movie price.")
            except Exception as e:
                print(f"\nAn unexpected error occurred while entering movie price: {e}. Please try again.")

    def select_show_date(self):
        while True:
            show_date = input("\nEnter show date (YYYY-MM-DD): ")
            parts = show_date.split('-')
            if len(parts) == 3 and all(part.isdigit() for part in parts):
                year, month, day = parts
                try:
                    input_date = datetime(int(year), int(month), int(day))
                    today = datetime.now()
                    seven_days_from_now = today + timedelta(days=7)
                    if today <= input_date <= seven_days_from_now:
                        return show_date,input_date
                    else:
                        if input_date < today:
                            print("\nThe entered date is in the past. Please choose a date from today onwards.\n")
                        else:
                            print("\nThe entered date is too far in the future. Please choose a date within the next 7 days.\n")
                except ValueError:
                    print("\nInvalid date. Please enter a valid date (YYYY-MM-DD).")
            else:
                print("\nInvalid date format. Please use YYYY-MM-DD.")
 
    def select_show_time(self):
        while True:
            try:
                show_times = {'morning': '09:00:00', 'afternoon': '13:00:00', 'evening': '17:00:00', 'night': '21:00:00'}

                print("╔════════════╦═════════════════╗")
                print("║ Period     ║ Time            ║")
                print("╠════════════╬═════════════════╣")
                
                for period, time in show_times.items():
                    print(f"║ {period.capitalize():<10} ║ {time:<15} ║")
                
                print("╚════════════╩═════════════════╝")
                    
                selected_period = input("\nEnter the period (morning, afternoon, evening, night): ").lower()
                if selected_period in show_times:
                    return show_times[selected_period]
                else:
                    print("\nInvalid input. Please select a valid period.")
                
            except Exception as e:
                print(f"An unexpected error occurred while selecting show time: {e}")

    def display_seating(self,entry_key):
    
        # Fetch booked seats from bookingpayment for the selected entry_key
        self.cursor.execute("SELECT seat_numbers FROM bookingpayment WHERE entry_key = %s", (entry_key,))
        booked_seats_data = self.cursor.fetchall()
        
        booked_seats = set()
        for row in booked_seats_data:
            if row[0]:  # Check if seat_numbers is not None
                booked_seats.update(row[0].split(', '))  # Split and update the set with booked seats

        # Define rows and columns for seating
        rows = ['H','G','F','E','D','C','B','A']
        cols_part1 = [str(i) for i in range(1, 9)]
        cols_part2 = [str(i) for i in range(9, 17)]

        # Display the column numbers with proper alignment
        print("\n----- Theater Seating Layout -----")
        print()
        print("     " + "  ".join(f"{col:>2}" for col in cols_part1) + "     " + "  ".join(f"{col:>2}" for col in cols_part2))
        print()

        for row in rows:
            print(f"{row} | ", end="")
            for col in cols_part1:
                seat = f"{row}{col}"
                if seat in booked_seats:
                    print(f"  ■ ", end="")  
                else:
                    print(f"  □ ", end="")  

            print("   ", end="")  # Gap in between

            for col in cols_part2:
                seat = f"{row}{col}"
                if seat in booked_seats:
                    print(f"  ■ ", end="")  
                else:
                    print(f"  □ ", end="")  
            print()  
        print("\n      ════════════════════════════════════════════════════════════════")
        print("                           Screen this side")


        while True:
            try:
                num_seats = int(input("\nHow many seats would you like to book?  "))
                if num_seats > 0:
                    break
                else:
                    print("\nPlease enter a positive number.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")

        selected_seats = []
        for i in range(num_seats):
            while True:
                seat_number = input(f"\nEnter the seat number for seat {i + 1} (e.g., A4, B10): ").upper().strip()
                if seat_number in booked_seats:
                    print(f"\nSeat {seat_number} is already booked. Please choose a different seat.")
                elif seat_number in selected_seats:
                    print(f"\nSeat {seat_number} is already selected. Please choose a different seat.")
                elif len(seat_number) > 3 or not seat_number[:1] in rows or not seat_number[1:].isdigit():
                    print("\nInvalid seat format. Please enter a valid seat (e.g., A4, B10).")
                elif not (1 <= int(seat_number[1:]) <= 16):
                    print("\nSeat number should be between 1 and 16. Please enter a valid seat.")
                else:
                    selected_seats.append(seat_number)
                    break

        # Display selected seats
        print("\nYou have selected the following seats:", ", ".join(selected_seats))
        return num_seats,selected_seats

# AdminManagement for add,update,remove show
class AdminManagement(Validation):  
    def manage_shows(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=============================")
                print("         Manage Show")
                print("=============================")
                print("1. Add Show")
                print("2. Update Show")
                print("3. Delete Show")
                print("4. See Movie Stats")
                print("5. Exit Admin Menu")

                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.fetch_user_data()
                    self.fetch_movieshow_data()  
                    self.add_show()
                elif choice == 2:
                    self.fetch_movieshow_data()  
                    self.update_show()
                elif choice == 3:
                    self.delete_show()
                elif choice == 4:
                    self.show_movie_stats()
                elif choice == 5:
                    break
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")


    def add_show(self):
        print("\n----- City Selection -----")
        print("Please select a city for adding the movie from the following options:")
        city_key,city_value=self.select_city()

        print("\n----- Theater Selection -----")
        print("Please select a theater for adding the movie from the following options:")
        theater_key,theater_value=self.select_theater()

        movie_id,movie_name=self.select_movie_name()
        print("\nMovie ID:",movie_id)
        
        genre=self.select_genre()

        movie_duration=self.select_movie_duration()

        show_date,input_date=self.select_show_date()

        # Ask for the number of days the movie will be shown
        while True:
            num_days = input("\nEnter for how many days do you want to add movie entries for this showtime(1-7)? ")
            
            if num_days.isdigit() and 1 <= int(num_days) <= 7:
                num_days = int(num_days)
                break
            else:
                print("\nInvalid input. Please enter a number between 1 and 7.")

        print("\n----- Show Time Selection -----")
        print("Please select a show time from the following options:")
        show_time=self.select_show_time()

        movie_price = self.select_movie_price()


        available_seats=128

        # Insert multiple entries for each day
        for i in range(num_days):
            try:
                show_date_incremented = input_date + timedelta(days=i)
                formatted_date = show_date_incremented.strftime('%Y-%m-%d')

                entry_key = f"{city_key}-{theater_key}-{movie_id}-{formatted_date[2:4]+formatted_date[5:7]+formatted_date[8:]}-{show_time}"
                
                query = "SELECT * FROM movieshowtimes WHERE city=%s AND theater_name=%s AND show_date=%s AND show_time=%s"
                self.cursor.execute(query, (city_value, theater_value, formatted_date, show_time))
                result = self.cursor.fetchone()

                if result:
                    print(f"\nA show in '{theater_value}', {city_value} on {formatted_date} at {show_time} already exists.")
                    print("Please choose a different time or date for this show.")
                else:
                    insert_query = "INSERT INTO movieshowtimes (entry_key, city, theater_name, movie_name, genre, movie_duration, movie_price, show_date, show_time, available_seats, total_seats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    self.cursor.execute(insert_query, (entry_key, city_value, theater_value, movie_name, genre, movie_duration, movie_price, formatted_date, show_time, available_seats, available_seats))
                    self.connection.commit()
                    print(f"\nShow added successfully for {formatted_date}!")


            except mysql.connector.Error as e:
                print(f"\nDatabase error: {e}")
                self.connection.rollback()
            except Exception as e:
                print(f"\nAn unexpected error occurred while adding the show: {e}")

        enter = input("\nPress Enter to proceed to continue..")

    def update_show(self):
        print("\n--- City Selection ---")
        print("Please select a city from which you want to update the movie show from the following options:")
        city_key, city_value = self.select_city()

        print("\n--- Theater Selection ---")
        print("Please select a theater from which you want to update the movie show from the following options:")
        theater_key, theater_value = self.select_theater()

        current_time = datetime.now()
        two_hours_from_now = current_time + timedelta(hours=2)

        print(f"\nFetching shows for {theater_value}, {city_value}...\n")
        self.cursor.execute("SELECT entry_key, movie_name, show_date, show_time FROM movieshowtimes WHERE city=%s AND theater_name=%s AND available_seats=128 AND (show_date > %s OR (show_date = %s AND show_time >= %s)) ORDER BY show_date, show_time",(city_value, theater_value,current_time.date(), current_time.date(), two_hours_from_now.time()))
        shows = self.cursor.fetchall()


        if not shows:
            print(f"\nNo shows found for {theater_value}, {city_value}.")
            enter = input("\nPress Enter to proceed to continue..")
            return

        print("\n--- Available Shows ---")
        print("╔═══════╦═══════════════════════╦════════════╦════════════╗")
        print("║ Index ║ Movie Name            ║ Date       ║ Time       ║")
        print("╠═══════╬═══════════════════════╬════════════╬════════════╣")

        for index, (entry_key, movie_name, show_date, show_time) in enumerate(shows, 1):
            print(f"║ {index:<5} ║ {movie_name:<21} ║ {show_date.strftime('%Y-%m-%d'):<10} ║ {show_time:<10} ║")

        print("╚═══════╩═══════════════════════╩════════════╩════════════╝")



        # Ask the Admin How Many Shows to Update
        while True:
            try:
                num_to_update = int(input(f"\nEnter how many shows you want to update: "))
                if 1 <= num_to_update <= len(shows):
                    break
                else:
                    print(f"\nInvalid number. Please enter a number between 1 and {len(shows)}.")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        # Ask Admin for Specific Shows to Update
        shows_to_update = []
        for i in range(num_to_update):
            while True:
                try:
                    choice = int(input(f"\nEnter the index number of show {i + 1} you want to update: "))
                    if 1 <= choice <= len(shows):
                        selected_show = shows[choice - 1] 
                        entry_key_to_update = selected_show[0]
                        if entry_key_to_update not in shows_to_update:
                            shows_to_update.append(entry_key_to_update)
                        else:
                            print("\nYou already selected this show. Please select a different one.")
                        break
                    else:
                        print("\nInvalid choice. Please enter a valid number.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

        print("\nEnter details of the movie to update all selected shows: ")

        new_movie_id, new_movie_name = self.select_movie_name()
        new_genre = self.select_genre()
        new_movie_duration = self.select_movie_duration()

        for entry_key in shows_to_update:
            print(f"\nUpdating show with entry key: {entry_key}")

            city_key, theater_key, _, formatted_date, show_time = entry_key.split("-")

            # Initialising new entry_key
            new_entry_key = f"{city_key}-{theater_key}-{new_movie_id}-{formatted_date}-{show_time}"

            update_query = "UPDATE movieshowtimes  SET movie_name=%s, genre=%s, movie_duration=%s, entry_key=%s  WHERE entry_key=%s"

            self.cursor.execute(update_query, (new_movie_name, new_genre, new_movie_duration, new_entry_key, entry_key))
            self.connection.commit()

            print(f"\nShow with entry key {entry_key} has been updated to new entry key {new_entry_key} successfully!")

        enter = input("\nPress Enter to proceed to continue..")

    def delete_show(self):
        print("\n----- City Selection -----")
        print("Please select a city from which you want to delete the movie show from the following options:")
        city_key, city_value = self.select_city()

        print("\n----- Theater Selection -----")
        print("Please select a theater from which you want to delete the movie show from the following options:")
        theater_key, theater_value = self.select_theater()

        current_time = datetime.now()
        two_hours_from_now = current_time + timedelta(hours=2)

        print(f"\nFetching shows for {theater_value}, {city_value}...\n")
        self.cursor.execute("SELECT entry_key, movie_name, show_date, show_time FROM movieshowtimes WHERE city=%s AND theater_name=%s AND available_seats=128 AND (show_date > %s OR (show_date = %s AND show_time >= %s)) ORDER BY show_date, show_time",(city_value, theater_value,current_time.date(), current_time.date(), two_hours_from_now.time()))
        shows = self.cursor.fetchall()

        if not shows:
            print(f"\nNo shows found for {theater_value}, {city_value}.")
            enter = input("\nPress Enter to proceed to continue..")
            return

        print("\n----- Available shows -----")
        print("╔═══════╦═══════════════════════╦════════════╦════════════╗")
        print("║ Index ║ Movie Name            ║ Date       ║ Time       ║")
        print("╠═══════╬═══════════════════════╬════════════╬════════════╣")

        for index, (entry_key, movie_name, show_date, show_time) in enumerate(shows, 1):
            print(f"║ {index:<5} ║ {movie_name:<21} ║ {show_date.strftime('%Y-%m-%d'):<10} ║ {show_time:<10} ║")

        print("╚═══════╩═══════════════════════╩════════════╩════════════╝")


        # Ask the Admin How Many shows to Delete
        while True:
            try:
                num_to_delete = int(input(f"\nEnter how many shows you want to delete : "))
                if 1 <= num_to_delete <= len(shows):
                    break
                else:
                    print(f"\nInvalid number. Please enter a number between 1 and {len(shows)}.")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        # Ask Admin for Specific shows to Delete
        shows_to_delete = []
        for i in range(num_to_delete):
            while True:
                try:
                    choice = int(input(f"\nEnter the index number of show {i + 1} you want to delete: "))
                    if 1 <= choice <= len(shows):
                        selected_show = shows[choice - 1]  
                        entry_key_to_delete = selected_show[0] 
                        if entry_key_to_delete not in shows_to_delete: 
                            shows_to_delete.append(entry_key_to_delete)
                        else:
                            print("\nYou already selected this show. Please select a different one.")
                        break
                    else:
                        print("\nInvalid choice. Please enter a valid number.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

        for entry_key in shows_to_delete:
            try:
                delete_query = "DELETE FROM movieshowtimes WHERE entry_key=%s"
                self.cursor.execute(delete_query, (entry_key,))
                self.connection.commit()
                print(f"\nShow with entry key {entry_key} has been deleted successfully!")

                enter = input("\nPress Enter to proceed to continue..")

            except mysql.connector.Error as e:
                print(f"\nFailed to delete show with entry key {entry_key}. Database error: {e}")
                self.connection.rollback() 
            except Exception as e:
                print(f"\nAn unexpected error occurred while deleting show with entry key {entry_key}: {e}")
                self.connection.rollback()

    def show_movie_stats(self):
        print("\n--- Movie Hype Analysis ---")
        
        print("Select City:")
        city_key, city_value = self.select_city()
        
        print("Select Theater:")
        theater_key, theater_value = self.select_theater()

        query = " SELECT movie_name, SUM(total_seats - available_seats) AS seats_booked  FROM movieshowtimes WHERE city=%s AND theater_name=%s GROUP BY movie_name"
        self.cursor.execute(query, (city_value, theater_value))
        results = self.cursor.fetchall()

        if not results:
            print(f"\nNo showtimes found for {theater_value} in {city_value}.")
            enter = input("\nPress Enter to proceed to continue..")
            return

        movie_names = []
        seats_booked = []

        for movie_name, booked in results:
            movie_names.append(movie_name)
            seats_booked.append(booked)

        plt.figure(figsize=(10, 6))
        plt.bar(movie_names, seats_booked, color='skyblue')
        plt.xlabel('Movies', fontsize=12, color='darkgreen')
        plt.ylabel('Seats Booked (Hype)', fontsize=12, color='darkgreen')
        plt.title(f"Movie Hype in {theater_value}, {city_value}", fontsize=14, fontweight='bold', color='darkred')

        
        plt.tight_layout()
        plt.show()

        enter = input("\nPress Enter to proceed to continue..")


# UserManagement class for book,view,cancel tickets
class UserManagement(Validation):
    def __init__(self):
        super().__init__()

    def sign_up(self):
        try:
            self.fetch_user_data()  
            print("\n---------- Sign Up Page ----------")
            name = input("\nEnter your name: ")

            while True:
                mobile_no = self.get_valid_mobile_no() 
                if mobile_no in self.mobile_numbers:  
                    print("\nMobile number already exists. Please enter a different number.")
                else:
                    break  

            user_id = self.get_unique_user_id(name, mobile_no)

            print(f"\nYour User ID is: {user_id}")
            password = self.create_password()

            self.insert_user(user_id, name, password, mobile_no)
            print("\nSign Up Successful!")
            self.user_id = user_id
            return
        except Exception as e:
            print(f"Error during sign up: {e}")

    def login(self):
        try:
            self.fetch_user_data()
            print("\n---------- Login Page ----------")
            user_id = input("\nEnter your User ID: ")
            if user_id in self.user:
                password = input("Enter your Password: ")

                if user_id == "admin91" and password == "101010":
                    print("Welcome back admin!")
                    return "admin"
                elif self.user[user_id]["password"] == password:
                    print("\nLogin Successful!")
                    self.user_id = user_id 
                    return "user"
                else:
                    print("\nIncorrect Password.")
            else:
                print("\nUser doesn't exist, please Sign Up first.")
        except Exception as e:
            print(f"Error during login: {e}")

    def user_dashboard(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=============================")
                print("        User dashboard")
                print("=============================")
                print("1. Book Tickets")
                print("2. View My Bookings")
                print("3. Cancel Booking")
                print("4. View Booking History")
                print("5. See Movie Popurarity")
                print("6. Log Out")
                choice = int(input("\nEnter your choice: "))

                if choice == 1:
                    self.fetch_movieshow_data()
                    self.book_tickets()
                elif choice == 2:
                    self.view_my_bookings()
                elif choice == 3:
                    self.cancel_booking()  
                elif choice == 4:
                    self.view_booking_history()
                elif choice == 5:
                    AdminManagement.show_movie_stats(self)
                elif choice == 6:
                    print("\nLogging out...")
                    break  # Exit the user dashboard and log out
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")


    def book_tickets(self):
        try:
            print("\n--- City Selection ---")
            print("Please select a city for booking the movie from the following options:")
            city_key, city_value = self.select_city() 
            
            # Get current time and 2 hours from now
            current_time = datetime.now()
            two_hours_from_now = current_time + timedelta(hours=2)

            self.cursor.execute(" SELECT DISTINCT movie_name, genre, movie_duration FROM movieshowtimes WHERE city = %s AND (show_date > %s OR (show_date = %s AND show_time >= %s))", (city_value, current_time.date(), current_time.date(), two_hours_from_now.time()))
            
            movies = self.cursor.fetchall()
            
            if not movies:
                print(f"\nNo movies available in {city_value} at the moment ")
                enter = input("\nPress Enter to proceed to continue..")
                return
            
            print(f"\n--- Movies Available in {city_value} ---")
            print("╔═══════╦═══════════════════════╦══════════════════════╦════════════════╗")
            print("║ Index ║ Movie Name            ║ Genre                ║ Duration       ║")
            print("╠═══════╬═══════════════════════╬══════════════════════╬════════════════╣")
            
            for i, (movie_name, genre, duration) in enumerate(movies, 1):
                print(f"║ {i:<5} ║ {movie_name:<21} ║ {genre:<20} ║ {duration:<14} ║")
            
            print("╚═══════╩═══════════════════════╩══════════════════════╩════════════════╝")
            
            while True:
                try:
                    movie_choice = int(input("\nEnter the index number of the movie you want to watch: "))
                    if 1 <= movie_choice <= len(movies):
                        selected_movie = movies[movie_choice - 1][0]
                        break
                    else:
                        print(f"\nInvalid index. Please select a number between 1 and {len(movies)}.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")
            
            print(f"\nYou selected: {selected_movie}")
            
            self.cursor.execute(" SELECT DISTINCT theater_name FROM movieshowtimes WHERE city = %s AND movie_name = %s AND (show_date > %s OR (show_date = %s AND show_time >= %s))", (city_value, selected_movie, current_time.date(), current_time.date(), two_hours_from_now.time()))

            theaters = self.cursor.fetchall()

            if not theaters:
                print(f"\nNo theaters in {city_value} are showing {selected_movie} at the moment.")
                enter = input("\nPress Enter to proceed to continue..")
                return

            theater_list = []

            print(f"\n--- Theaters Showing '{selected_movie}' in {city_value} ---")
            print("╔═══════╦════════════════╗")
            print("║ Index ║ Theater Name   ║")
            print("╠═══════╬════════════════╣")

            for entry in theaters:
                theater_name = entry[0]
                if theater_name not in theater_list:
                    theater_list.append(theater_name) 
                    print(f"║ {len(theater_list):<5} ║ {theater_name:<14} ║") 

            print("╚═══════╩════════════════╝")

            while True:
                try:
                    theater_choice = int(input("\nEnter the index number of the theater: "))
                    if 1 <= theater_choice <= len(theater_list):
                        selected_theater = theater_list[theater_choice - 1]
                        break
                    else:
                        print(f"\nInvalid index. Please select a number between 1 and {len(theater_list)}.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

            print(f"\nYou selected: {selected_theater}")

            # Display available showtimes for the selected movie and theater, and include entry_key
            self.cursor.execute(" SELECT entry_key, show_date, show_time, movie_price FROM movieshowtimes WHERE city = %s AND movie_name = %s AND theater_name = %s AND (show_date > %s OR (show_date = %s AND show_time >= %s))ORDER BY show_date ASC, show_time ASC ", (city_value, selected_movie, selected_theater, current_time.date(), current_time.date(), two_hours_from_now.time()))

            showtimes = self.cursor.fetchall()

            if not showtimes:
                print(f"\nNo showtimes available for {selected_movie} at {selected_theater}.")
                enter = input("\nPress Enter to proceed to continue..")
                return

            print(f"\n--- Available Showtimes for '{selected_movie}' at {selected_theater} ---")
            print("╔═══════╦════════════╦════════════╦═══════════════╗")
            print("║ Index ║ Show Date  ║ Show Time  ║ Ticket Price  ║")
            print("╠═══════╬════════════╬════════════╬═══════════════╣")

            for i, (entry_key, show_date, show_time, movie_price) in enumerate(showtimes, 1):
                print(f"║ {i:<5} ║ {show_date.strftime('%Y-%m-%d'):<10} ║ {show_time:<10} ║ {movie_price:<13} ║")

            print("╚═══════╩════════════╩════════════╩═══════════════╝")

            while True:
                try:
                    showtime_choice = int(input("\nEnter the index number of the showtime you want to book: "))
                    if 1 <= showtime_choice <= len(showtimes):
                        selected_showtime = showtimes[showtime_choice - 1]
                        break
                    else:
                        print(f"\nInvalid index. Please select a number between 1 and {len(showtimes)}.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

            selected_entry_key = selected_showtime[0] 

            print(f"\nYou selected showtime on {selected_showtime[1]} at {selected_showtime[2]} with ticket price: ₹{selected_showtime[3]}")

            # Display Booking Method
            num_seats,selected_seats=self.display_seating(selected_entry_key)
            seat_numbers = ', '.join(selected_seats)

            ticket_price=num_seats*movie_price
            total_price=round(ticket_price+(ticket_price*0.28),2)


            # Ask for payment
            while True:
                confirm_payment = input(f"\nThe total price for {num_seats} seats is ₹{total_price} (including gst of 18% & base price of 10%). Do you want to proceed with payment (yes/no)? ").lower()
                if confirm_payment == 'yes':
                    print("\nProcessing payment...")
                    print("Payment successful. Your seats are booked!")

                    # Fetch the latest booking_id from the bookingpayment table
                    self.cursor.execute("SELECT booking_id FROM bookingpayment ORDER BY booking_id DESC LIMIT 1")
                    result = self.cursor.fetchone()

                    if result:
                        last_booking_id = result[0]
                        last_id_num = int(last_booking_id[1:])
                        new_id_num = last_id_num + 1
                    else:
                        new_id_num = 1

                    booking_id = f"B{new_id_num:02d}"


                    insert_query = "INSERT INTO bookingpayment (booking_id, user_id, entry_key, num_of_tickets, amount, seat_numbers, booking_status)VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    self.cursor.execute(insert_query, (booking_id, self.user_id, selected_entry_key, num_seats, total_price, seat_numbers, 'booked'))
                    self.connection.commit()

                    update_seats_query = "UPDATE movieshowtimes SET available_seats = available_seats - %s WHERE entry_key = %s"
                    self.cursor.execute(update_seats_query, (num_seats, selected_entry_key))
                    self.connection.commit()

                    print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
                    print("║                            Booking Confirmed!                             ║")
                    print("╠═══════════════════════════════════════════════════════════════════════════╣")
                    print(f"║ Your booking for the movie '{selected_movie}' has been successfully completed.     ║")
                    print(f"║ City: {city_value:<68}║")
                    print(f"║ Theater: {theater_name:<65}║")
                    print(f"║ Date: {selected_showtime[1].strftime('%Y-%m-%d'):<68}║")
                    print(f"║ Time: {selected_showtime[2]:<68}║")
                    print(f"║ Booking ID: {booking_id:<62}║")
                    print("╠═══════════════════════════════════════════════════════════════════════════╣")
                    print("║                             Enjoy the movie!                              ║")
                    print("╚═══════════════════════════════════════════════════════════════════════════╝")

                    break
                elif confirm_payment == 'no':
                    print("\nBooking cancelled.")
                    break
                else:
                    print("Please enter 'yes' or 'no'.")

            enter = input("\nPress Enter to proceed to continue..")

        except Exception as e:
            print(f"\nError during the movie booking process: {e}")

    def view_my_bookings(self):
        try:
            current_time = datetime.now()

            # Fetch all user bookings using JOIN
            query = " SELECT bp.booking_id, ms.movie_name, ms.city, ms.theater_name, ms.show_date, ms.show_time, bp.amount, bp.seat_numbers FROM bookingpayment bp JOIN movieshowtimes ms ON bp.entry_key =  ms.entry_key WHERE bp.user_id = %s AND booking_status = %s AND (ms.show_date > %s OR (ms.show_date = %s AND ms.show_time > %s)) "
            self.cursor.execute(query, (self.user_id, 'booked', current_time.date(), current_time.date(), current_time.time()))
            bookings = self.cursor.fetchall()

            if not bookings:
                print("\nNo future bookings found.")
                enter = input("\nPress Enter to proceed to continue..")
                return

            print(f"\n--- Bookings for User ID: {self.user_id} ---\n")
            print("╔══════╦═════════════╦══════════════════════════════╦═══════════╦═════════════╦════════════╦════════════════╦═══════════════╦═══════════════════════╗")
            print("║ No.  ║ Booking ID  ║ Movie Name                   ║ City      ║ Theater     ║ Movie Date ║ Movie Time     ║ Amount Paid   ║ Seat Numbers          ║")
            print("╠══════╬═════════════╬══════════════════════════════╬═══════════╬═════════════╬════════════╬════════════════╬═══════════════╬═══════════════════════╣")

            for i, (booking_id, movie_name, city, theater_name, show_date, show_time, amount, seat_numbers) in enumerate(bookings, 1):
                print(f"║ {i:<4} ║ {booking_id:<11} ║ {movie_name:<28} ║ {city:<9} ║ {theater_name:<11} ║ {show_date.strftime('%Y-%m-%d'):<10} ║ {show_time:<14} ║ ₹{amount:<12} ║ {seat_numbers:<21} ║")
            
            print("╚══════╩═════════════╩══════════════════════════════╩═══════════╩═════════════╩════════════╩════════════════╩═══════════════╩═══════════════════════╝")
        
            enter = input("\nPress Enter to proceed to continue..")

        except mysql.connector.Error as e:
            print(f"Error fetching bookings: {e}")

    def cancel_booking(self):
        try:
            booking_id = input("\nEnter the Booking ID of the booking you want to cancel: ").upper().strip()

            self.cursor.execute("SELECT entry_key, num_of_tickets, amount FROM bookingpayment WHERE booking_id = %s AND user_id = %s AND booking_status = %s", (booking_id, self.user_id,'booked'))
            booking = self.cursor.fetchone()

            if not booking:
                print("\nBooking not found. Please check the Booking ID and try again.")
                enter = input("\nPress Enter to proceed to continue..")
                return

            entry_key, num_of_tickets, amount_paid = booking

            self.cursor.execute("SELECT show_date, show_time FROM movieshowtimes WHERE entry_key = %s", (entry_key,))
            show_details = self.cursor.fetchone()
            show_date, show_time = show_details
            show_time = datetime.strptime(show_time, '%H:%M:%S').time()


            show_datetime = datetime.combine(show_date, show_time)

            current_datetime = datetime.now()

            # Check if the cancellation is allowed (only if the show is more than 2 hours away)
            if (show_datetime - current_datetime) < timedelta(hours=2):
                print("\nCancellation is not allowed. You can only cancel the booking if the showtime is more than 2 hours away.")
                enter = input("\nPress Enter to proceed to continue..")
                return


            amount_paid=float(amount_paid)
            cancellation_charge=amount_paid*0.28
            refund_amount = round(amount_paid - cancellation_charge, 2)

            # Updating booking_status as cancelled and seat number as NULL
            self.cursor.execute(" UPDATE bookingpayment SET booking_status = 'cancelled', seat_numbers = NULL WHERE booking_id = %s AND user_id = %s", (booking_id, self.user_id))
            self.connection.commit()

            update_seats_query = "UPDATE movieshowtimes SET available_seats = available_seats + %s WHERE entry_key = %s"
            self.cursor.execute(update_seats_query, (num_of_tickets, entry_key))
            self.connection.commit()

            print("\nCancelling booking...")
            print(f"Booking ID: {booking_id} for {num_of_tickets} seats has been successfully cancelled. Refund details below:\n")

            print("╔═══════════════════════════════════════╦═══════════════════╗")
            print("║               Description             ║       Amount      ║")
            print("╠═══════════════════════════════════════╬═══════════════════╣")
            print(f"║ Amount Paid                           ║ ₹{amount_paid:<16} ║")
            print(f"║ Cancellation Fee (28% including GST)  ║ ₹{round(cancellation_charge, 2):<16} ║")
            print(f"║ Refund Amount                         ║ ₹{refund_amount:<16} ║")
            print("╚═══════════════════════════════════════╩═══════════════════╝")

            enter = input("\nPress Enter to proceed to continue..")

        except mysql.connector.Error as e:
            print(f"Error canceling booking: {e}")

    def view_booking_history(self):
        try:
            current_time = datetime.now()

            # Fetch all past bookings using JOIN
            query = " SELECT bp.booking_id, ms.movie_name, ms.city, ms.theater_name, ms.show_date, ms.show_time, bp.amount, bp.seat_numbers, bp.booking_status FROM bookingpayment bp JOIN movieshowtimes ms ON bp.entry_key =  ms.entry_key WHERE bp.user_id = %s AND (ms.show_date < %s OR (ms.show_date = %s AND ms.show_time < %s)) "
            self.cursor.execute(query, (self.user_id, current_time.date(), current_time.date(), current_time.time()))
            bookings = self.cursor.fetchall()

            if not bookings:
                print("\nNo past bookings found.")
                enter = input("\nPress Enter to proceed to continue..")
                return

            print(f"\n--- Booking History for User ID: {self.user_id} ---\n")
            print("╔════╦══════╦════════════════════════╦═══════════╦═════════════╦════════════╦════════════╦═══════════════╦══════════════════════╦════════════════╗")
            print("║ No ║ B_ID ║      Movie Name        ║   City    ║ Theater     ║    Date    ║    Time    ║ Amount Paid   ║   Seat Numbers       ║ Status         ║")
            print("╠════╬══════╬════════════════════════╬═══════════╬═════════════╬════════════╬════════════╬═══════════════╬══════════════════════╬════════════════╣")

            # Loop through the results and display details in table format
            for i, (booking_id, movie_name, city, theater_name, show_date, show_time, amount, seat_numbers, booking_status) in enumerate(bookings, 1):
                seat_numbers = seat_numbers if seat_numbers else 'N/A'
                print(f"║ {i:<2} ║ {booking_id:<4} ║ {movie_name:<22} ║ {city:<8} ║ {theater_name:<11} ║ {show_date.strftime('%Y-%m-%d'):<10} ║ {show_time:<10} ║ ₹{amount:<12} ║ {seat_numbers:<20} ║ {booking_status:<14} ║")

            print("╚════╩══════╩════════════════════════╩═══════════╩═════════════╩════════════╩════════════╩═══════════════╩══════════════════════╩════════════════╝")

        
            enter = input("\nPress Enter to proceed to continue..")

        except mysql.connector.Error as e:
            print(f"Error fetching booking history: {e}")
            


class MainClass:
    def __init__(self):
        self.user_management = UserManagement()
        self.admin_management = AdminManagement()

    def display_menu(self):
        print("\n============================================================")
        print("        WELCOME TO THE MOVIE TICKET BOOKING SYSTEM")
        print("============================================================")
        while True:
            try:
                print("\n---------- Menu ----------")
                print("1. Sign Up")
                print("2. Log In")
                print("3. Exit")
                choice = int(input("\nEnter your choice (1/2/3): "))
                if choice == 1:
                    self.user_management.sign_up()
                    time.sleep(2)
                    self.user_management.user_dashboard()
                    print("\nThank you for using the system. Goodbye!")
                    break
                    
                elif choice == 2:
                    role = self.user_management.login()
                    time.sleep(2)
                    if role == "admin":
                        self.admin_management.manage_shows()
                    elif role == "user":
                        self.user_management.user_dashboard()
                        print("\nThank you for using the system. Goodbye!")
                        break
                    else:
                        print("\nLogin failed. Please try again or sign-up first.")
                
                elif choice == 3:
                    print("\nThank you for using the system. Goodbye!")
                    break

                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")


# Main execution
try:
    main_class = MainClass() 
    main_class.display_menu()
except Exception as e:
    print(f"Error during application execution: {e}")
finally:
    main_class.user_management.close_connection() 