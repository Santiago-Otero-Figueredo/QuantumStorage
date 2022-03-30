from django.db import models

from apps.users.models import User

# Create your models here.
from apps.core.models import QuantumStorageModel


class EntityDirectory(QuantumStorageModel):
    name = models.CharField(max_length=255, verbose_name='Name of the file')
    type = models.CharField(max_length=255, verbose_name='Type of entity(folder, music, text, video, etc...) ')
    size = models.PositiveBigIntegerField(verbose_name='Size of the file in bytes')
    route = models.CharField(max_length=255, verbose_name='Route where it is located')
    collaborators = models.ManyToManyField('users.User', related_name='shared_entities', through='folders.Collaborations', verbose_name='Users collaborating in the folder')


class Folder(EntityDirectory):
    owner_user = models.ForeignKey('users.User', related_name='folders', verbose_name='User owner of the folder', on_delete=models.CASCADE)    
    folders = models.ForeignKey('self', related_name='parent_folder', verbose_name='Parent folder of the current folder', on_delete=models.CASCADE, null=True)


class File(EntityDirectory):
    container_folder = models.ForeignKey('folders.Folder', related_name='files', verbose_name='Folder where the file is contained', on_delete=models.CASCADE)    
    extension = models.CharField(max_length=15, verbose_name='Extension of the file')
    

class Permissions(QuantumStorageModel):
    code = models.CharField(max_length=3, verbose_name='Code of permission')
    name = models.CharField(max_length=255, verbose_name='Name of permission')


class Collaborations(QuantumStorageModel):
    user = models.ForeignKey('users.User', related_name='collaborations_entities', verbose_name='Collaborators of the folder', on_delete=models.CASCADE)
    permissions = models.ManyToManyField('folders.Permissions', related_name='collaborations', verbose_name='Permissions of the collaborator') # El creador de la entidad debe tener el permiso admin
    entity_directory = models.ForeignKey('folders.EntityDirectory', related_name='collaborative_folder', verbose_name='Folder to collaborate', on_delete=models.CASCADE)
    invite_reason = models.CharField(max_length=255)
