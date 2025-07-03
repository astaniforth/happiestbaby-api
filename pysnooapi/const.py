"""The snoo constants."""

BASE_ENDPOINT = "https://api-us-east-1-prod.happiestbaby.com"
COGNITO_ENDPOINT = "https://cognito-idp.us-east-1.amazonaws.com/"
LOGIN_URI = "/us/v2/login"  # Legacy endpoint - may not work with current API
REFRESH_URI = "/us/v2/refresh"  # Legacy endpoint - may not work with current API
AUTH_DATA_URI = "/us/users/{email}/auth-data"  # New Cognito-based auth endpoint

# Cognito Authentication
COGNITO_CLIENT_ID = "6kqofhc8hm394ielqdkvli0oea"
COGNITO_USER_POOL_ID = "us-east-1_W1CDHvNWi"
COGNITO_REGION = "us-east-1"
DEVICES_URI = "/me/devices"
ACCOUNT_URI = "/us/me"
BABY_URI = "/us/v3/me/baby"
SESSION_URI = "/analytics/sessions/last"
SESSION_STATS_DAILY_URI = "/ss/v2/babies/{baby_id}/sessions/aggregated/daily"
SESSION_STATS_AVG_URI = "/ss/v2/babies/{baby_id}/sessions/aggregated/avg"
DEVICE_CONFIGS_URI = "/ds/devices/{serial_number}/configs"

# Updated API endpoints based on latest logs
BABIES_URI = "/us/me/v10/babies"
ACCOUNT_V10_URI = "/us/me/v10/me"
SETTINGS_URI = "/us/me/v10/settings"
LEGAL_CHECK_URI = "/us/me/v10/legal/check"
APP_SETTINGS_URI = "/us/v1/app-settings/target-version/ios"

# Device endpoints
DEVICES_V10_URI = "/hds/me/v10/devices"
DEVICES_V11_URI = "/hds/me/v11/devices"

# Sleep session endpoints
SESSION_LAST_V10_URI = "/ss/me/v10/babies/{baby_id}/sessions/last"
SESSION_DAILY_V11_URI = "/ss/me/v11/babies/{baby_id}/sessions/daily"

# Journal and tracking endpoints
JOURNALS_GROUPED_TRACKING_URI = "/cs/me/v11/babies/{baby_id}/journals/grouped-tracking"
JOURNALS_TRACKING_URI = "/cs/me/v11/babies/{baby_id}/journals/tracking"
JOURNALS_CREATE_URI = "/cs/me/v11/journals"
LAST_PUMPING_JOURNAL_URI = "/cs/me/v11/journals/last-pumping-journal"
PUMPING_JOURNALS_TRACKING_URI = "/cs/me/v11/pumping-journals/tracking"
LAST_JOURNALS_URI = "/cs/me/v12/babies/{baby_id}/last-journals"
ARTICLES_URI = "/cs/me/v12/babies/{baby_id}/articles/in-app-content"

# Journal types
JOURNAL_TYPES = {
    'DIAPER': 'diaper',
    'BOTTLE_FEEDING': 'bottlefeeding',
    'BREAST_FEEDING': 'breastfeeding',
    'SOLID_FOOD': 'solidfood',
    'WEIGHT': 'weight',
    'HEIGHT': 'height',
    'HEAD': 'head',
    'PUMPING': 'pumping'
}

# Diaper types
DIAPER_TYPES = ['pee', 'poo']

# Feeding types
FEEDING_TYPES = ['breastmilk', 'formula']

WAIT_TIMEOUT = 60
MANUFACTURER = "Happiestbaby"
