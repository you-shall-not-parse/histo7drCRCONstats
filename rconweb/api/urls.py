import os
from typing import Callable

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import history_only


@csrf_exempt
def get_api_documentation(request):
    """Auto-generate minimal API documentation through introspection"""
    api_docs = [
        {
            "endpoint": name,
            "arguments": {},
            "return_type": None,
            "doc_string": None,
            "auto_settings_capable": False,
            "permissions_required": [],
            "allowed_http_methods": ["GET"],
        }
        for name, _ in endpoints
    ]

    return history_only.api_response(
        result=sorted(api_docs, key=lambda x: x["endpoint"]),
        command="get_api_documentation",
        failed=False,
    )


endpoints: list[tuple[str, Callable]] = [
    ("get_public_info", history_only.get_public_info),
    ("get_scoreboard_maps", history_only.get_scoreboard_maps),
    ("get_map_scoreboard", history_only.get_map_scoreboard),
]

# Expose endpoints though Django
urlpatterns = [path(name, func, name=name) for name, func in endpoints] + [
    path("get_api_documentation", get_api_documentation, name="get_api_documentation")
]
