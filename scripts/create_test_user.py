import requests

def create_test_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post("http://localhost:8000/users/", json=user_data)
        print("Test user created successfully:", response.json())
    except Exception as e:
        print("Error creating test user:", e)

if __name__ == "__main__":
    create_test_user() 