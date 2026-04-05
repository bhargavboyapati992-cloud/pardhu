import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")

try:
    client = Client(TWILIO_SID, TWILIO_AUTH)
    messages = client.messages.list(limit=5)
    
    print("--- TWILIO MESSAGE LOGS ---")
    with open("twilio_status_logs.txt", "w", encoding="utf-8") as f:
        f.write("--- TWILIO MESSAGE LOGS ---\n")
        if not messages:
            print("No messages found in your Twilio account history.")
            f.write("No messages found in your Twilio account history.\n")
        else:
            for record in messages:
                output = (
                    f"To: {record.to}\n"
                    f"From: {record.from_}\n"
                    f"Status: {record.status}\n"
                )
                if record.error_message:
                    output += f"Error Code: {record.error_code}\nError Message: {record.error_message}\n"
                output += f"Body: {record.body}\n---------------------------\n"
                
                print(output, end="")
                f.write(output)

except Exception as e:
    with open("twilio_status_logs.txt", "w", encoding="utf-8") as f:
        f.write(f"Failed to fetch logs. Error: {e}\n")
