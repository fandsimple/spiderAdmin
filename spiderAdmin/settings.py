import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6b4r&8wc!0wl4utvjer9swg@4apis@p#cx)#x_=4_w6h7f73+i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # 'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'spiderTask',
    'daterange_filter',

]

# add middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spiderAdmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': os.path.join(BASE_DIR, 'template'),
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spiderAdmin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'spider',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': 3306,
        'HOST': '127.0.0.1',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = 'static/'
# # STATIC_ROOT = '/Users/fanding/gitProjects/stongerSpider/spiderAdmin/static'
# STATICFILES_DIRS = [
#     # '/Users/fanding/gitProjects/stongerSpider/spiderAdmin/static'
# ]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

APPEND_SLASH = False

# 任务调度策略配置

GET_TASK_RULE = 0  # 0：按照优先级排序 1：按照任务类型排序 更新任务 > 全量任务 按照任务添加顺序执行 2：先按照任务类型排序，然后再按照优先级排序 更新任务 > 全量任务，序号大的先执行

# simple-ui 配置
# SIMPLEUI_DEFAULT_ICON = False

#
# import time
#
# SIMPLEUI_CONFIG = {
#     'system_keep': True,
#     'menu_display': ['Simpleui', '测试', '权限认证', '动态菜单测试'],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
#     'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
#     'menus': [{
#         'name': 'Simpleui',
#         'icon': 'fas fa-code',
#         'url': 'https://gitee.com/tompeppa/simpleui'
#     }, {
#         'app': 'auth',
#         'name': '权限认证',
#         'icon': 'fas fa-user-shield',
#         'models': [{
#             'name': '用户',
#             'icon': 'fa fa-user',
#             'url': 'auth/user/'
#         }]
#     }, {
#         'name': '测试',
#         'icon': 'fa fa-file',
#         'models': [{
#             'name': 'Baidu',
#             'url': 'http://baidu.com',
#             'icon': 'far fa-surprise'
#         }, {
#             'name': '内网穿透',
#             'url': 'https://www.wezoz.com',
#             'icon': 'fab fa-github'
#         }]
#     }, {
#         'name': '动态菜单测试',
#         'icon': 'fa fa-desktop',
#         'models': [{
#             'name': time.time(),
#             'url': 'http://baidu.com',
#             'icon': 'far fa-surprise'
#         }]
#     }]
# }


SIMPLEUI_STATIC_OFFLINE = True


STATIC_URL = '/static/'

