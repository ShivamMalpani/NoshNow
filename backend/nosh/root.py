from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response(
        {
            "restaurant_list": reverse(
                "restaurant_list", request=request, format=format
            ),
            "item_list": reverse(
                "item_list", args=[1], request=request, format=format
            ),
        }
    )