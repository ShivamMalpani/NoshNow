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
            "view_restaurant": reverse(
                "view_restaurant", args=[1], request=request, format=format
            ),
            "add_cart": reverse(
                "add_cart", request=request, format=format
            ),
            "clear_cart": reverse(
                "clear_cart", request=request, format=format
            ),
            "view_cart": reverse(
                "view_cart", args=[1], request=request, format=format
            ),
            "add_item": reverse(
                "add_item", request=request, format=format
            ),
            "update_item": reverse(
                "update_item", request=request, format=format
            ),
            "delete_item": reverse(
                "delete_item", request=request, format=format
            ),
            "view_item": reverse(
                "view_item", args=[1], request=request, format=format
            ),
            "update_item_status": reverse(
                "update_item_status", request=request, format=format
            ),
            "update_item_quantity": reverse(
                "update_item_quantity", request=request, format=format
            ),
            "create_order": reverse(
                "create_order", request=request, format=format
            ),
            "cancel_order": reverse(
                "cancel_order", request=request, format=format
            ),
            "view_order_history": reverse(
                "view_order_history", args=[1], request=request, format=format
            ),
            "view_order": reverse(
                "view_order", args=[1, 1], request=request, format=format
            ),
        }
    )