from django.shortcuts import render
from django.conf import settings
import httpx
# Create your views here.

FASTAPI_URL = settings.FASTAPI_BASE_URL

async def get_products():
    async with httpx.AsyncClient() as client:   # 비동기 http 커넥션
        try:
            response = await client.get(f'{FASTAPI_URL}/api/products')
            response.raise_for_status()     # 오류 발생시 예외 발생
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching products: {e}")
            return []

async def product_list(request):
    products = await get_products()
    return render(request,'products/product_list.html', {products:products})

