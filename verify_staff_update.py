import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_update():
    print("Testing Staff Update...")
    
    # 1. Create a staff to update
    print("Creating temporary staff...")
    staff_data = {
        "staff_id": "TEST_UPDATE",
        "surname": "TEST_SURNAME",
        "firstname": "TEST_FIRSTNAME",
        "active": True
    }
    r = requests.post(f"{BASE_URL}/staff/", json=staff_data)
    if r.status_code != 200:
        print(f"Failed to create staff: {r.text}")
        return
    
    created_staff = r.json()
    staff_id = created_staff['id']
    print(f"Created Staff ID: {staff_id}")
    
    # 2. Update the staff
    print(f"Updating Staff ID: {staff_id}...")
    update_data = {
        "staff_id": "TEST_UPDATE", # Required by schema, keep same
        "surname": "UPDATED_SURNAME",
        "firstname": "UPDATED_FIRSTNAME",
        "remark": "UPDATED REMARK"
    }
    r = requests.put(f"{BASE_URL}/staff/{staff_id}", json=update_data)
    
    if r.status_code == 200:
        updated_staff = r.json()
        print("Update Successful!")
        print(f"Original: {created_staff['surname']} {created_staff['firstname']}")
        print(f"Updated:  {updated_staff['surname']} {updated_staff['firstname']}")
        print(f"Remark:   {updated_staff['remark']}")
        
        if updated_staff['surname'] == "UPDATED_SURNAME":
            print("VERIFICATION PASSED: Surname updated matches.")
        else:
            print("VERIFICATION FAILED: Surname mismatch.")
    else:
        print(f"Update Failed: {r.status_code} {r.text}")

if __name__ == "__main__":
    test_update()
