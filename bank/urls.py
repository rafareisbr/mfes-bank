from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Bank API')

urlpatterns = [
    path("v1/", include('bank.api.v1.urls')),

    path('docs/', schema_view)
]

'''
    Para configurar o swagger, além do que está na documentação,
    foi necessário adicionar:
    
    TEMPLATES = [
        {
            ...
            OPTIONS: {
                ...
                'libraries': {
                    'staticfiles': 'django.templatetags.static',
                }
            }
        }
    ]
    
    Porque a biblioteca de static antes era chamada staticfiles
    Como isso mudou o código ficou defasado.
    
    E ainda, adicionar no settings.py essa configuração para funcionar a OpenAPI
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
    }
    
'''
