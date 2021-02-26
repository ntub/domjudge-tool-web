from django.db import models
from django.core.files.storage import default_storage

from utils.models import BaseModel


def problem_file_path(instance, filename):
    _id = str(instance.id).replace('-', '')
    return f'problems/problem_{_id}/problem.pdf'


class Problem(BaseModel):
    name = models.CharField('題目名稱', max_length=255)
    short_name = models.CharField('題目代號', max_length=50, help_text='ex: p01')
    description_file = models.FileField('題目說明檔', upload_to=problem_file_path)
    time_limit = models.FloatField('限制執行時間', default=1.0)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='problems', verbose_name='擁有者')

    def delete(self, using=None, keep_parents=False):
        _id = str(self.id).replace('-', '')
        pdf_path = self.description_file.path
        model = super().delete(using, keep_parents)
        default_storage.delete(pdf_path)
        return model

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '題目'
        verbose_name_plural = '題目'


def normalization_text(txt: str):
    new_txt = ''
    for line in txt.splitlines():
        s = line.strip()
        if s:
            new_txt += f'{s}\n'
    return new_txt


class ProblemInOut(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='int_out_data')
    input_content = models.TextField('輸入測資')
    answer_content = models.TextField('輸出答案')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.input_content = normalization_text(self.input_content)
        self.answer_content = normalization_text(self.answer_content)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '題目輸入輸出'
        verbose_name_plural = '題目輸入輸出'
