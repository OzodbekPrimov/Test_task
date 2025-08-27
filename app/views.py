
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Client, Product, Order
from .serializers import ClientSerializer, ProductSerializer, OrderSerializer


class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        operation_description="Barcha mijozlarni ko'rish (dropdown uchun)",
        responses={200: ClientSerializer(many=True)},
        tags=['Mijozlar']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Yangi mijoz yaratish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Mijoz ismi',
                    example='Ahmad Valiyev'
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Telefon raqami',
                    example='+998901234567'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email (ixtiyoriy)',
                    example='ahmad@example.com'
                ),
            },
            required=['name', 'phone'],
            example={
                "name": "Ahmad Valiyev",
                "phone": "+998901234567",
                "email": "ahmad@example.com"
            }
        ),
        responses={
            201: openapi.Response(
                description="Mijoz muvaffaqiyatli yaratildi",
                examples={
                    "application/json": {
                        "message": "Mijoz muvaffaqiyatli yaratildi!",
                        "data": {
                            "id": 1,
                            "name": "Ahmad Valiyev",
                            "phone": "+998901234567",
                            "email": "ahmad@example.com"
                        }
                    }
                }
            ),
            400: "Noto'g'ri ma'lumotlar"
        },
        tags=['Mijozlar']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Mijoz muvaffaqiyatli yaratildi!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="Barcha mahsulotlarni ko'rish (dropdown uchun)",
        responses={200: ProductSerializer(many=True)},
        tags=['Mahsulotlar']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Yangi mahsulot yaratish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Mahsulot nomi',
                    example='Olma'
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Tavsif (ixtiyoriy)',
                    example='Toza tabiiy olma'
                ),
                'base_price': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Asosiy narxi',
                    example=15000.00
                ),
            },
            required=['name', 'base_price'],
            example={
                "name": "Olma",
                "description": "Toza tabiiy olma",
                "base_price": 15000.00
            }
        ),
        responses={
            201: openapi.Response(
                description="Mahsulot muvaffaqiyatli yaratildi",
                examples={
                    "application/json": {
                        "message": "Mahsulot muvaffaqiyatli yaratildi!",
                        "data": {
                            "id": 1,
                            "name": "Olma",
                            "description": "Toza tabiiy olma",
                            "base_price": "15000.00"
                        }
                    }
                }
            ),
            400: "Noto'g'ri ma'lumotlar"
        },
        tags=['Mahsulotlar']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Mahsulot muvaffaqiyatli yaratildi!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Yangi buyurtma yaratish. Client va mahsulotlarni tanlang, har biriga son va narx kiriting.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'client': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Mijoz ID raqami',
                    example=1
                ),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'product': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Mahsulot ID raqami',
                                example=1
                            ),
                            'quantity': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Mahsulot soni',
                                example=5
                            ),
                            'price': openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                description='Mahsulot narxi',
                                example=25000.50
                            ),
                        },
                        required=['product', 'quantity', 'price']
                    ),
                    description='Buyurtma mahsulotlari ro\'yxati'
                ),
            },
            required=['client', 'items'],
            example={
                "client": 1,
                "items": [
                    {
                        "product": 1,
                        "quantity": 5,
                        "price": 25000.00
                    }
                ]
            }
        ),
        responses={
            201: openapi.Response(
                description="Buyurtma muvaffaqiyatli yaratildi",
                examples={
                    "application/json": {
                        "message": "Buyurtma muvaffaqiyatli yaratildi!",
                        "data": {
                            "id": 1,
                            "client": 1,
                            "client_name": "Ahmad Valiyev",
                            "items": [
                                {
                                    "id": 1,
                                    "product": 1,
                                    "product_name": "Olma",
                                    "quantity": 5,
                                    "price": "25000.00"
                                }
                            ],
                            "total_amount": 125000.00,
                            "created_at": "2025-01-01T10:30:00Z"
                        }
                    }
                }
            ),
            400: "Noto'g'ri ma'lumotlar"
        },
        tags=['Buyurtmalar']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Buyurtma muvaffaqiyatli yaratildi!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Mavjud buyurtmani yangilash. PUT - to'liq yangilash, PATCH - qisman yangilash",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'client': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Mijoz ID raqami (ixtiyoriy PATCH uchun)',
                    example=2
                ),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'product': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=8),
                            'price': openapi.Schema(type=openapi.TYPE_NUMBER, example=28000.00),
                        }
                    ),
                    description='Yangi mahsulotlar ro\'yxati'
                ),
            },
            example={
                "client": 2,
                "items": [
                    {
                        "product": 3,
                        "quantity": 10,
                        "price": 30000.00
                    }
                ]
            }
        ),
        responses={
            200: openapi.Response(
                description="Buyurtma muvaffaqiyatli yangilandi",
                examples={
                    "application/json": {
                        "message": "Buyurtma muvaffaqiyatli yangilandi!",
                        "data": {
                            "id": 1,
                            "client": 2,
                            "client_name": "Olim Karimov",
                            "total_amount": 300000.00
                        }
                    }
                }
            ),
            404: "Buyurtma topilmadi",
            400: "Noto'g'ri ma'lumotlar"
        },
        tags=['Buyurtmalar']
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Buyurtma muvaffaqiyatli yangilandi!',
            'data': serializer.data
        })


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Bitta buyurtmaning barcha ma'lumotlarini ko'rish",
        responses={
            200: OrderSerializer(),
            404: "Buyurtma topilmadi"
        },
        tags=['Buyurtmalar']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)