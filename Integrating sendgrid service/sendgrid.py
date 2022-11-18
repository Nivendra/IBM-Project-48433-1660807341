import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key='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')
from_email = Email("sharma.0276.abhi@gmail.com")  
to_email = To("1905064cse@cit.edu.in")  
subject = "IBM Project"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, to_email, subject, content)

mail_json = mail.get()
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)