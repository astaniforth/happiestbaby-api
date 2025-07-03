# HappiestBaby API Client

A comprehensive Python API client for HappiestBaby devices and services, including Snoo Smart Sleeper control and complete baby tracking functionality. This client provides full access to the HappiestBaby ecosystem through their mobile app API.

## What's New in This Fork

This project builds upon the excellent work of the original [pysnoo](https://github.com/rado0x54/pysnoo) module by rado0x54 and **significantly expands** it into a comprehensive HappiestBaby ecosystem client.

### 🚀 Major Additions vs Original Fork

| Feature Category | Original pysnoo | This Fork (happiestbaby-api) |
|---|---|---|
| **Device Control** | ✅ Basic Snoo control | ✅ Enhanced device management + session tracking |
| **Authentication** | ❌ Legacy/basic auth | ✅ AWS Cognito authentication with auto-refresh |
| **Baby Journal System** | ❌ None | ✅ **Complete 8-type journal system** |
| **CRUD Operations** | ❌ Read-only device data | ✅ **Full Create/Read/Update/Delete** for all data |
| **Unit Conversions** | ❌ None | ✅ **Automatic imperial ↔ metric** conversions |
| **Data Types Supported** | 1 (device status) | **8+** (diaper, feeding, weight, height, etc.) |
| **API Coverage** | Limited legacy endpoints | **Multiple API versions** (v10, v11, v12) |
| **Date/Time Filtering** | ❌ None | ✅ **Advanced date range filtering** |
| **Error Handling** | Basic | ✅ **Comprehensive error handling + retry logic** |
| **Type Safety** | Minimal | ✅ **Full type hints throughout** |
| **Testing Coverage** | Limited | ✅ **Comprehensive unit + integration tests** |

### 🍼 Complete Baby Journal System
Unlike the original device-only focus, this fork provides **complete baby tracking** functionality matching the HappiestBaby mobile app:

- **8 Journal Types**: Diaper, bottle feeding, breast feeding, solid food, weight, height, head circumference, pumping
- **Full CRUD Operations**: Create, read, update, delete all journal entries
- **Smart Unit Conversion**: Automatic oz↔grams, oz↔ml, inches↔cm conversions
- **Advanced Querying**: Date ranges, filtering, grouping, last entries
- **Real-time Sync**: Mirrors mobile app functionality exactly

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

### Complete Journal System (8 Types Supported)

| Journal Type | Data Tracked | Units Supported | Features |
|---|---|---|---|
| **🧷 Diaper Changes** | Wet/dirty types, timing | N/A | Pee, poo tracking with notes |
| **🍼 Bottle Feeding** | Amount, milk type | oz ↔ ml | Breast milk or formula amounts |
| **🤱 Breast Feeding** | Duration per breast, timing | minutes/seconds | Left/right breast duration tracking |
| **🥄 Solid Food** | Food types, amounts | Various | Solid food introduction tracking |
| **⚖️ Weight Tracking** | Baby weight | oz ↔ grams | Growth monitoring with percentiles |
| **📏 Height Tracking** | Baby length/height | inches ↔ cm | Length/height measurements |
| **🧠 Head Circumference** | Head measurements | inches ↔ cm | Head growth tracking |
| **🍼 Pumping** | Pumped milk amounts | oz ↔ ml | Breast milk pumping sessions |

**Key Features:**
- ✅ **Full CRUD**: Create, read, update, delete all entries
- ✅ **Auto Unit Conversion**: Seamless imperial ↔ metric conversion
- ✅ **Date Range Filtering**: Query by custom date ranges
- ✅ **Bulk Operations**: Get grouped data across all types
- ✅ **Real-time Sync**: Matches HappiestBaby mobile app exactly

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

### Complete Journal API Reference
All journal methods are available through `api.journal` with full CRUD operations:

#### 📊 Read Operations (Query & Retrieve)
| Method | Purpose | Returns |
|---|---|---|
| `get_diaper_tracking(baby_id, start_date, end_date)` | Diaper change history | List of diaper entries |
| `get_feeding_tracking(baby_id, start_date, end_date, feeding_type)` | Feeding history by type | List of feeding entries |
| `get_weight_tracking(baby_id, start_date, end_date)` | Weight measurements | List of weight entries |
| `get_height_tracking(baby_id, start_date, end_date)` | Height/length measurements | List of height entries |
| `get_head_tracking(baby_id, start_date, end_date)` | Head circumference data | List of head circumference entries |
| `get_solid_food_tracking(baby_id, start_date, end_date)` | Solid food introduction | List of solid food entries |
| `get_pumping_tracking(baby_id, start_date, end_date)` | Pumping session data | List of pumping entries |
| `get_grouped_tracking(baby_id, start_date, end_date)` | **All journal data grouped** | Complete journal dataset |
| `get_last_journals(baby_id)` | Most recent entries | Latest entries across all types |

#### ✏️ Create Operations (Add New Entries)
| Method | Purpose | Key Parameters |
|---|---|---|
| `create_diaper_entry(...)` | Log diaper changes | `diaper_types=['pee', 'poo']` |
| `create_feeding_entry(...)` | Log bottle feeding | `amount_imperial/metric`, `milk_type` |
| `create_breast_feeding_entry(...)` | Log nursing sessions | `left_duration`, `right_duration` |
| `create_weight_entry(...)` | Record weight | `weight_imperial/metric` |
| `create_height_entry(...)` | Record height/length | `height_imperial/metric` |
| `create_head_entry(...)` | Record head circumference | `circumference_imperial/metric` |

#### 🔄 Update & Delete Operations
| Method | Purpose | Notes |
|---|---|---|
| `update_journal_entry(entry_id, updates)` | Modify existing entry | Requires complete object |
| `delete_journal_entry(entry_id)` | Remove entry | Permanent deletion |

**Advanced Features:**
- 🔄 **Automatic Unit Conversion**: Pass either imperial or metric, get both
- 📅 **Flexible Date Filtering**: Custom date ranges for all operations
- 🏷️ **Rich Metadata**: Notes, user IDs, timestamps on all entries
- ⚡ **Bulk Operations**: Retrieve all journal types in single calls
- 🔒 **Type Safety**: Full type hints for all parameters and returns

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

## 🚀 Advanced Features & Capabilities

### 🔐 Modern Authentication (AWS Cognito)
- **Secure Authentication**: Uses AWS Cognito for enterprise-grade security
- **Automatic Token Refresh**: Handles token expiration transparently
- **Thread-Safe**: Concurrent request handling with proper locking
- **Error Recovery**: Automatic re-authentication on auth failures

### 🔄 Intelligent Unit Conversions
Automatic bidirectional conversion between measurement systems:
```python
# Pass imperial, get both imperial and metric
weight_entry = await api.journal.create_weight_entry(
    baby_id=baby_id,
    weight_imperial=8.5  # oz
)
# Automatically stores: imperial=8.5oz, metric=241.0g

# Or pass metric, get both
height_entry = await api.journal.create_height_entry(
    baby_id=baby_id, 
    height_metric=55.0  # cm
)
# Automatically stores: metric=55.0cm, imperial=21.65in
```

**Conversion Rates:**
- **Weight**: 1 oz = 28.3495 grams
- **Liquid**: 1 oz = 29.5735 ml  
- **Length**: 1 inch = 2.54 cm

### 📅 Advanced Date & Time Handling
- **Flexible Date Ranges**: Query any custom time period
- **Timezone Aware**: Proper UTC handling with local timezone support
- **ISO 8601 Format**: Standard datetime formatting throughout

### 🔄 Complete CRUD Operations
- **Create**: Add new journal entries with validation
- **Read**: Query with flexible filtering and grouping
- **Update**: Modify existing entries (requires complete object)
- **Delete**: Remove entries permanently

### ⚡ Performance & Reliability
- **Async/Await**: Non-blocking operations throughout
- **Request Retry Logic**: Automatic retry on transient failures
- **Connection Pooling**: Efficient HTTP connection reuse
- **Rate Limit Handling**: Built-in delays and backoff strategies

### 🔒 Type Safety & Developer Experience
- **Full Type Hints**: Complete typing for better IDE support
- **Comprehensive Error Handling**: Specific exceptions for different failure modes
- **Extensive Logging**: Debug-friendly logging throughout
- **Documentation**: Detailed docstrings for all methods

## 🛠️ Developer Notes

### Journal Entry Updates
⚠️ **Important**: Journal updates require sending the complete object, not just changed fields. Always include all required fields: `type`, `startTime`, `babyId`, `userId`, `data`, and optionally `note`.

### Rate Limiting
🚀 The module includes intelligent rate limiting:
- Built-in delays between requests
- Exponential backoff on failures
- Automatic retry logic for transient errors
- Connection pooling for efficiency

### Best Practices
- Use date ranges wisely to avoid large datasets
- Include meaningful notes for better tracking
- Handle errors gracefully with try/catch blocks
- Close sessions properly when done

### Error Handling
The module provides specific exception types:
- `AuthenticationError`: Login/token issues
- `InvalidCredentialsError`: Bad username/password
- `RequestError`: API communication problems
- `SnooError`: General device/API errors

# Acknowledgement

The structure of this project is inspired by [pymyq](https://github.com/arraylabs/pymyq) and builds upon the original [pysnoo](https://github.com/rado0x54/pysnoo) module.

# Disclaimer

The code here is based off of an unsupported API from
[happiestbaby.com](https://www.happiestbaby.com/) and is subject to change without
notice. The authors claim no responsibility for damages to your Snoo or
property by use of the code within.