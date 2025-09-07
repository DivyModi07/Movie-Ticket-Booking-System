# 🎬 Movie Ticket Booking System

A comprehensive Python-based movie ticket booking system with MySQL database integration, featuring both user and admin functionalities.

## ✨ Features

### 👤 User Features
- **User Registration & Authentication** - Secure sign-up and login system
- **Movie Booking** - Browse movies by city, select theaters, and book tickets
- **Interactive Seat Selection** - Visual theater layout with real-time seat availability
- **Booking Management** - View current bookings and booking history
- **Cancellation** - Cancel bookings with refund calculation (28% cancellation fee)
- **Movie Popularity** - View movie statistics and popularity charts

### 👨‍💼 Admin Features
- **Show Management** - Add, update, and delete movie shows
- **Multi-day Scheduling** - Schedule movies for up to 7 days
- **Analytics** - Movie popularity analysis with visual charts
- **Real-time Updates** - Manage showtimes and seat availability

## 🛠️ Technical Stack

- **Backend**: Python
- **Database**: MySQL
- **Visualization**: Matplotlib
- **Dependencies**: mysql-connector-python

## 🗃️ Database Schema

The system uses three main tables:
- `users` - User accounts and authentication
- `movieshowtimes` - Movie show information and seat availability
- `bookingpayment` - Booking transactions and payment details

## 🚀 Installation

1. **📥 Clone the repository**
   ```bash
   git clone https://github.com/DivyModi07/Movie-Ticket-Booking-System
   cd "Movie-Ticket-Booking-System"
   ```

2. **📦 Install Python dependencies**
   ```bash
   pip install mysql-connector-python matplotlib
   ```

3. **🗄️ Set up MySQL database**
   - Import the provided SQL file: `movie_booking(database).sql`
   - Update database credentials in `movie_booking.py` (lines 13-18)

4. **▶️ Run the application**
   ```bash
   python movie_booking.py
   ```

## 📖 Usage

### 🔑 Default Admin Account
- **User ID**: admin91
- **Password**: 101010

### 👤 User Registration
- Create a new account with name and mobile number
- System generates unique User ID automatically
- Set a 6-digit PIN for authentication

### 🎫 Booking Process
1. Select city (Ahmedabad, Surat, Vadodara)
2. Choose from available movies
3. Select theater and showtime
4. Pick seats from interactive layout
5. Confirm payment with automatic GST calculation

## 🌟 Key Features

- **Real-time Seat Management** - Prevents double booking
- **Dynamic Pricing** - Different prices for different showtimes
- **GST Calculation** - Automatic tax calculation (18% GST + 10% base)
- **Cancellation Policy** - 2-hour advance cancellation with refund
- **Data Visualization** - Movie popularity charts using Matplotlib
- **Input Validation** - Comprehensive validation for all user inputs

## 📁 Project Structure

```
Movie Ticket Booking System (PYTHON)/
├── movie_booking.py              # Main application file
├── movie_booking(database).sql   # Database schema and sample data
└── README.md                     # Readme file
```

## 📋 Requirements

- Python 3.6+
- 🗄MySQL 5.7+
- Windows/Linux/macOS
