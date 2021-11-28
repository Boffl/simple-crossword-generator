from django.db import models


# Create your models here.
class Words3(models.Model):
    """ Database with all the words and definitions for the crossword """
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=30)
    definition = models.TextField()
    hint = models.TextField()
    zipf_freq = models.FloatField()

    def __str__(self):
        return self.word

    class Meta:
        managed = False
        db_table = 'words_2'


