import requests
import json
from datetime import datetime

DAO_URL = "http://localhost:5001"


class AdminClient:
    def __init__(self):
        self.base_url = DAO_URL

    def list_all_requests(self):
        """List all requests"""
        response = requests.get(f"{self.base_url}/requests")
        if response.status_code == 200:
            requests_data = response.json()
            print(f"\nTotal requests: {len(requests_data)}")
            print("-" * 80)
            for req in requests_data:
                print(
                    f"ID: {req['id']} | {req['client_name']} | {req['temperature']}°C | {req['activity']} | {req['created_at']}")
        else:
            print(f"Error: {response.status_code}")

    def get_request(self, request_id):
        """Get a specific request by ID"""
        response = requests.get(f"{self.base_url}/requests/{request_id}")
        if response.status_code == 200:
            req = response.json()
            print("\nRequest Details:")
            print(f"  ID: {req['id']}")
            print(f"  Client: {req['client_name']}")
            print(f"  Birth Date: {req['birth_date']}")
            print(f"  Machine: {req['machine_name']}")
            print(f"  Username: {req['username']}")
            print(f"  Temperature: {req['temperature']}°C")
            print(f"  Activity: {req['activity']}")
            print(f"  Created: {req['created_at']}")
        else:
            print(f"Error: Request {request_id} not found")

    def create_request(self, data):
        """Create a new request"""
        response = requests.post(f"{self.base_url}/requests", json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"Request created with ID: {result['id']}")
        else:
            print(f"Error creating request: {response.status_code}")

    def update_request(self, request_id, data):
        """Update an existing request"""
        response = requests.put(f"{self.base_url}/requests/{request_id}", json=data)
        if response.status_code == 200:
            print(f"Request {request_id} updated successfully")
        else:
            print(f"Error updating request: {response.status_code}")

    def delete_request(self, request_id):
        """Delete a request"""
        response = requests.delete(f"{self.base_url}/requests/{request_id}")
        if response.status_code == 200:
            print(f"Request {request_id} deleted successfully")
        else:
            print(f"Error deleting request: {response.status_code}")

def main():
    client = AdminClient()

    while True:
        print("\n=== Admin Client for DAO Service ===")
        print("1. List all requests")
        print("2. Get specific request")
        print("3. Create new request")
        print("4. Update request")
        print("5. Delete request")
        print("0. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            client.list_all_requests()

        elif choice == "2":
            request_id = input("Enter request ID: ")
            client.get_request(int(request_id))

        elif choice == "3":
            print("\nEnter request data:")
            data = {
                'client_name': input("Client name: "),
                'birth_date': input("Birth date (YYYY-MM-DD): "),
                'machine_name': input("Machine name: "),
                'username': input("Username: "),
                'temperature': float(input("Temperature: ")),
                'activity': input("Activity: ")
            }
            client.create_request(data)

        elif choice == "4":
            request_id = input("Enter request ID to update: ")
            print("\nEnter new data:")
            data = {
                'client_name': input("Client name: "),
                'birth_date': input("Birth date (YYYY-MM-DD): "),
                'machine_name': input("Machine name: "),
                'username': input("Username: "),
                'temperature': float(input("Temperature: ")),
                'activity': input("Activity: ")
            }
            client.update_request(int(request_id), data)

        elif choice == "5":
            request_id = input("Enter request ID to delete: ")
            confirm = input(f"Are you sure you want to delete request {request_id}? (y/n): ")
            if confirm.lower() == 'y':
                client.delete_request(int(request_id))

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()