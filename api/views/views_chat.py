from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated
)

from authapi.models import User
from ..models import Chat
from ..serializers import (
    ChatSerializer, ChatModelSerializer, ConversationSerializer
)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)

        if serializer.is_valid():
            receiver_user = User.objects.filter(public_id=serializer.data['receiver_id']).first()
            if receiver_user is not None:
                new_chat = Chat(
                    sender=request.user,
                    receiver=receiver_user,
                    message=serializer.data['message'],
                )
                new_chat.save_chat()

                return Response(
                    {
                        'message':  serializer.data['message'],
                        'sent_at': new_chat.sent_at,
                        'receiver': {
                            'first_name': receiver_user.first_name,
                            'last_name': receiver_user.last_name,
                            'public_id': receiver_user.public_id,
                        }
                    }
                )

            else:
                return Response(
                    {
                        "error": True,
                        "message": "User does not exist"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        conversations = Chat.get_conversations(request.user)
        return Response(
            {   
                'total': len(conversations),
                'results': conversations
            }
        )


class ChatList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        con_serializer = ConversationSerializer(data=request.data)

        if con_serializer.is_valid():
            recipient = User.objects.filter(public_id =con_serializer.data['recipient_id']).first()
            chat_serializer = ChatModelSerializer(
                Chat.get_conversation(recipient, request.user),
                many=True
            )

            return Response(
                {
                    "total": len(chat_serializer.data),
                    "results": chat_serializer.data
                }
            )
        
        else:
            return Response(
                con_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
