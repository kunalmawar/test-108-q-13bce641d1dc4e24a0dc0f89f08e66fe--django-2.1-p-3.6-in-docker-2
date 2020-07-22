# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.username


class FriendRequests(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reciever')
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return 'User1: %s, User2: %s, Is_Friends: %s' % (self.user1.username, self.user2.username, self.is_complete)