import logging

from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from scrobbles.mixins import ScrobblableMixin

logger = logging.getLogger(__name__)
BNULL = {"blank": True, "null": True}


class Author(TimeStampedModel):
    name = models.CharField(max_length=255)


class Book(ScrobblableMixin):
    COMPLETION_PERCENT = getattr(settings, 'SPORT_COMPLETION_PERCENT', 90)

    start = models.DateTimeField(**BNULL)

    def __str__(self):
        return f"{self.start.date()} - {self.round} - {self.home_team} v {self.away_team}"

    def get_absolute_url(self):
        return reverse("sports:event_detail", kwargs={'slug': self.uuid})

    @classmethod
    def find_or_create(cls, data_dict: Dict) -> "Event":
        """Given a data dict from Jellyfin, does the heavy lifting of looking up
        the video and, if need, TV Series, creating both if they don't yet
        exist.

        """
