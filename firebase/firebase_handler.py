import firebase_admin

from firebase_admin import credentials
from firebase_admin import db


if not firebase_admin._apps:

    cred = credentials.Certificate(
        "firebase/firebase-adminsdk.json"
    )

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL":
            "https://iot-vehicle-tracking-sys-cbf04-default-rtdb.asia-southeast1.firebasedatabase.app"
        }
    )


def upload_vehicle_data(data):

    ref = db.reference(
        "vehicle_logs"
    )

    ref.push(data)