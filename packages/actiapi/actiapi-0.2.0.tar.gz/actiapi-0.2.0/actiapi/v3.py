"""Client for API V2.

See https://github.com/actigraph/CentrePoint3APIDocumentation.
"""
import logging
from typing import Any, Dict, List, Union

import requests

from actiapi import ActiGraphClient


class ActiGraphClientV3(ActiGraphClient):
    """Client for CentrePoint V3 API."""

    BASE_URL = "https://api.actigraphcorp.com"
    AUTH_API = "https://auth.actigraphcorp.com/connect/token"

    @staticmethod
    def _generate_headers(token: str, raw: bool = False):
        headers = {}
        if not raw:
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def _get_access_token(self, scope: str):
        endpoint = self.AUTH_API
        request_body = {
            "client_id": self.api_access_key,
            "client_secret": self.api_secret_key,
            "scope": scope,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            endpoint, data=request_body, headers=headers, verify=True
        )
        try:
            return response.json()["access_token"]
        except KeyError:
            raise RuntimeError(
                "No access token! Make sure you have API_ACCESS_KEY and API_SECRET_KEY!"
            )

    def get_files(
        self,
        user: Union[int, str],
        study_id: int,
    ) -> List[str]:
        """Return download URLs to raw AVRO files.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        token = self._get_access_token(
            "DataAccess",
        )
        results = self._get_paginated(
            f"/dataaccess/v3/files/studies/{study_id}/subjects/{user}"
            f"/raw-accelerometer?fileFormat=avro&",
            token,
        )

        results = [x["downloadUrl"] for x in results]

        return results

    def get_study_metadata(self, study_id) -> List[Dict[str, Any]]:
        """Save all study metadata to file.

        Parameters
        ----------
        study_id:
            Id of the study
        """
        token = self._get_access_token("CentrePoint")

        results = self._get_paginated(
            f"/centrepoint/v3/Studies/{study_id}/Subjects?", token
        )
        return results

    def get_minute_summary(
        self, user: Union[int, str], study_id: int
    ) -> List[Dict[str, Any]]:
        """Return minute level data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        token = self._get_access_token(
            "Analytics",
        )
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/{user}/MinuteSummaries?", token
        )
        return results

    def get_daily_summary(
        self, user: Union[int, str], study_id: int
    ) -> List[Dict[str, Any]]:
        """Return daily summary data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        token = self._get_access_token(
            "Analytics",
        )
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/{user}/DailyStatistics?", token
        )
        return results

    def _get_paginated(self, request: str, token: str):
        results = []
        offset = 0
        limit = 100
        while True:
            paginated_request = f"{request}offset={offset}&limit={limit}"
            headers = self._generate_headers(token)
            response = requests.get(
                self.BASE_URL + paginated_request,
                headers=headers,
            )
            reply = response.json()
            total_count = reply["totalCount"]

            for item in reply["items"]:
                results.append(item)
            if offset + limit >= total_count:
                break
            offset += limit
        if len(results) == 0:
            logging.error("No raw data found.")
            return []
        return results
