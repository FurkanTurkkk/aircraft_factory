from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

class BusinessException(Exception):
    def __init__(self, detail):
        self.detail = detail

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, BusinessException):
            return Response({'error': exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Sunucu hatası!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response