from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # DRF-тің стандартты қате өңдеушісін шақыру
    response = exception_handler(exc, context)

    # Егер басқа да арнайы логика керек болса, осы жерге қосуға болады
    if response is not None:
        response.data['status_code'] = response.status_code

    return response