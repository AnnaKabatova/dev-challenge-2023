from django.db import models


class Spreadsheet(models.Model):
    id = models.CharField(primary_key=True, max_length=30)


class Cell(models.Model):
    cell_id = models.CharField(max_length=30)
    value = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (("spreadsheet", "cell_id"),)
