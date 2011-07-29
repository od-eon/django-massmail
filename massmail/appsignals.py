from cron.appsignals import cron_signal
from massmail.models import QueueEmail
from django.db import transaction
from emencia.django.newsletter.mailer import Mailer
from emencia.django.newsletter.models import Newsletter
from misc.lib import dbg

@transaction.autocommit
def sendMails(sender, freq, **kwargs):

    if freq != 'every5minutes':
        return

    qs = QueueEmail.objects.all()[:10]
    for q in qs:
        q.send()



def register():
    cron_signal.connect(sendMails)
