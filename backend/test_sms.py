from notifications import send_sms
import os

print("TWILIO_SID from env:", os.environ.get("TWILIO_SID"))
print("TWILIO_AUTH from env:", os.environ.get("TWILIO_AUTH_TOKEN"))

# Try sending a test SMS
result = send_sms("+917793929357", "Test SMS from Smart Plant System")
print("Send SMS result:", result)
