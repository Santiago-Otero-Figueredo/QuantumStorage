from distutils import extension
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
from apps.core.models import QuantumStorageModel

class File(QuantumStorageModel):
    folder = models.ForeignKey('folders.Folder', related_name='files', verbose_name='Folder where the file is contained', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Name of the file')
    route = models.CharField(max_length=255, verbose_name='Route where it is located')
    extension = models.CharField(max_length=15, verbose_name='Extension of the file')
    size = models.PositiveBigIntegerField(verbose_name='Size of the file in bytes')
    
    
class Folder(QuantumStorageModel):
    owner_user = models.ForeignKey('users.User', related_name='folders', verbose_name='User owner of the folder', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField('users.User', related_name='shared_folders', through='folders.Collaborators', verbose_name='Users collaborating in the folder')
    folders = models.ForeignKey('self', related_name='parent_folder', verbose_name='Parent folder of the current folder', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name = 'Name of the folder')


class Collaborators(QuantumStorageModel):
    user = models.ForeignKey('users.User', related_name='collaborating_users', verbose_name='Collaborators of the folder', on_delete=models.CASCADE)
    folder = models.ForeignKey('folders.Folder', related_name='collaborative_folder', verbose_name='Folder to collaborate', on_delete=models.CASCADE)
    invite_reason = models.CharField(max_length=255)