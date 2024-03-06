from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from django.utils.translation import gettext as _


class Tasks(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Name'))
    description = models.TextField(max_length=500,
                                   blank=True,
                                   null=True,
                                   verbose_name=_('Description'))
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               related_name='status',
                               verbose_name=_('Status'))
    author = models.ForeignKey(Users,
                               on_delete=models.PROTECT,
                               related_name='author',
                               verbose_name=_('Author'))
    executor = models.ForeignKey(Users,
                                 on_delete=models.PROTECT,
                                 related_name='executor',
                                 verbose_name=_('Executor'),
                                 blank=True,
                                 null=True)
    labels = models.ManyToManyField(Labels,
                                    blank=True,
                                    related_name='labels',
                                    verbose_name=_('Labels'))
    timestamp = models.DateTimeField(auto_now_add=True,
                                     verbose_name=_('Date of creation'))

    def __str__(self) -> str:
        return self.name
