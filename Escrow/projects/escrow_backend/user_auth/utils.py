from django.core.mail import EmailMessage
import jwt, uuid
from datetime import datetime, timedelta
from django.conf import settings

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()
        
    @staticmethod
    def generate_jwt_token(user_id):
        payload = {
            'token_type': 'access',
            'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 minutes
            'iat': datetime.utcnow(),
            'jti': uuid.uuid4().hex,
            'user_id': user_id
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token