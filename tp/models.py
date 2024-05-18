from django.db import models

# Create your models here.
class register(models.Model):
    Name=models.CharField(max_length=30,null=False )
    Mobile=models.CharField(max_length=10 , blank=True,null=False)
    Email=models.EmailField(unique=True,null=False)
    Date_of_birth=models.DateField()
    gender_choice=[('M','Male'),('F','Female'),('O','Other')]
    Gender=models.CharField(max_length=1 , choices=gender_choice)
    password=models.CharField(max_length=25,null=False)
    
    def __str__(self):
        return self.Email
class forgot(models.Model):

    Email=models.EmailField()

class password(models.Model):
    password=models.CharField(max_length=20)
    confirm_password=models.CharField(max_length=20 )

class Script(models.Model):
    title = models.CharField(max_length=100)
    synopsis = models.TextField()
    genre = models.CharField(max_length=50)
    script_file = models.FileField(upload_to='scripts/')

    def __str__(self):
        return self.title