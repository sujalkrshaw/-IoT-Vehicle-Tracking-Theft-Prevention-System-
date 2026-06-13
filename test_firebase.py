from firebase.firebase_handler import (
    upload_vehicle_data
)

upload_vehicle_data(
    {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "status": "SAFE"
    }
)

print(
    "Firebase Upload Successful"
)