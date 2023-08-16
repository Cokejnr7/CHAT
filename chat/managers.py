from django.db import models


class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        threads = self.get_queryset().filter(thread_type="p")
        threads = threads.filter(users__in=[user1, user2]).distinct()

        if threads.exists():
            return threads.first()

        else:
            threads = self.create(thread_type="p")
            threads.users.add(user1)
            threads.users.add(user2)
