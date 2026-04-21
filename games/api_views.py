from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from games.models import Game
from games.permissions import IsCreatorOrReadOnly
from games.serializers import GameSerializer


class GameListAPI(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]

class GameDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsCreatorOrReadOnly]
    lookup_field = 'id'
