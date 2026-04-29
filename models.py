from django.db import models

class Truck(models.Model):
    nome = models.CharField(max_length=100)
    cap_peso = models.FloatField(help_text="Capacidade de peso em kg")
    alt = models.FloatField(help_text="Altura em metros")
    larg = models.FloatField(help_text="Largura em metros")
    comp = models.FloatField(help_text="Comprimento em metros")

    def __str__(self):
        return self.nome

class Load(models.Model):
    name = models.CharField(max_length=100)
    peso = models.FloatField(help_text="Peso em kg")
    alt = models.FloatField(help_text="Altura em metros")
    larg = models.FloatField(help_text="Largura em metros")
    comp = models.FloatField(help_text="Comprimento em metros")
    val = models.FloatField(help_text="Valor em R$")
    quantidade = models.PositiveIntegerField(default=1, help_text="Quantidade desta carga")

    def __str__(self):
        return f"{self.name} ({self.quantidade}x)"
