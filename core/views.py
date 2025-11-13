from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO

def index(request):
    """Bosh sahifa"""
    return render(request, 'index.html')

def generate_qr_api(request):
    """API orqali QR yaratish"""
    data = request.GET.get('data', '')
    fill_color = request.GET.get('fill_color', '#000000')
    back_color = '#ffffff'  # Orqa fon rangi oq

    if not data:
        return JsonResponse({'error': 'Data is required.'}, status=400)

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img: PilImage = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Rasmni bytesga saqlaymiz
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
