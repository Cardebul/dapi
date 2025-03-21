# dapi

## dependencies

- dependencies
  - docker-compose


### quickstart

```
cd dapi
```

```
docker build -t base -f Dockerfile.base . 
```

```
docker-compose up --build 
```

### simple-doc



GET /api/products - all products

POST    /api/products - all products

{
    "category_id": "uuid",
    "price": float,
    "name": str
}


GET    /api/products/uuid
PUT    /api/products/uuid
{
    "category_id": "uuid",
    "price": float,
    "name": str
}
DELETE    /api/products/uuid


date format %Y-%m-%d example 2025-1-12
GET     /api/sales/total
req query params

start_date
end_date

GET     /api/sales/top-products

req query params

start_date
end_date
limit