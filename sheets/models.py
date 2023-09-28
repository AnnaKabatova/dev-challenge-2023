import sympy
from django.db import models


class Sheet(models.Model):
    sheet_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.sheet_id


class Cell(models.Model):
    cell_id = models.CharField(max_length=255)
    sheet = models.ForeignKey(
        Sheet,
        on_delete=models.CASCADE,
        related_name='cell',
    )
    value = models.CharField(max_length=255)
    result = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.sheet.sheet_id}/{self.cell_id}'
    
    def save(self, *args, **kwargs):
        if self.value.startswith('='):
            try:
                expr = sympy.sympify(self.value[1:])
                self.result = str(expr.evalf())
            except (sympy.SympifyError, ValueError):
                self.result = 'ERROR'
        else:
            self.result = self.value
        super().save(*args, **kwargs)
