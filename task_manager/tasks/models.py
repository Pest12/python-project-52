from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels

from django.utils.translation import gettext_lazy as _


class Tasks(models.Model):
    """Represents a task in the task manager."""
    name = models.CharField(max_length=150,
                            null=False,
                            blank=False,
                            unique=True,
                            verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Сreation date'))
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               null=False,
                               blank=False,
                               verbose_name=_('Status'))
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.PROTECT,
                               null=False,
                               related_name='task_author',
                               verbose_name=_('Author'))
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True,
                                 related_name='task_executor',
                                 verbose_name=_('Executor'))
    labels = models.ManyToManyField(Labels,
                                    blank=True,
                                    null=True,
                                    through='TaskToLabel',
                                    through_fields=('task', 'label'),
                                    verbose_name=_('Labels'))

    def __str__(self):
        return self.name


class TaskToLabel(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)
