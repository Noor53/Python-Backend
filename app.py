from flask import Flask,request,jsonify,session
import csv
#from students import students
from datetime import datetime

app = Flask(__name__)
#app.secret_key = 'your_secret_key'
data_file = 'data/user_data.csv'

def read_data():
  with open(data_file, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)
   # print(data)
  return data

def write_data(data):
  with open(data_file, 'a', newline='') as csvfile:
    fieldnames = data.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(data)

# Function to check if a user is logged in
def is_logged_in():
  return 'username' in session

# Function to get the currently logged-in username
def get_logged_in_user():
  if is_logged_in():
    return session['username']
  return None

# @app.route('/register', methods=['POST'])
# def register_user():
#   # Get user data from request body
#   print("Before getting data")
#   data = request.json
#   print("After getting data"+data)
#   username = data.get('username')
#   password = data.get('password')

#   # Validate user data (optional)
#   # ... (add validation logic)

#   # Check if username already exists
#   existing_users = read_data()
#   for user in existing_users:
#     if user['username'] == username:
#       return jsonify({'message': 'Username already exists'}), 400

#   # Create new user entry
#   new_user = {
#       'username': username,
#       'password': password,  # Store password securely (hashing recommended)
#       'login_time': None,
#       'logout_time': None,
#       'session_id': None,  # Optional: Track session ID for advanced use cases
#   }
#   write_data(new_user)

#   return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/registeruser', methods=['POST'])
def register_user():
   print(request.form)
   if request.content_type == 'application/json':
         print("Json Data")
         data = request.json
         print(data)
         username = data.get('username')
         password = data.get('password')
   else:
        print("form data")
        data = request.form
        username = data.get('username')
        password = data.get('password')
    
   if not username or not password:
         return jsonify({'message': 'Username and password are required'}), 400

   # Check if username already exists
   existing_users = read_data()
   for user in existing_users:
     if user['username'] == username:
       return jsonify({'message': 'Username already exists'}), 400

   # Create new user entry
   new_user = {
       'username': username,
      'password': password,  # Store password securely (hashing recommended)
       'login_time': None,
      'logout_time': None,
       'session_id': None,  # Optional: Track session ID for advanced use cases
   }
   write_data(new_user)

   return jsonify({'message': 'User registered successfully!'}), 201

# Route to login a user (POST)
@app.route('/login', methods=['POST'])
def login_user():
  # Get login credentials from request body
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  # Validate credentials (optional)
  # ... (add validation logic)

  # Check if username exists
  existing_users = read_data()
  for user in existing_users:
    if user['username'] == username and user['password'] == password:  # Consider secure password hashing
      # Login successful
      session['username'] = username
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      user['login_time'] = current_time
      # Update user data in CSV (optional for tracking login time)
      write_data(user)
      return jsonify({'message': 'Login successful!'}), 200
  return jsonify({'message': 'Invalid username or password'}), 401

# Route to logout a user (POST)
@app.route('/logout', methods=['POST'])
def logout_user():
  if not is_logged_in():
    return jsonify({'message': 'You are not logged in'}), 401

  username = get_logged_in_user()
  session.pop('username', None)  # Remove user from session

  # Find the user in the CSV data (optional for tracking logout time)
  existing_users = read_data()
  for user in existing_users:
    if user['username'] == username:
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      user['logout_time'] = current_time
      # Update user data in CSV (optional)
      write_data(user)
      break

  return jsonify({'message': 'Logout successful!'}), 200

@app.route('/user', methods=['GET'])
def get_user_info():
  if not is_logged_in():
    return jsonify({'message': 'You are not logged in'}), 401

  username = get_logged_in_user()

  # Find the user's data in the CSV
  existing_users = read_data()
  for user in existing_users:
    if user['username'] == username:
      # Return user data (excluding password for security)
      return jsonify(user), 200
  return jsonify({'message': 'User not found'}), 404

if __name__ == "__main__":
        app.run(debug=True)
        