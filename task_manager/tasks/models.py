from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels

from django.utils.translation import gettext_lazy as _


class Tasks(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.PROTECT,
                               related_name='tasks_author',
                               verbose_name=_('Author'))
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 blank=True, null=True,
                                 related_name='tasks_executor',
                                 verbose_name=_('Executor'))
    labels = models.ManyToManyField(Labels, blank=True,
                                    related_name='labels',
                                    verbose_name=_('Labels'))
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name=_('Date of creation'))

    def __str__(self):
        return self.name