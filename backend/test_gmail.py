
from app.services.gmail_service import send_email

def main():
    recipient = input("Enter the recipient Gmail address: ").strip()

    try:
        result = send_email(
            to_email=recipient,
            subject="TaskFlow - Gmail Integration Test",
            body="""
Hello!

This is a test email from TaskFlow.

Your Gmail API integration is working successfully.

Soon, TaskFlow will automatically send notifications when:
1. A new task is assigned to you.
2. A task is marked as completed.

Regards,
TaskFlow Team
"""
        )

        print("\nEmail sent successfully!")
        print("Gmail Message ID:", result["message_id"])

    except Exception as error:
        print("\nEmail sending failed.")
        print("Error:", str(error))


if __name__ == "__main__":
    main()
