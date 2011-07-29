from django.db import models
from datetime import datetime
from django.conf import settings


# notify dependency
from notify.utils import notify

STATUS = (
    ('1', 'Pending'),
    ('2', 'Processing'),
    ('3', 'Processed'),
    ('4', 'Directly Sent'),
)


class Queue(models.Model):
    """
    Email queue
    """
    body = models.TextField()
    subject = models.TextField()
    from_email = models.EmailField()
    status = models.CharField(max_length = 1, choices = STATUS, default = '1')
    sent = models.DateTimeField(default = datetime.now)

    hostname = models.CharField(max_length = 255, blank=True, null=True)

    def __unicode__(self):
        return self.subject

    class Meta:
#FIFO
#        ordering = ('-sent',)
        ordering = ('sent',)


class QueueEmail(models.Model):
    """
    email address with FK to a Queue



    TO DO:
        - if sending error, put message at the end of queue and store number of tries, so that if tried 5 times, give up
    """
    to_email = models.EmailField()
    queue = models.ForeignKey(Queue)
    sent = models.DateTimeField(default = datetime.now)

    def __unicode__(self):
        return self.to_email

    class Meta:
#FIFO
#        ordering = ('-sent',)
        ordering = ('sent',)

    def send(self):
        qe = QueueEmail.objects.select_related('queue').get(id = self.id)
        q = qe.queue

        # send email and mark queue as 'processing'
        notify(str(self.to_email), q.subject, {'body': q.body}, template = 'massmail/email_blank.html', from_email = settings.DEFAULT_FROM_EMAIL)

        #delete
        self.delete()

        # see if queue is done
        qes = QueueEmail.objects.filter(queue = q).count()
        q.status = '2'
        if not qes:
            q.status = '3'

        q.save()
        
