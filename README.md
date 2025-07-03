# HappiestBaby API Client

A comprehensive Python API client for HappiestBaby devices and services, including Snoo Smart Sleeper control and complete baby tracking functionality. This client provides full access to the HappiestBaby ecosystem through their mobile app API.

## Fork Acknowledgment

This project builds upon the excellent work of the original [pysnoo](https://github.com/rado0x54/pysnoo) module by rado0x54. We've significantly extended it with:
- Complete baby journal/tracking functionality for all data types
- AWS Cognito authentication support
- Updated API endpoints for HappiestBaby app v2.6.1+
- Comprehensive CRUD operations for all journal types (feeding, diaper, weight, height, etc.)
- Enhanced device management and session tracking

# [Homeassistant](https://home-assistant.io)
[Homeassistant](https://home-assistant.io) has a [custom Snoo component](https://github.com/sanghviharshit/ha-snoo) leveraging this package.
This can be added into HACS as a custom repository.

# Getting Started

## Installation

This comprehensive HappiestBaby API client can be installed directly from this repository:

```bash
# Install directly from GitHub
pip install git+https://github.com/astaniforth/happiestbaby-api.git

# Or clone and install locally for development
git clone https://github.com/astaniforth/happiestbaby-api.git
cd happiestbaby-api
pip install -e .
```

Note: This package replaces and extends the original `pysnoo` package with comprehensive journal functionality and updated authentication.

## Basic Usage

`happiestbaby_api` starts within an [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
`ClientSession`:

```python
import asyncio
from aiohttp import ClientSession

async def main() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      # YOUR CODE HERE

asyncio.get_event_loop().run_until_complete(main())
```

To get all Snoo devices associated with an account:

```python
import asyncio
from aiohttp import ClientSession
import happiestbaby_api

async def main() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      snoo = await happiestbaby_api.login('<EMAIL>', '<PASSWORD>', websession)

      # Returns snoo devices
      devices = snoo.devices
      # >>> {"serial_number123": <Device>, "serial_number456": <Device>}

asyncio.get_event_loop().run_until_complete(main())
```

## Journal Functionality (NEW)

This fork adds comprehensive baby journal tracking functionality matching the HappiestBaby mobile app:

### Supported Journal Types
- **Diaper Changes**: Track wet/dirty diapers with types (pee, poo)
- **Feeding**: 
  - Bottle feeding (breast milk or formula) with amounts in oz/ml
  - Breast feeding with duration tracking per breast
- **Growth Measurements**:
  - Weight tracking (oz/grams)
  - Height tracking (inches/cm)
  - Head circumference (inches/cm)

### Journal Examples

```python
import asyncio
from datetime import datetime, timedelta
from happiestbaby_api import login

async def journal_examples():
    """Examples of journal functionality."""
    # Login
    api = await login('<EMAIL>', '<PASSWORD>')
    
    # Get baby ID (if you have multiple babies, choose appropriately)
    babies = await api.get_account()
    baby_id = babies[0]['id']
    
    # Create a diaper entry
    diaper_entry = await api.journal.create_diaper_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        diaper_types=['pee', 'poo'],  # Use 'poo' not 'poop'
        note="Normal diaper change"
    )
    
    # Create a bottle feeding entry
    feeding_entry = await api.journal.create_feeding_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        feeding_type='bottlefeeding',
        amount_imperial=4.0,  # 4 oz (automatically converts to ml)
        milk_type='breastmilk',  # or 'formula'
        note="Morning feeding"
    )
    
    # Create a breast feeding entry
    breast_entry = await api.journal.create_breast_feeding_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(minutes=20),
        left_duration=600,  # 10 minutes in seconds
        right_duration=600,  # 10 minutes in seconds
        last_used_breast='right',
        note="Bedtime feeding"
    )
    
    # Track weight
    weight_entry = await api.journal.create_weight_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        weight_imperial=10.5,  # 10.5 oz (automatically converts to grams)
        note="Weekly weigh-in"
    )
    
    # Track height
    height_entry = await api.journal.create_height_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        height_imperial=22.0,  # 22 inches (automatically converts to cm)
        note="Monthly measurement"
    )
    
    # Track head circumference
    head_entry = await api.journal.create_head_entry(
        baby_id=baby_id,
        start_time=datetime.now(),
        circumference_imperial=16.5,  # 16.5 inches (automatically converts to cm)
        note="Pediatrician visit"
    )
    
    # Read journal entries
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    diaper_entries = await api.journal.get_diaper_tracking(baby_id, start_date, end_date)
    feeding_entries = await api.journal.get_feeding_tracking(baby_id, start_date, end_date, 'bottlefeeding')
    weight_entries = await api.journal.get_weight_tracking(baby_id, start_date, end_date)
    
    # Update a journal entry (requires complete object)
    if diaper_entries:
        entry = diaper_entries[0]
        await api.journal.update_journal_entry(
            entry_id=entry['id'],
            updates={
                'type': entry['type'],
                'startTime': entry['startTime'],
                'babyId': entry['babyId'],
                'userId': entry['userId'],
                'data': entry['data'],
                'note': 'Updated note'
            }
        )
    
    # Delete a journal entry
    await api.journal.delete_journal_entry(entry['id'])

asyncio.run(journal_examples())
```

## API Methods

These are coroutines and need to be `await`ed – see `example.py` for examples.

### Core Authentication & Device Methods
* `login`: Login method that authenticates user and also updates device information
* `authenticate`: Authenticate (or re-authenticate) to Snoo. Call this to
  re-authenticate immediately after changing username and/or password otherwise
  new username/password will only be used when token has to be refreshed.
* `get_account`: Retrieve account details
* `update_device_info`: Retrieve info and status for devices including account, baby, config and session
* `get_session_for_account`: Retrieve session details for the account
* `get_configs_for_device`: Retrieve config details for the devices
* `get_baby_for_account`: Retrieve baby details associated with the account
* `get_session_stats_avg_for_account`: Retrieve aggregated session stats for the week
* `get_session_stats_daily_for_account`: Retrieve aggregated session stats for the given date

### Journal Methods (NEW)
All journal methods are available through `api.journal`:

#### Read Operations
* `get_diaper_tracking(baby_id, start_date, end_date)`: Get diaper entries
* `get_feeding_tracking(baby_id, start_date, end_date, feeding_type)`: Get feeding entries
* `get_weight_tracking(baby_id, start_date, end_date)`: Get weight entries
* `get_height_tracking(baby_id, start_date, end_date)`: Get height entries
* `get_head_tracking(baby_id, start_date, end_date)`: Get head circumference entries
* `get_pumping_tracking(baby_id, start_date, end_date)`: Get pumping entries
* `get_grouped_tracking(baby_id, start_date, end_date)`: Get all journal entries grouped
* `get_last_journals(baby_id)`: Get the most recent journal entries

#### Create Operations
* `create_diaper_entry(baby_id, start_time, diaper_types, note=None, user_id=None)`
* `create_feeding_entry(baby_id, start_time, feeding_type, amount_imperial=None, amount_metric=None, milk_type='breastmilk', note=None, user_id=None)`
* `create_breast_feeding_entry(baby_id, start_time, end_time, left_duration=None, right_duration=None, last_used_breast='left', note=None, user_id=None)`
* `create_weight_entry(baby_id, start_time, weight_imperial=None, weight_metric=None, note=None, user_id=None)`
* `create_height_entry(baby_id, start_time, height_imperial=None, height_metric=None, note=None, user_id=None)`
* `create_head_entry(baby_id, start_time, circumference_imperial=None, circumference_metric=None, note=None, user_id=None)`

#### Update & Delete Operations
* `update_journal_entry(entry_id, updates)`: Update an entry (requires complete object)
* `delete_journal_entry(entry_id)`: Delete an entry

## Device Methods

All of the routines on the `SnooDevice` class are coroutines and need to be
`await`ed – see `example.py` for examples.

* `update`: get the latest device info (state, etc.). Note that
  this runs api.update_device_info and thus all accounts/devices will be updated

## API Properties

* `account`: dictionary with the account
* `devices`: dictionary with all devices
* `last_state_update`: datetime (in UTC) last state update was retrieved
* `password`: password used for authentication. Can only be set, not retrieved
* `username`: username for authentication.

## Account Properties

* `userId`: User ID for the account
* `email`: Email for the account
* `givenName`: Name for the account
* `surname`: Last name for the account
* `region`: Region for the account

### Example
```
{
    "email": "abc@xyz.com",
    "givenName": "ABC",
    "surname": "XYZ",
    "userId": "afdgjfhdsgsg",
    "region": "US"
}
```

## Session Properties

* `startTime`: datetime when the current or last session started
* `endTime`: datetime when the last session ended or None if current session is active
* `levels`: sequence of levels in current session sorted by time. (Last level is the latest)

### Example
```
{
    "startTime": "2021-02-01T01:02:34.456Z",
    "endTime": "2021-02-01T04:02:34.456Z",
    "levels": [
        {
            "level": "BASELINE"
        },
        {
            "level": "LEVEL1"
        },
        {
            "level": "BASELINE"
        },
        {
            "level": "ONLINE"
        }
    ]
}
```

## Important Notes

### Authentication
This fork uses AWS Cognito authentication which is required for the latest HappiestBaby API. The module handles token refresh automatically.

### Unit Conversions
The journal methods automatically convert between imperial and metric units:
- Weight: oz ↔ grams (1 oz = 28.3495 grams)
- Liquid: oz ↔ ml (1 oz = 29.5735 ml)
- Length: inches ↔ cm (1 inch = 2.54 cm)

### Journal Entry Updates
Journal updates require sending the complete object, not just changed fields. Always include all required fields: `type`, `startTime`, `babyId`, `userId`, `data`, and optionally `note`.

### Rate Limiting
Be mindful of API rate limits. The module includes appropriate delays and error handling, but rapid consecutive requests may be throttled.

# Acknowledgement

The structure of this project is inspired by [pymyq](https://github.com/arraylabs/pymyq) and builds upon the original [pysnoo](https://github.com/rado0x54/pysnoo) module.

# Disclaimer

The code here is based off of an unsupported API from
[happiestbaby.com](https://www.happiestbaby.com/) and is subject to change without
notice. The authors claim no responsibility for damages to your Snoo or
property by use of the code within.