from django.db import models

# Create your models here.
class User(models.Model):
    # id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=54)
    phone=models.CharField(max_length=13)
    amount=models.IntegerField()
    paid=models.BooleanField(default=False)

    
    def __str__(self):
        return self.name + " paid " +str(self.amount)
    