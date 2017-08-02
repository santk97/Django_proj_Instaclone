
from sendgrid import SendGridAPIClient , Email

sg = SendGridAPIClient('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')
message = Email()

message.add_to("Email Address of Reciever")
message.set_from("Email Address of Sender")
message.set_subject("Email Subject")
message.set_html("Email html")

sg.send(message)