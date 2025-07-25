from flask import Flask, request, jsonify
import re
from models import User

app = Flask(__name__)

def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_data(data: dict, required_fields: list) -> tuple[bool, str]:
    """Validate user input data"""
    if not isinstance(data, dict):
        return False, "Invalid JSON data"
    
    for field in required_fields:
        if field not in data or not data[field] or not isinstance(data[field], str):
            return False, f"Missing or invalid field: {field}"
    
    if 'email' in data and not validate_email(data['email']):
        return False, "Invalid email format"
    
    if 'password' in data and len(data['password']) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, ""

@app.route('/')
def home():
    return jsonify({"message": "User Management System", "status": "healthy"})

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.get_all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve users"}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve user"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        is_valid, error_msg = validate_user_data(data, ['name', 'email', 'password'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Check if email already exists
        existing_user = User.get_by_email(data['email'])
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409
        
        user = User(name=data['name'], email=data['email'], password=data['password'])
        if user.save():
            return jsonify({"message": "User created successfully", "user": user.to_dict()}), 201
        else:
            return jsonify({"error": "Failed to create user"}), 500
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Validate only provided fields
        provided_fields = [field for field in ['name', 'email'] if field in data]
        if not provided_fields:
            return jsonify({"error": "No valid fields provided"}), 400
        
        is_valid, error_msg = validate_user_data(data, provided_fields)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Check if email already exists (if email is being updated)
        if 'email' in data and data['email'] != user.email:
            existing_user = User.get_by_email(data['email'])
            if existing_user:
                return jsonify({"error": "Email already exists"}), 409
        
        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        if user.save():
            return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200
        else:
            return jsonify({"error": "Failed to update user"}), 500
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if user.delete():
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete user"}), 500
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/search', methods=['GET'])
def search_users():
    try:
        name = request.args.get('name')
        if not name or not name.strip():
            return jsonify({"error": "Please provide a name to search"}), 400
        
        users = User.search_by_name(name.strip())
        return jsonify([user.to_dict() for user in users]), 200
    
    except Exception as e:
        return jsonify({"error": "Failed to search users"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        is_valid, error_msg = validate_user_data(data, ['email', 'password'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        user = User.get_by_email(data['email'])
        if user and User.verify_password(data['password'], user.password):
            return jsonify({
                "status": "success", 
                "user_id": user.id,
                "message": "Login successful"
            }), 200
        else:
            return jsonify({"status": "failed", "error": "Invalid credentials"}), 401
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)