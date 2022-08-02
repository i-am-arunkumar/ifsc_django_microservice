from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.cache import cache

class IFSCTestCase(APITestCase):
   
    def test_ifsc_slug(self):
        url = reverse('ifsc',args=('SBIN0000002',))
        cache.clear()
        
        #first hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_SBIN0000002")
        result = response.data["result"]
        assert response.status_code == 200
        assert api_hit == 1
        assert result["ifsc"] == "SBIN0000002"
        assert result["bank"] == "STATE BANK OF INDIA"
        assert result["micr_code"] == "799002002"
        assert result["branch"] == "AGARTALA"
        assert result["district"] == "WEST TRIPURA"
        assert result["address"] == "H.G.BASAK RD., AGARTALA, TRIPURA-779001"
        assert result["city"] == "AGARTALA"
        assert result["state"] == "TRIPURA"

        #second hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_SBIN0000002")
        cache_hit = cache.get("hits_SBIN0000002")
        result = response.data["result"]
        assert api_hit == 1
        assert cache_hit == 1
        assert response.status_code == 200
        assert result["ifsc"] == "SBIN0000002"
        assert result["bank"] == "STATE BANK OF INDIA"
        assert result["micr_code"] == "799002002"
        assert result["branch"] == "AGARTALA"
        assert result["district"] == "WEST TRIPURA"
        assert result["address"] == "H.G.BASAK RD., AGARTALA, TRIPURA-779001"
        assert result["city"] == "AGARTALA"
        assert result["state"] == "TRIPURA"        

    
    def test_leaderboard(self):
        url = reverse('leaderboard')
        cache.clear()

        #first hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_leaderboard")
        assert response.status_code == 200
        assert api_hit == 1

        #second hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_leaderboard")
        cache_hit = cache.get("hits_leaderboard")
        assert response.status_code == 200
        assert api_hit == 1
        assert cache_hit == 1
        
        

    def test_statistics(self):
        url = reverse('statistics')
        cache.clear()

        #first hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_statistics")
        assert response.status_code == 200
        assert api_hit == 1

        #second hit
        response = self.client.get(url)
        api_hit = cache.get("hits_api_statistics")
        cache_hit = cache.get("hits_statistics")
        assert response.status_code == 200
        assert api_hit == 1
        assert cache_hit == 1
        
