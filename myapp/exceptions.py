from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # DRF-тің стандартты қате өңдеушісін шақырамыз
    response = exception_handler(exc, context)

    if response is not None:
        # Қате форматын өзгертеміз
        custom_data = {
            'status_code': response.status_code,
            'message': 'Қате орын алды',
            'errors': response.data
        }
        response.data = custom_data

    return response