from django.contrib.auth.models import User
# importing signal
from django.db.models.signals import post_save


# receiver function
def check_user_created(sender, instance, **kwargs):
    print('User is Created ')


# When the signal sends its message, each connected receiver gets called
post_save.connect(check_user_created, sender=User)
