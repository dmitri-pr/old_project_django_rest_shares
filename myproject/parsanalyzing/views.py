from parsanalyzing.models import Parsanalyze, BestForBuying
from parsanalyzing.serializers import ParsanalyzeSerializer, BestForBuyingSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics
from rest_framework import renderers


# class ParsanalyzingHighlight(generics.GenericAPIView):
#     queryset = Parsanalyzing.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         parsanalyzing = self.get_object()
#         return Response(parsanalyzing.highlighted)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'parsanalyze': reverse('parsanalyze-list', request=request, format=format),
        'bestforbuying': reverse('bestforbuying-list', request=request, format=format)
    })


class ParsanalyzeList(APIView):
    """
    List all parsanalyze, or create a new snippet.
    """
    def get(self, request, format=None):
        parsanalyze = Parsanalyze.objects.all()
        serializer = ParsanalyzeSerializer(parsanalyze, many=True,
        context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ParsanalyzeSerializer(data=request.data,
        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParsanalyzeDetail(APIView):
    """
    Retrieve, update or delete a parsanalyzing instance.
    """
    def get_object(self, pk):
        try:
            return Parsanalyze.objects.get(pk=pk)
        except Parsanalyze.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        parsanalyze = self.get_object(pk)
        serializer = ParsanalyzeSerializer(parsanalyze,
        context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        parsanalyze = self.get_object(pk)
        serializer = ParsanalyzeSerializer(parsanalyze, data=request.data,
        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        parsanalyze = self.get_object(pk)
        parsanalyze.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ParsanalyzeHighlight(generics.GenericAPIView):
#     queryset = Parsanalyze.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         parsanalyze = self.get_object()
#         return Response(parsanalyze.highlighted)


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'bestforbuying': reverse('bestforbuying-list', request=request, format=format)
#     })


class BestForBuyingList(APIView):
    def get(self, request, format=None):
        bestforbuying = BestForBuying.objects.all()
        serializer = BestForBuyingSerializer(bestforbuying, many=True,
        context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BestForBuyingSerializer(data=request.data,
        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BestForBuyingDetail(APIView):
    def get_object(self, pk):
        try:
            return BestForBuying.objects.get(pk=pk)
        except BestForBuying.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bestforbuying = self.get_object(pk)
        serializer = BestForBuyingSerializer(bestforbuying,
        context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        bestforbuying = self.get_object(pk)
        serializer = BestForBuyingSerializer(bestforbuying, data=request.data,
        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bestforbuying = self.get_object(pk)
        bestforbuying.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)