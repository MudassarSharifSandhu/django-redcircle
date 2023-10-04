import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
import re


class CategoryData(APIView):
    def post(self, request):
        api_url = "https://api.redcircleapi.com/categories"
        try:
            response = requests.get(api_url)
            data = response.json()

            if "categories" in data:
                categories_data = data["categories"]

                for category_data in categories_data:
                    red_circle_id = category_data["id"]
                    name = category_data["name"]
                    has_children = category_data["has_children"]
                    is_root = category_data["is_root"]
                    path = category_data["path"]
                    link = category_data["link"]
                    parent_id = category_data.get("parent_id")
                    parent_name = category_data.get("parent_name")
                    type = category_data["type"]
                    domain = category_data["domain"]

                    if is_root:
                        parent = None
                        red_circle_parent_id = None
                        parent_name = None
                    else:
                        try:
                            parent = Category.objects.get(
                                red_circle_id=parent_id)
                            red_circle_parent_id = parent_id
                            parent_name = parent.name
                        except Category.DoesNotExist:
                            parent = None
                            red_circle_parent_id = None
                            parent_name = None

                    # Create or update the Category instance
                    data = {
                        'red_circle_id': red_circle_id,
                        'name': name,
                        'has_children': has_children,
                        'is_root': is_root,
                        'path': path,
                        'link': link,
                        'parent': parent,
                        'red_circle_parent_id': red_circle_parent_id,
                        'parent_name': parent_name,
                        'type': type,
                        'domain': domain
                    }
                    category, updated = Category.objects.update_or_create(red_circle_id=red_circle_id, defaults=data)

                categories = Category.objects.all()
                serializer = CategorySerializer(data=categories, many=True)
                if serializer.is_valid():
                        serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"message": "No categories found in the API response."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductData(APIView):
    def post(self, request):
        params = {
            'category_id': 'pmrkg',
            'type': 'category',
            'api_key': 'demo'
        }
        api_url = "https://api.redcircleapi.com/request"
        try:
            response = requests.get(api_url, params=params)
            data = response.json()

            if "category_results" in data:
                categories_results = data["category_results"]
                for product in categories_results:
                    product_details = product['product']
                    tcin = product_details["tcin"]
                    title = product_details["title"]

                    cost = product["offers"]["primary"]["price"]
                    price = cost*1.1
                    unit_cost = cost
                    unit_price = price
                    size = None
                #     Seperate Name Size and Unit from Title
                    matches = re.match(r'(.+?)(\d+)(\D+)', title)
                    if matches:
                        title = matches.group(1).strip()
                        size = int(matches.group(2))
                        unit_cost = cost/size
                        unit_price = price/size
                # unit = matches.group(3).strip() # gives unit e.g kg, lb
                    sub_category_red_circle_id = params["category_id"]
                    image = product_details["images"][0]
                    brand = product_details["brand"]
                    description = product_details["feature_bullets"][0]
                    sub_category = Category.objects.get(
                        red_circle_id=sub_category_red_circle_id)
                    data = {
                        # 'red_circle_product_id': tcin,
                        'title': title,
                        'cost': cost,
                        'price': price,
                        'unit_cost': unit_cost,
                        'unit_price': unit_price,
                        'size': size,
                        'category': sub_category.parent,
                        'sub_category': sub_category,
                        'image': image,
                        'brand': brand,
                        'description': description,
                    }
                    category, updated = Product.objects.update_or_create(red_circle_product_id=tcin, defaults=data)

                products = Product.objects.all()
                serializer = ProductSerializer(data=products, many=True)
                if serializer.is_valid():
                    serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"message": "No categories found in the API response."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
