import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bitespeed_app.models import contact
from bitespeed_app.serializer import ContactSerializer

@api_view(['GET', 'POST'])
def post_identity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', None)
        phoneNumber = data.get('phoneNumber', None)
        if phoneNumber:
            phone_qs = contact.objects.filter(phoneNumber=phoneNumber).order_by('id').first()
            if not phone_qs:
                email_qs = contact.objects.filter(email=email).order_by('id').first()
                if not email_qs:
                    obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=None, linkPrecedence = 'primary')
                    obj.save()
                else:
                    serializer = ContactSerializer(email_qs)
                    serialized_data = serializer.data
                    id = serialized_data.get('id')
                    linkedId = serialized_data.get('linkedId')
                    if not linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=id, linkPrecedence = 'secondary')
                        obj.save()
                    elif linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=linkedId, linkPrecedence = 'secondary')
                        obj.save()
            else:
                serializer = ContactSerializer(phone_qs)
                serialized_data = serializer.data
                id = serialized_data.get('id')
                linkedId = serialized_data.get('linkedId')
                email_qs = contact.objects.filter(email=email).order_by('-id').first()
                if not email_qs:
                    if not linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=id, linkPrecedence = 'secondary')
                        obj.save()
                    elif linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=linkedId, linkPrecedence = 'secondary')
                        obj.save()
                else:
                    serializer = ContactSerializer(email_qs)
                    serialized_data = serializer.data
                    id_email = serialized_data.get('id')
                    linkedId__email = serialized_data.get('linkedId')
                    if id_email < id:
                        obj = contact.objects.filter(email=email, phoneNumber=phoneNumber, linkedId=id_email).update( linkPrecedence = 'secondary')
                    elif id_email > id:
                        obj = contact.objects.filter(email=email, phoneNumber=phoneNumber, linkedId=id).update( linkPrecedence = 'secondary')

        elif email:
            email_qs = contact.objects.filter(email=email).order_by('-id').first()
            if not email_qs:
                phone_qs = contact.objects.filter(phoneNumber=phoneNumber).order_by('-id').first()
                if not phone_qs:
                    obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=None, linkPrecedence = 'primary')
                    obj.save()
                else:
                    serializer = ContactSerializer(phone_qs)
                    serialized_data = serializer.data
                    id = serialized_data.get('id')
                    linkedId = serialized_data.get('linkedId')
                    if not linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=id, linkPrecedence = 'secondary')
                        obj.save()
                    elif linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=linkedId, linkPrecedence = 'secondary')
                        obj.save()
            else:
                serializer = ContactSerializer(email_qs)
                serialized_data = serializer.data
                id = serialized_data.get('id')
                linkedId = serialized_data.get('linkedId')
                phone_qs = contact.objects.filter(phoneNumber=phoneNumber).order_by('-id').first()
                if not phone_qs:
                    if not linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=id, linkPrecedence = 'secondary')
                        obj.save()
                    elif linkedId:
                        obj = contact.objects.create(email=email, phoneNumber=phoneNumber, linkedId=linkedId, linkPrecedence = 'secondary')
                        obj.save()
                else:
                    serializer = ContactSerializer(phone_qs)
                    serialized_data = serializer.data
                    id_email = serialized_data.get('id')
                    linkedId__email = serialized_data.get('linkedId')
                    if id_email < id:
                        obj = contact.objects.filter(email=email, phoneNumber=phoneNumber, linkedId=id_email).update(linkPrecedence = 'secondary')
                    elif id_email>id:
                        obj = contact.objects.filter(email=email, phoneNumber=phoneNumber, linkedId=id).update(linkPrecedence = 'secondary')
        if phoneNumber:
            primary_id_qs_1 = contact.objects.filter(phoneNumber=phoneNumber, linkedId=None).order_by('id').first()
        if email:
            primary_id_qs_2 = contact.objects.filter(email = email, linkedId=None).order_by('id').first()
        primary_id_qs_1 = ContactSerializer(primary_id_qs_1)
        primary_id_1 = primary_id_qs_1.data.get("id", None)
        primary_id_qs_2 = ContactSerializer(primary_id_qs_2)
        primary_id_2 = primary_id_qs_2.data.get("id", None)
        if not primary_id_1:
            primary_id_1 = primary_id_2
        elif not primary_id_2:
            primary_id_2 = primary_id_1
        if primary_id_1 > primary_id_2:
            primary_id = primary_id_2
        else:
            primary_id = primary_id_1
        emails_get = contact.objects.filter(linkedId=primary_id).order_by("id")
        emails_get = ContactSerializer(emails_get, many=True).data
        emails = []
        for email in emails_get:
            emails.append(email.get("email", None))
        unique_email_set = set(emails)
        unique_emails = list(unique_email_set)
        phone_number = contact.objects.filter(email__in = unique_emails).order_by('id')
        phone_number = ContactSerializer(phone_number, many=True).data
        phone_numbers = []
        for phone in phone_number:
            phone_numbers.append(phone.get("phoneNumber", None))
        unique_phone_set = set(phone_numbers)
        unique_phone_numbers = list(unique_phone_set)
        secondary_ids = contact.objects.filter(linkedId = primary_id).order_by("id")
        secondary_id = ContactSerializer(secondary_ids, many=True).data
        secondary_ids = []
        for secondary in secondary_id:
            secondary_ids.append(secondary.get("id", None))
        unique_ids_set = set(secondary_ids)
        unique_ids_numbers = list(unique_ids_set)
        response = {
            "contact":{
                "primartContatctId": primary_id,
                "emails": unique_emails,
                "phoneNumbers":unique_phone_numbers,
                "secondaryContactIds":unique_ids_numbers
            }
        }
    return Response(response, status=200)