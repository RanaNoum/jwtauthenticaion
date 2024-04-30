# from django.core.mail import EmailMessage
# from django.core.mail import send_mail
# from django.conf import settings
# import os

# class Util:
#   @staticmethod
#   def send_email(data):
#     email = EmailMessage(
#       subject=data['subject'],
#       body=data['body'],
#       from_email=os.environ.get('EMAIL_FROM'),
#       to=[data['noumanlatifm@gmail.com']]
#     )
#     email.send()

# def send_model_data_via_email(model_instance):
#     subject = PricingEstimate
#     message = 'test date'
#     for field in model_instance._meta.get_fields():
#         message += f'{field.name}:{getattr(model_instance,field.name)}\n'
#         send_mail(
#             subject,
#             message,
#             settings:'18251598-111@uog.edu.pk',
#             ['noumanlatifm@gmail.com']


#         )

#  def send_model_data_via_email(model_instance):
#     subject = 'Model Data'
#     message = 'test date'
#     for field in model_instance._meta.get_fields():
#         message += f'{field.name}:{getattr(model_instance, field.name)}\n'
#     send_mail(
#         subject,
#         message,
#         '18251598-111@uog.edu.pk',  # sender email
#         ['noumanlatifm@gmail.com']  # recipient email
#     )

