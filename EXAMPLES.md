# 📚 HappiestBaby API Examples & Demonstrations

This directory contains comprehensive examples showcasing the full capabilities of the HappiestBaby API client, demonstrating how this fork extends far beyond the original pysnoo's device-only functionality.

## 🎯 What This Fork Provides vs Original pysnoo

| Feature Category | Original pysnoo | This Fork (happiestbaby-api) |
|---|---|---|
| **Device Control** | ✅ Basic Snoo control | ✅ Enhanced device management + session tracking |
| **Authentication** | ❌ Legacy/basic auth | ✅ **AWS Cognito with auto-refresh** |
| **Baby Journal System** | ❌ None | ✅ **Complete 8-type journal system** |
| **CRUD Operations** | ❌ Read-only device data | ✅ **Full Create/Read/Update/Delete** |
| **Unit Conversions** | ❌ None | ✅ **Automatic imperial ↔ metric** |
| **Data Types Supported** | 1 (device status) | **8+** (all baby tracking data) |
| **API Coverage** | Limited legacy endpoints | **Multiple API versions** (v10, v11, v12) |
| **Date/Time Filtering** | ❌ None | ✅ **Advanced date range filtering** |
| **Error Handling** | Basic | ✅ **Comprehensive error handling + retry logic** |
| **Type Safety** | Minimal | ✅ **Full type hints throughout** |

## 📁 Available Examples

### 1. 📓 `comprehensive_demo.ipynb` - **Interactive Jupyter Notebook**
**Best for**: Learning, experimentation, and interactive exploration

**What it demonstrates:**
- 🔐 **AWS Cognito Authentication** with automatic token refresh
- 📱 **Device Management** for Snoo Smart Sleepers
- 👶 **Baby Profile Management** with proper data structures
- 📝 **Complete 8-Type Journal System**:
  - 🧷 Diaper Changes (pee, poo tracking)
  - 🍼 Bottle Feeding (amounts + milk types)
  - 🤱 Breast Feeding (duration per breast)
  - 🥄 Solid Food (food introduction)
  - ⚖️ Weight Tracking (oz ↔ grams)
  - 📏 Height Tracking (inches ↔ cm)
  - 🧠 Head Circumference (inches ↔ cm)
  - 🍼 Pumping (milk volumes)
- 🔄 **Full CRUD Operations** (Create, Read, Update, Delete)
- 📊 **Advanced Data Querying** with date ranges and filtering
- 🎯 **Real API Testing** with actual journal entry creation

**How to use:**
1. Update credentials in the first cell:
   ```python
   EMAIL = "your-email@example.com"
   PASSWORD = "your-password"
   ```
2. Run all cells
3. Execute with: `await main()`

**Perfect for:**
- First-time users exploring the API
- Developers learning the journal system
- Testing different features interactively
- Understanding the full scope vs original pysnoo

---

## 🚀 Quick Start Guide

### For Jupyter Notebooks (Recommended)

```python
# 1. Install the package
pip install git+https://github.com/astaniforth/happiestbaby-api.git

# 2. In Jupyter, import and setup
from aiohttp import ClientSession
import happiestbaby_api

# 3. Authenticate
async with ClientSession() as websession:
    api = await happiestbaby_api.login('your-email@example.com', 'your-password', websession)
    
    # 4. Use the API
    babies = await api.get_babies()
    devices = api.devices
    
    # 5. Journal operations
    baby_id = babies[0]['_id']
    diaper_entries = await api.journal.get_diaper_tracking(baby_id, start_date, end_date)
```

### For Regular Python Scripts

```python
import asyncio
from aiohttp import ClientSession
import happiestbaby_api

async def main():
    async with ClientSession() as websession:
        api = await happiestbaby_api.login('email', 'password', websession)
        # Your code here...

asyncio.run(main())
```

---

## 📋 Complete Journal System Overview

### 8 Supported Journal Types

| Type | Purpose | Data Tracked | Units |
|------|---------|--------------|-------|
| **Diaper** | Track diaper changes | Wet/dirty types, timing | N/A |
| **Bottle Feeding** | Formula/breast milk bottles | Amount, milk type | oz ↔ ml |
| **Breast Feeding** | Nursing sessions | Duration per breast | minutes/seconds |
| **Solid Food** | Food introduction | Food types, amounts | Various |
| **Weight** | Growth tracking | Baby weight | oz ↔ grams |
| **Height** | Growth tracking | Length/height | inches ↔ cm |
| **Head Circumference** | Development tracking | Head measurements | inches ↔ cm |
| **Pumping** | Milk expression | Pumped volumes | oz ↔ ml |

### CRUD Operations Available

- **✅ CREATE**: Add new entries for all 8 types
- **✅ READ**: Query with date ranges, filtering, grouping
- **✅ UPDATE**: Modify existing entries
- **✅ DELETE**: Remove entries permanently

### Advanced Features

- **🔄 Unit Conversion**: Automatic imperial ↔ metric conversion
- **📅 Date Filtering**: Custom date ranges for all operations
- **📊 Bulk Operations**: Get grouped data across all types
- **🕐 Recent Entries**: Quick access to latest entries
- **🏷️ Rich Metadata**: Notes, timestamps, user tracking

---

## 🛠️ Development Notes

### Authentication
- Uses **AWS Cognito** for enterprise-grade security
- **Automatic token refresh** handled transparently
- **Thread-safe** concurrent operations
- **Error recovery** with automatic re-authentication

### API Endpoints
- **Multiple API versions** supported (v10, v11, v12)
- **Fallback logic** to legacy endpoints when needed
- **Smart endpoint detection** based on available features

### Error Handling
- **Specific exception types** for different error conditions
- **Retry logic** with exponential backoff
- **Comprehensive logging** for debugging
- **Graceful degradation** when features unavailable

### Performance
- **Async/await** throughout for non-blocking operations
- **Connection pooling** for HTTP efficiency
- **Rate limiting** built-in to respect API limits
- **Caching** where appropriate for frequently accessed data

---

## 🆘 Troubleshooting

### Common Issues

**Authentication Errors**
- Verify credentials are correct
- Check if account has 2FA enabled
- Ensure network connectivity

**Journal Operations Failing**
- Verify baby has valid `_id` field (not `id`)
- Check date ranges are reasonable
- Ensure required fields are provided

**API Endpoint Errors**
- Package automatically handles endpoint migrations
- Legacy endpoints used as fallbacks
- Contact maintainer if persistent 404 errors

### Getting Help

1. **Check Examples**: Start with `comprehensive_demo.ipynb`
2. **Review Tests**: Look at `tests/integration/` for patterns
3. **Enable Debug Logging**: Set `logging.basicConfig(level=logging.DEBUG)`
4. **Create Issues**: Report problems on GitHub

---

## 🎉 What Makes This Fork Special

This isn't just an enhanced version of pysnoo—it's a **complete baby tracking ecosystem** that:

- **Matches Commercial Apps**: Provides the same functionality as premium baby tracking apps
- **Production Ready**: Used in real applications with comprehensive error handling
- **Developer Friendly**: Full type hints, extensive documentation, clear examples
- **Future Proof**: Supports multiple API versions with automatic fallbacks
- **Comprehensive**: 8 journal types vs original's device-only focus

**Ready to build the next generation of baby tracking applications!** 🚀