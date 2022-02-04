from django.db import models

from simple_history.models import HistoricalRecords

class ModeloQuantumStorage(models.Model):
    fecha_creacion = models.DateTimeField(editable=False, null=True)
    fecha_modificacion = models.DateTimeField(null=True)
    historico = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from django.utils import timezone
        
        if not(self.id):
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(Registro, self).save(*args, **kwargs)
