from django.db import models

class contact(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    phoneNumber = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=254)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'contact'

