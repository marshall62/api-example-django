import hashlib, hmac
from django.http import JsonResponse
import drchrono.settings as settings

def webhook_verify(request):
    bytes = settings.WEBHOOK_SECRET_TOKEN.encode()
    msg = request.GET['msg']
    secret_token = hmac.new(bytes, msg.encode(), hashlib.sha256).hexdigest()
    # note I changed this from json_response
    return JsonResponse({
        'secret_token': secret_token
    })


# TODO needs to accept a GET request as verification from the API.
# needs to accept POST
# must be https
def handle_update (request):
    if request.method == 'GET':
        return webhook_verify(request)
    elif request.method == 'POST':
        pass
    else:
        pass
