from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import read_all, write_all
from .serializers import VideoSerializer


class VideoListCreate(APIView):
    def get(self, request):
        items = read_all()
        sort_by = request.GET.get("sort_by")
        order = request.GET.get("order", "asc")
        if sort_by:
            if sort_by not in VideoSerializer().fields:
                return Response(
                    {"detail": f"Invalid sort_by '{sort_by}'"},
                    status=400)
            items.sort(key=lambda x: x[sort_by], reverse=(order == "desc"))
        return Response(items)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new = serializer.validated_data
        items = read_all()
        if any(v["source_post_id"] == new["source_post_id"] for v in items):
            return Response({"source_post_id": ["must be unique"]}, status=400)
        items.append(new)
        write_all(items)
        return Response(new, status=status.HTTP_201_CREATED)


class VideoDetail(APIView):
    def get_obj(self, pk):
        items = read_all()
        for v in items:
            if v["source_post_id"] == pk:
                return v, items
        return None, items

    def put(self, request, pk):
        existing, items = self.get_obj(pk)
        if not existing:
            return Response(status=404)
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.validated_data
        # replace
        items = [updated if v["source_post_id"] == pk else v for v in items]
        write_all(items)
        return Response(updated)

    def delete(self, request, pk):
        _, items = self.get_obj(pk)
        new_list = [v for v in items if v["source_post_id"] != pk]
        if len(new_list) == len(items):
            return Response(status=404)
        write_all(new_list)
        return Response(status=204)
