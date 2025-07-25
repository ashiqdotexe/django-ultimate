from rest_framework.test import APIClient
from rest_framework import status
import pytest
@pytest.mark.django_db
class TestCollection:
    def test_if_user_is_anonymous_return_404(self):
        client = APIClient()
        response=client.post("/store/collections/", {"title":"A"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED