"""Journal management for HappiestBaby app."""
import logging
from datetime import datetime
from typing import Dict, List, Optional
from .const import (
    BASE_ENDPOINT,
    JOURNALS_GROUPED_TRACKING_URI,
    JOURNALS_TRACKING_URI,
    JOURNALS_CREATE_URI,
    LAST_PUMPING_JOURNAL_URI,
    PUMPING_JOURNALS_TRACKING_URI,
    LAST_JOURNALS_URI,
    JOURNAL_TYPES,
    DIAPER_TYPES,
    FEEDING_TYPES
)

_LOGGER = logging.getLogger(__name__)


class JournalManager:
    """Manage baby journal entries and tracking data."""

    def __init__(self, api):
        """Initialize journal manager with API reference."""
        self.api = api

    async def get_grouped_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime,
        group: str = "activity"
    ) -> Optional[List[Dict]]:
        """Get grouped tracking data for a date range.

        Args:
            baby_id: Baby ID
            from_datetime: Start datetime
            to_datetime: End datetime
            group: Group type (default: "activity")

        Returns:
            List of grouped journal entries
        """
        params = {
            "fromDateTime": from_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "toDateTime": to_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "group": group
        }

        _LOGGER.debug(f"Getting grouped tracking for baby {baby_id}")
        _, response = await self.api.request(
            method="get",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_GROUPED_TRACKING_URI.format(baby_id=baby_id)}",
            params=params
        )

        return response

    async def get_journal_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime,
        journal_type: str
    ) -> Optional[List[Dict]]:
        """Get journal tracking data by type.

        Args:
            baby_id: Baby ID
            from_datetime: Start datetime
            to_datetime: End datetime
            journal_type: Type of journal (diaper, bottlefeeding, etc.)

        Returns:
            List of journal entries for the specified type
        """
        params = {
            "fromDateTime": from_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "toDateTime": to_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "journalType": journal_type
        }

        _LOGGER.debug(f"Getting {journal_type} tracking for baby {baby_id}")
        _, response = await self.api.request(
            method="get",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_TRACKING_URI.format(baby_id=baby_id)}",
            params=params
        )

        return response

    async def get_diaper_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get diaper change tracking data."""
        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, JOURNAL_TYPES['DIAPER']
        )

    async def get_feeding_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime,
        feeding_type: str = "bottlefeeding"
    ) -> Optional[List[Dict]]:
        """Get feeding tracking data.

        Args:
            baby_id: Baby ID
            from_datetime: Start datetime
            to_datetime: End datetime
            feeding_type: Type of feeding (bottlefeeding, breastfeeding)
        """
        if feeding_type not in [JOURNAL_TYPES['BOTTLE_FEEDING'], JOURNAL_TYPES['BREAST_FEEDING']]:
            raise ValueError(f"Invalid feeding type: {feeding_type}")

        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, feeding_type
        )

    async def get_weight_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get weight tracking data."""
        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, JOURNAL_TYPES['WEIGHT']
        )

    async def get_height_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get height tracking data."""
        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, JOURNAL_TYPES['HEIGHT']
        )

    async def get_head_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get head circumference tracking data."""
        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, JOURNAL_TYPES['HEAD']
        )

    async def get_solid_food_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get solid food tracking data."""
        return await self.get_journal_tracking(
            baby_id, from_datetime, to_datetime, JOURNAL_TYPES['SOLID_FOOD']
        )

    async def get_pumping_tracking(
        self,
        baby_id: str,
        from_datetime: datetime,
        to_datetime: datetime
    ) -> Optional[List[Dict]]:
        """Get pumping session tracking data."""
        params = {
            "fromDateTime": from_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "toDateTime": to_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }

        _LOGGER.debug("Getting pumping tracking data")
        _, response = await self.api.request(
            method="get",
            returns="json",
            url=f"{BASE_ENDPOINT}{PUMPING_JOURNALS_TRACKING_URI}",
            params=params
        )

        return response

    async def get_last_pumping_journal(self) -> Optional[Dict]:
        """Get the last pumping journal entry."""
        _LOGGER.debug("Getting last pumping journal")
        _, response = await self.api.request(
            method="get",
            returns="json",
            url=f"{BASE_ENDPOINT}{LAST_PUMPING_JOURNAL_URI}"
        )

        return response

    async def get_last_journals(self, baby_id: str) -> Optional[List[Dict]]:
        """Get the most recent journal entries for a baby."""
        _LOGGER.debug(f"Getting last journals for baby {baby_id}")
        _, response = await self.api.request(
            method="get",
            returns="json",
            url=f"{BASE_ENDPOINT}{LAST_JOURNALS_URI.format(baby_id=baby_id)}"
        )

        return response

    async def create_diaper_entry(
        self,
        baby_id: str,
        start_time: datetime,
        diaper_types: List[str],
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new diaper change entry.

        Args:
            baby_id: Baby ID
            start_time: When the diaper change occurred
            diaper_types: List of diaper types (pee, poop)
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        for diaper_type in diaper_types:
            if diaper_type not in DIAPER_TYPES:
                raise ValueError(f"Invalid diaper type: {diaper_type}")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        data = {
            "type": JOURNAL_TYPES['DIAPER'],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "types": diaper_types
            }
        }

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating diaper entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def create_feeding_entry(
        self,
        baby_id: str,
        start_time: datetime,
        feeding_type: str,
        amount_imperial: Optional[float] = None,
        amount_metric: Optional[float] = None,
        milk_type: str = "breastmilk",
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new feeding entry.

        Args:
            baby_id: Baby ID
            start_time: When feeding occurred
            feeding_type: Type (bottlefeeding, breastfeeding)
            amount_imperial: Amount in oz (for bottle feeding)
            amount_metric: Amount in ml (for bottle feeding) - auto-calculated if not provided
            milk_type: Type of milk (breastmilk, formula)
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        if feeding_type not in [JOURNAL_TYPES['BOTTLE_FEEDING'], JOURNAL_TYPES['BREAST_FEEDING']]:
            raise ValueError(f"Invalid feeding type: {feeding_type}")

        if milk_type not in FEEDING_TYPES:
            raise ValueError(f"Invalid milk type: {milk_type}")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        # For bottle feeding, ensure both imperial and metric amounts are provided
        if feeding_type == JOURNAL_TYPES['BOTTLE_FEEDING']:
            if amount_imperial is None and amount_metric is None:
                raise ValueError("Either amount_imperial or amount_metric must be provided for bottle feeding")

            # Convert between units if one is missing
            if amount_imperial is not None and amount_metric is None:
                amount_metric = round(amount_imperial * 29.5735, 2)  # oz to ml
            elif amount_metric is not None and amount_imperial is None:
                amount_imperial = round(amount_metric / 29.5735, 2)  # ml to oz

        data = {
            "type": feeding_type,
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "type": milk_type
            }
        }

        # Add amounts for bottle feeding
        if feeding_type == JOURNAL_TYPES['BOTTLE_FEEDING']:
            if amount_imperial is not None:
                data["data"]["amountImperial"] = amount_imperial
            if amount_metric is not None:
                data["data"]["amountMetric"] = amount_metric

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating {feeding_type} entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def create_weight_entry(
        self,
        baby_id: str,
        start_time: datetime,
        weight_imperial: Optional[float] = None,
        weight_metric: Optional[float] = None,
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new weight entry.

        Args:
            baby_id: Baby ID
            start_time: When weight was measured
            weight_imperial: Weight in oz
            weight_metric: Weight in grams - auto-calculated if not provided
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        if weight_imperial is None and weight_metric is None:
            raise ValueError("Either weight_imperial or weight_metric must be provided")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        # Convert between units if one is missing
        if weight_imperial is not None and weight_metric is None:
            weight_metric = round(weight_imperial * 28.3495, 2)  # oz to grams
        elif weight_metric is not None and weight_imperial is None:
            weight_imperial = round(weight_metric / 28.3495, 2)  # grams to oz

        data = {
            "type": JOURNAL_TYPES['WEIGHT'],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "weightImperial": weight_imperial,
                "weightMetric": weight_metric
            }
        }

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating weight entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def update_journal_entry(
        self,
        entry_id: str,
        updates: Dict
    ) -> Optional[Dict]:
        """Update an existing journal entry.

        Note: The API requires a complete object for PUT requests, not just changed fields.
        If you provide only partial updates, this method will fetch the current entry first
        and merge your updates into the complete object.

        Args:
            entry_id: ID of the journal entry to update
            updates: Dictionary of fields to update (can be partial or complete object)

        Returns:
            Updated journal entry
        """
        _LOGGER.debug(f"Updating journal entry {entry_id}")

        # If updates looks like a complete object (has required fields), use as-is
        required_fields = ['type', 'startTime', 'babyId', 'userId', 'data']
        is_complete = all(field in updates for field in required_fields)

        if is_complete:
            # Complete object provided, use directly
            payload = updates
        else:
            # Partial updates provided, need to fetch current entry and merge
            # For now, we'll require complete objects since fetching current entry
            # would require implementing a get_journal_entry method
            raise ValueError(
                "Partial updates not supported yet. Please provide a complete journal entry object "
                "with fields: type, startTime, babyId, userId, data, and optionally note"
            )

        _, response = await self.api.request(
            method="put",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}/{entry_id}",
            json=payload
        )

        return response

    async def delete_journal_entry(self, entry_id: str) -> bool:
        """Delete a journal entry.

        Args:
            entry_id: ID of the journal entry to delete

        Returns:
            True if successful
        """
        _LOGGER.debug(f"Deleting journal entry {entry_id}")
        _, response = await self.api.request(
            method="delete",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}/{entry_id}"
        )

        return response is not None

    async def create_height_entry(
        self,
        baby_id: str,
        start_time: datetime,
        height_imperial: Optional[float] = None,
        height_metric: Optional[float] = None,
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new height entry.

        Args:
            baby_id: Baby ID
            start_time: When height was measured
            height_imperial: Height in inches
            height_metric: Height in cm - auto-calculated if not provided
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        if height_imperial is None and height_metric is None:
            raise ValueError("Either height_imperial or height_metric must be provided")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        # Convert between units if one is missing
        if height_imperial is not None and height_metric is None:
            height_metric = round(height_imperial * 2.54, 2)  # inches to cm
        elif height_metric is not None and height_imperial is None:
            height_imperial = round(height_metric / 2.54, 2)  # cm to inches

        data = {
            "type": JOURNAL_TYPES['HEIGHT'],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "heightImperial": height_imperial,
                "heightMetric": height_metric
            }
        }

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating height entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def create_head_entry(
        self,
        baby_id: str,
        start_time: datetime,
        circumference_imperial: Optional[float] = None,
        circumference_metric: Optional[float] = None,
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new head circumference entry.

        Args:
            baby_id: Baby ID
            start_time: When head circumference was measured
            circumference_imperial: Head circumference in inches
            circumference_metric: Head circumference in cm - auto-calculated if not provided
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        if circumference_imperial is None and circumference_metric is None:
            raise ValueError("Either circumference_imperial or circumference_metric must be provided")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        # Convert between units if one is missing
        if circumference_imperial is not None and circumference_metric is None:
            circumference_metric = round(circumference_imperial * 2.54, 2)  # inches to cm
        elif circumference_metric is not None and circumference_imperial is None:
            circumference_imperial = round(circumference_metric / 2.54, 2)  # cm to inches

        data = {
            "type": JOURNAL_TYPES['HEAD'],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "circumferenceImperial": circumference_imperial,
                "circumferenceMetric": circumference_metric
            }
        }

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating head circumference entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def create_breast_feeding_entry(
        self,
        baby_id: str,
        start_time: datetime,
        end_time: datetime,
        left_duration: Optional[int] = None,
        right_duration: Optional[int] = None,
        last_used_breast: str = "left",
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Optional[Dict]:
        """Create a new breast feeding entry.

        Args:
            baby_id: Baby ID
            start_time: When feeding started
            end_time: When feeding ended
            left_duration: Duration on left breast in seconds
            right_duration: Duration on right breast in seconds
            last_used_breast: Which breast was used last (left/right)
            note: Optional note
            user_id: User ID (will be auto-detected if not provided)

        Returns:
            Created journal entry
        """
        if last_used_breast not in ['left', 'right']:
            raise ValueError("last_used_breast must be 'left' or 'right'")

        # Auto-detect user ID if not provided
        if not user_id:
            user_id = await self._get_user_id(baby_id)

        # Calculate total duration
        total_duration = 0
        if left_duration:
            total_duration += left_duration
        if right_duration:
            total_duration += right_duration

        data = {
            "type": JOURNAL_TYPES['BREAST_FEEDING'],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endTime": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "babyId": baby_id,
            "userId": user_id,
            "data": {
                "lastUsedBreast": last_used_breast,
                "totalDuration": total_duration
            }
        }

        # Add breast-specific durations
        if left_duration is not None:
            data["data"]["left"] = {"duration": left_duration}
        if right_duration is not None:
            data["data"]["right"] = {"duration": right_duration}

        if note:
            data["note"] = note

        _LOGGER.debug(f"Creating breast feeding entry for baby {baby_id}")
        _, response = await self.api.request(
            method="post",
            returns="json",
            url=f"{BASE_ENDPOINT}{JOURNALS_CREATE_URI}",
            json=data
        )

        return response

    async def _get_user_id(self, baby_id: str) -> str:
        """Get user ID by looking up from existing journal entries.

        Args:
            baby_id: Baby ID to get journals for

        Returns:
            User ID string
        """
        try:
            # Try to get from recent diaper entries
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            diaper_entries = await self.get_diaper_tracking(baby_id, start_date, end_date)
            if diaper_entries and len(diaper_entries) > 0:
                user_id = diaper_entries[0].get('userId')
                if user_id:
                    return user_id

            # No user ID found in recent entries
            raise ValueError("Could not auto-detect user ID. Please provide user_id parameter.")

        except Exception as e:
            _LOGGER.error(f"Error getting user ID: {e}")
            raise ValueError(f"Could not auto-detect user ID: {e}. Please provide user_id parameter.")
