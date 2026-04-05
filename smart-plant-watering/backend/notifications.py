import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID", "your_account_sid_here")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token_here")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

def send_sms(to_number: str, message: str):
    # Dummy printing for simulator mode to avoid real errors if not set
    print(f"--- FAKE SMS SENDER ---")
    print(f"To: {to_number}")
    print(f"Message: {message}")
    print(f"-----------------------")
    
    if TWILIO_SID == "your_account_sid_here":
        print("Mock: SMS Sent Details Logged. Real Twilio credentials not provided.")
        return True

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return True
    except Exception as e:
        print(f"Twilio Error: {e}")
        return False
