from django.db import models


class Spreadsheet(models.Model):
    id = models.CharField(primary_key=True, max_length=30)

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.get(id__iexact=id)
        except cls.DoesNotExist:
            return None


class Cell(models.Model):
    cell_id = models.CharField(max_length=30)
    value = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("spreadsheet", "cell_id"),)

    @classmethod
    def get_by_cell_id(cls, spreadsheet, cell_id):
        try:
            return cls.objects.get(spreadsheet=spreadsheet, cell_id__iexact=cell_id)
        except cls.DoesNotExist:
            return None
