# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

LMS_BASE = "openedx.ryumatsu.com:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

CMS_BASE = "studio.openedx.ryumatsu.com:8001"
CMS_ROOT_URL = "http://" + CMS_BASE

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.openedx.ryumatsu.com:8000"

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "Test for Prep courses - https://openedx.ryumatsu.com"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

try:
    from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
    warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
    warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
except ImportError:
    # REMOVE-AFTER-V18:
    # In Quince, edx-platform uses Django 5. But on master, edx-platform still uses Django 3.
    # So, Tutor v17 needs to silence these warnings, whereas Tutor v17-nightly fails to import them.
    # Once edx-platform master is upgraded to Django 5, the try-except wrapper can be removed.
    pass

warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://openedx.ryumatsu.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "lEs3Z4JofFDz0TFoQnPlqWPg"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "GVak80ne4xpaJi0t7R6xiI8RPAGkRoet3yAKEiP5gbbU2ytnJy4UarYDce1-x0tCEGRkB6o_hYO6b-ygGqTtd26mFKMFKHPoKhZuNtA2s2t1a6-ZfTfdo5Czo5dgznamSgBOU2nWo_tuiBfc8XJBMQbnO0T3sZ3ogYW2HdfzZN10GJ2fhfiv79AeFgy6oWIdxuecFUhrcbqfl_yXshzIJNBH3BFyz2PtszXncLSZix7iTUVkUtuNU5XNq8Rb-1mdt-7j8kRSpwAjLABK6OX7pKwRIyWRstKbjLXPOt8BunasX-z6dZHwJmMW3p7HxgVCamAcODi8-fGEJeaNLBhDHQ",
        "n": "1MewHQCV1D0Y2UKljVJYIEwSme_kc6M0Xi7yTjPAHOCKGQD71NQyGqZKdZKHdKKc2VzmJIdsxongm5VT8GBPp9_9qJXP8DPN2yZVetY0cyQqLXQl0Kf0N1wMx9fRvlsP3Wb0ivS09BLCBVlJ_YCpGuPaagufKjmxO-SnJVeXBAagtTCb87CCGDEIxqcUVXElpPZPMG-OfxK9goCNhFE-tv4e4rJphi8PijMlirPMWf4vWw4Ja-qIr0Hc94uXTFotzbIgldwDAYGpW1kosvu7vKYGe9mWNjrN-upzZTb5lW9zJuRIUnuOcJMZAvy7-uFs_3WgHFSCzkLIZ7MyK64S6Q",
        "p": "1871DcmuWje2cii_zKbumDnMm9yBx-NTFGlrrMhT4dxbnH5cpfFVCQK3EFhZgKfYi7CKw0fJtCIyVGagYIGZM8rDpD_o-O4l7ZZLPz4sH6S_TyHSXjWaJRAhCJtbp7X1Lv5YEy0muT1ZHLgkvPcvnqaMh_tbvHsvtEq_iHMxaNs",
        "q": "_GhYvquMdtOV9a7sRsU9RMssZtCHORKUBd1dRaIHBSHS3uIIwlcavdAca8C8NpotKLfOyYcplRtdGju4Jiu4OiICGC9opi6aIPMHJYs37NTDs1fAqoY11-bF65Hgl534HLBC08J8LARggkQ1ELDCI2IAWnoY07UVIZTHCd1lrIs",
        "dq": "dmMu9Meby4Q0exa_pfYPZbvyKIs4UZGgMhwBCo8Twdl6gaX9O8IFPfBl1DiDTw0Dj2yfJjEqVNCP26UVG3o4H7QhzVw3NnL3QesbeAWThpbI786CBLmMeaa5QGOctyCV5kbaIV7ARRkMdy0swpZViKkHx2grSulNbwHMVZktfj8",
        "dp": "0oos1vu4pnmN_Ae3PvBo-4gADtrsnlcv2U0T6Cg0dbgmhCFfP-GWxUip0j9vai3V_EoKxoNFzABEu8S3mA83qKibf6V-I0UrKYQj-xorr99paMklVBXVQW1f3Oa8X30MK4Gl6Wd2TOgGBRe9d8Fr6sqvdYaLM_G2U51NCNDhFls",
        "qi": "scQ2e72yFHcLfIuP5o0u6q1E6SQYYz30f0szxMZcTEfg6TC2vniXNzlgwm33k60aD82G2YoEsgXRmKPxDAybQ-qF6U6u1tUoxUdjV9Bg7I5LVXYJWv9yvXL5mWPOECqmDKKOECL4VDQGLxkqSvC_6eIt5ZQIZvN2dotwt0qRYfk",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "1MewHQCV1D0Y2UKljVJYIEwSme_kc6M0Xi7yTjPAHOCKGQD71NQyGqZKdZKHdKKc2VzmJIdsxongm5VT8GBPp9_9qJXP8DPN2yZVetY0cyQqLXQl0Kf0N1wMx9fRvlsP3Wb0ivS09BLCBVlJ_YCpGuPaagufKjmxO-SnJVeXBAagtTCb87CCGDEIxqcUVXElpPZPMG-OfxK9goCNhFE-tv4e4rJphi8PijMlirPMWf4vWw4Ja-qIr0Hc94uXTFotzbIgldwDAYGpW1kosvu7vKYGe9mWNjrN-upzZTb5lW9zJuRIUnuOcJMZAvy7-uFs_3WgHFSCzkLIZ7MyK64S6Q",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://openedx.ryumatsu.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "lEs3Z4JofFDz0TFoQnPlqWPg"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "Test for Prep courses - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "NXAhb4eRZe45uLDSuPgbBcip"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common CMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"


# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.openedx.ryumatsu.com:2001/course-authoring"
CORS_ORIGIN_WHITELIST.append("http://apps.openedx.ryumatsu.com:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.openedx.ryumatsu.com:2001")
CSRF_TRUSTED_ORIGINS.append("http://apps.openedx.ryumatsu.com:2001")
