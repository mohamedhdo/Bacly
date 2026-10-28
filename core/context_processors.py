from django.conf import settings
from bacly.services.ai import is_mock_mode_active


def global_context(request):
    """
    Context variables available across all templates.
    """
    return {
        "is_mock_mode": is_mock_mode_active(),
        "app_name": "Bacly",
        "app_tagline": "Your private Bac tutor, in your pocket.",
    }
