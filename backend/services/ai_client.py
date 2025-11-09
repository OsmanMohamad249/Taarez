"""
AI Service Client for communicating with the AI model service.
"""

import httpx
from typing import Dict, Any
from fastapi import UploadFile

from core.config import settings


class AIServiceError(Exception):
    """Custom exception for AI service errors."""

    pass


class AIClient:
    """Client for communicating with the AI model service."""

    def __init__(self):
        self.base_url = settings.AI_SERVICE_URL
        self.timeout = 30.0

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if the AI service is healthy.

        Returns:
            Dict with health status
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise AIServiceError(f"AI service health check failed: {str(e)}")

    async def process_measurements(
        self,
        photo_front: UploadFile,
        photo_back: UploadFile,
        photo_left: UploadFile,
        photo_right: UploadFile,
        height: float,
        weight: float,
    ) -> Dict[str, Any]:
        """
        Send photos and measurements to AI service for processing.

        Args:
            photo_front: Front view photo
            photo_back: Back view photo
            photo_left: Left side photo
            photo_right: Right side photo
            height: User height in cm
            weight: User weight in kg

        Returns:
            Dict with measurement results from AI service

        Raises:
            AIServiceError: If the request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Prepare files for upload
                files = [
                    (
                        "photo_front",
                        (photo_front.filename, await photo_front.read(), photo_front.content_type),
                    ),
                    (
                        "photo_back",
                        (photo_back.filename, await photo_back.read(), photo_back.content_type),
                    ),
                    (
                        "photo_left",
                        (photo_left.filename, await photo_left.read(), photo_left.content_type),
                    ),
                    (
                        "photo_right",
                        (photo_right.filename, await photo_right.read(), photo_right.content_type),
                    ),
                ]

                # Prepare form data
                data = {"height": height, "weight": weight}

                # Make the request
                response = await client.post(
                    f"{self.base_url}/api/measurements/process",
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                return response.json()

            except httpx.HTTPError as e:
                raise AIServiceError(f"AI service request failed: {str(e)}")

    async def validate_photo(self, photo: UploadFile) -> Dict[str, Any]:
        """
        Validate a single photo with the AI service.

        Args:
            photo: Photo to validate

        Returns:
            Dict with validation results

        Raises:
            AIServiceError: If the request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                files = {"photo": (photo.filename, await photo.read(), photo.content_type)}

                response = await client.post(
                    f"{self.base_url}/api/measurements/validate", files=files
                )
                response.raise_for_status()
                return response.json()

            except httpx.HTTPError as e:
                raise AIServiceError(f"Photo validation failed: {str(e)}")


# Singleton instance
ai_client = AIClient()
