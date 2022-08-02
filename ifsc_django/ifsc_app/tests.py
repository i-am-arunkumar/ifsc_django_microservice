from django.test import TestCase
from django.urls import reverse
from django.db.models import Count

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ifsc_app.models import IFSC
from ifsc_app.Serializers import IFSCSerializer


class IFSCTestCase(APITestCase):

    def test_ifsc_slug(self):
        url = reverse('ifsc-detail',args=('SBIN0000002',))
        response = self.client.get(url)
        result = response.data["result"]
        assert response.status_code == 200
        assert result["ifsc"] == 'SBIN0000002'
        assert result["bank"] == "STATE BANK OF INDIA"
        assert result["micr_code"] == "799002002"
        assert result["branch"] == "AGARTALA"
        assert result["district"] == "WEST TRIPURA"
        assert result["address"] == "H.G.BASAK RD., AGARTALA, TRIPURA-779001"
        assert result["city"] == "AGARTALA"
        assert result["state"] == "TRIPURA"   
    
    def test_leaderboard(self):
        url = reverse('ifsc-leaderboard')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_statistics(self):
        url = reverse('ifsc-statistics')
        response = self.client.get(url)
        assert response.status_code == 200

