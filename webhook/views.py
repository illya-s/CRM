from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
import subprocess, hmac, hashlib, config


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        signature = request.META.get('HTTP_X_HUB_SIGNATURE_256', '')
        body = request.body

        hash = hmac.new(config.WKEY.encode(), body, hashlib.sha256).hexdigest()
        expected_signature = f"sha256={hash}"

        if not hmac.compare_digest(signature, expected_signature):
            return HttpResponse(f"Invalid request: {expected_signature}", status=404)

        subprocess.call(['/var/www/update_crm.sh'])

        return JsonResponse({"status": "success"}, status=200)
    else:
        return HttpResponseNotFound(f"Invalid request: {request.method}")
