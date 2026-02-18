import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_resume_iq():
    session = requests.Session()
    
    # 1. Register
    register_url = f"{BASE_URL}/auth/register"
    print(f"Testing Registration at {register_url}...")
    register_data = {
        "username": "testuser_script",
        "password": "password123"
    }
    # Send as JSON to trigger the JSON response path in auth.py
    response = session.post(register_url, json=register_data)
    
    if response.status_code == 200:
        print("Registration successful!")
        print(response.json())
    elif response.status_code == 400 and "Username already exists" in response.text:
        print("User already exists, proceeding to login.")
    else:
        print(f"Registration failed: {response.status_code}")
        print(response.text)
        return

    # 2. Login
    login_url = f"{BASE_URL}/auth/login"
    print(f"Testing Login at {login_url}...")
    login_data = {
        "username": "testuser_script",
        "password": "password123"
    }
    response = session.post(login_url, json=login_data)
    
    if response.status_code == 200:
        print("Login successful!")
        print(response.json())
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return

    # 3. Access Dashboard
    dashboard_url = f"{BASE_URL}/dashboard"
    print(f"Accessing Dashboard at {dashboard_url}...")
    response = session.get(dashboard_url)
    
    if response.status_code == 200:
        print("Dashboard accessed successfully!")
        if "ResumeIQ" in response.text:
            print("Dashboard content verified.")
        else:
            print("Dashboard content might look different than expected.")
    else:
        print(f"Dashboard access failed: {response.status_code}")

    # 4. Upload Resume
    upload_url = f"{BASE_URL}/upload"
    print(f"Testing Resume Upload at {upload_url}...")
    
    files = {'resume': open('test_resume.docx', 'rb')}
    data = {'role': 'Backend Developer'}
    
    response = session.post(upload_url, files=files, data=data)
    
    if response.status_code == 200:
        print("Resume uploaded successfully!")
        result = response.json()
        print(f"Score: {result.get('score')}")
        print("Verified analysis data returned.")
    else:
        print(f"Upload failed: {response.status_code}")
        print(response.text)

    # 5. Verify Database Persistence (via Dashboard check again)
    print("Verifying persistence in Dashboard...")
    response = session.get(dashboard_url)
    if "test_resume.docx" in response.text:
        print("SUCCESS: Resume found in dashboard!")
    else:
        print("FAILURE: Resume NOT found in dashboard.")

if __name__ == "__main__":
    try:
        test_resume_iq()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is it running?")
