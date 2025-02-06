import aiohttp
from typing import Dict, List, Optional
from app.config import DATA_CRUD_SERVICE_URL


class DataCRUDClient:
    def __init__(self):
        self.base_url = DATA_CRUD_SERVICE_URL

    async def create_applicant(self, applicant_data: Dict) -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/applicants/", json=applicant_data
            ) as response:
                if response.status == 201:
                    return await response.json()
                return None

    async def update_applicant(
        self, applicant_id: str, applicant_data: Dict
    ) -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.base_url}/applicants/{applicant_id}", json=applicant_data
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def create_transactions(
        self, applicant_id: str, transactions: List[Dict]
    ) -> Optional[List[Dict]]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/applicants/{applicant_id}/transactions/bulk/",
                json=transactions,
            ) as response:
                if response.status == 201:
                    return await response.json()
                return None

    async def create_kfi(self, applicant_id: str, kfi_data: Dict) -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/applicants/{applicant_id}/kfis/", json=kfi_data
            ) as response:
                if response.status == 201:
                    return await response.json()
                return None

    async def get_applicant(self, applicant_id: str) -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/applicants/{applicant_id}"
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
