from django.db import models

# Create your models here.

# Creamos la nueva clase para el modelo, que será un CharField



# Modelo de un elemento de la DB, no de la DB en sí
class UrlDB(models.Model):
    larga = models.CharField(max_length=64)

    def __str__(self):  # Método para devolver como string el apartado del campo
        return self.larga
