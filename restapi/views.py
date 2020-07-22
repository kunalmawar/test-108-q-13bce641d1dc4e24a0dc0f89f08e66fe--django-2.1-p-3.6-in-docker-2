# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restapi.models import *


class UserAPIView(APIView):

    def post(self, request):
        """
        To create user
        """
        username = request.data.get('username', None)
        error_flag = False
        error_msg = ''
        #print(username)
        if username and len(username)<50:
            username = username.lower()
            user, created = UserProfile.objects.get_or_create(username=username)
            if not created:
                error_flag = True
                error_msg = 'user already exists'
        else:
            error_flag = True
            error_msg = 'username missing or name too long'
        if not error_flag:
            return Response({'username': username}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'failure', 'reason': error_msg}, status=status.HTTP_400_BAD_REQUEST)


class SendFriendRequest(APIView):

    def post(self, request, userA, userB):
        """
        To send friend request
        """
        error_flag = False
        error_msg = ''
        # Ideally parameters should come in request data instead of url as it is a post request
        # print(userA, userB)
        if userA and userB:
            userA = userA.lower()
            userB = userB.lower()
            user1 = UserProfile.objects.filter(username=userA)
            user2 = UserProfile.objects.filter(username=userB)
            if user1 and user2:
                frnreq1 = FriendRequests.objects.filter(user1=user1[0], user2=user2[0])
                frnreq2 = FriendRequests.objects.filter(user1=user2[0], user2=user1[0])
                if (frnreq1 and frnreq1[0].is_complete) or (frnreq2 and frnreq2[0].is_complete):
                    error_flag = True
                    error_msg = 'users are already friends'
                elif frnreq1 and not frnreq1[0].is_complete:
                    error_flag = True
                    error_msg = 'friend request already sent'
                elif frnreq2 and not frnreq2[0].is_complete:
                    # Both of them are now friends
                    #print('Both of them are now friends')
                    frnreq = frnreq2[0]
                    frnreq.is_complete = True
                    frnreq.save()
                elif not frnreq1 and not frnreq2:
                    # Valid friend request
                    #print('Valid friend request')
                    FriendRequests.objects.create(user1=user1[0], user2=user2[0])
            else:
                error_flag = True
                error_msg = 'at least one of the user is invalid'
        else:
            error_flag = True
            error_msg = 'at least one of the user is missing'
        if not error_flag:
            return Response({'status': 'success'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'status': 'failure', 'reason': error_msg}, status=status.HTTP_400_BAD_REQUEST)


class GetPendingRequests(APIView):

    def get(self, request, userA):
        """
        To get all pending requests sent to a user
        """
        if userA:
            userA = userA.lower()
            user = UserProfile.objects.filter(username=userA)
            if user:
                frn_req = FriendRequests.objects.filter(user2=user[0], is_complete=False)
                if frn_req:
                    request_list = frn_req.values_list('user1__username', flat=True)
                    return Response({'friend_requests': request_list}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'failure', 
                        'reason': 'pending requests not found'
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'failure', 'reason': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failure', 'reason': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'friend_requests': request_list}, status=status.HTTP_202_ACCEPTED)


class GetAllFriends(APIView):

    def get(self, request, userA):
        """
        To get all friends of a user
        """
        frn_list = []
        if userA:
            userA = userA.lower()
            user = UserProfile.objects.filter(username=userA)
            if user:
                frnreq1 = FriendRequests.objects.filter(user1=user[0], is_complete=True)
                frnreq2 = FriendRequests.objects.filter(user2=user[0], is_complete=True)
                if frnreq1 or frnreq2:
                    frn_list += frnreq1.values_list('user2__username', flat=True)
                    frn_list += frnreq2.values_list('user1__username', flat=True)
                    return Response({'friends': frn_list}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'failure', 
                        'reason': 'friends not found'
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'failure', 'reason': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failure', 'reason': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'friend_requests': request_list}, status=status.HTTP_202_ACCEPTED)


class GetAllFriendSuggestions(APIView):

    def get(self, request, userA):
        """
        To get all friends of a user
        """
        suggestion_list = []
        if userA:
            userA = userA.lower()
            user = UserProfile.objects.filter(username=userA)
            if user:
                # finding direct friends first
                direct_frn_list = []
                direct_frns1 = FriendRequests.objects.filter(user1=user[0], is_complete=True)
                direct_frns2 = FriendRequests.objects.filter(user2=user[0], is_complete=True)
                if direct_frns1 or direct_frns2:
                    direct_frn_list += direct_frns1.values_list('user2__username', flat=True)
                    direct_frn_list += direct_frns2.values_list('user1__username', flat=True)
                    # Finding first degree people
                    first_degree_frns = []
                    for dfl in direct_frn_list:
                        first_deg_frns1 = FriendRequests.objects.filter(
                            user1__username=dfl, is_complete=True).exclude(user2__username=userA)
                        first_deg_frns2 = FriendRequests.objects.filter(
                            user2__username=dfl, is_complete=True).exclude(user1__username=userA)
                        if first_deg_frns1 or first_deg_frns2:
                            first_degree_frns += first_deg_frns1.values_list('user2__username', flat=True)
                            first_degree_frns += first_deg_frns2.values_list('user1__username', flat=True)
                    # Finding second degree people
                    second_degree_frns = []
                    for fdf in first_degree_frns:
                        sec_deg_frns1 = FriendRequests.objects.filter(
                            user1__username=fdf, is_complete=True).exclude(user2__username__in=[userA]+direct_frn_list)
                        sec_deg_frns2 = FriendRequests.objects.filter(
                            user2__username=fdf, is_complete=True).exclude(user1__username__in=[userA]+direct_frn_list)
                        if sec_deg_frns1 or sec_deg_frns2:
                            second_degree_frns += sec_deg_frns1.values_list('user2__username', flat=True)
                            second_degree_frns += sec_deg_frns2.values_list('user1__username', flat=True)
                suggestion_list = first_degree_frns + second_degree_frns
                if suggestion_list:
                    return Response({'suggestions': suggestion_list}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'failure', 
                        'reason': 'suggestions not found'
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'failure', 'reason': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'failure', 'reason': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'friend_requests': request_list}, status=status.HTTP_202_ACCEPTED)