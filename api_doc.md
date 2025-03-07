# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Get Paginated Data
**Endpoint:**
```
GET /api/data?page={page}&per_page={per_page}&filter_key=filter_value
```
**Description:**
Retrieves paginated data with optional filters.

**Query Parameters:**
- `page` (int, optional): Page number (default: 1).
- `per_page` (int, optional): Number of items per page (default: 10).
- Additional filter parameters can be added (e.g., `codeOffice=123`).

**Response:**
```json
{
  "total": 100,
  "page": 1,
  "per_page": 10,
  "data": [
    {"codeOffice": "123", "taxCode": "456", "amount": 1000}
  ]
}
```

### 2. Get Count of Filtered Data
**Endpoint:**
```
GET /api/count?filter_key=filter_value
```
**Description:**
Returns the count of records matching the filters.

**Query Parameters:**
- Any filter parameter (e.g., `codeOffice=123`).

**Response:**
```json
{
  "count": 25
}
```

### 3. Get Recettes by Date Range
**Endpoint:**
```
GET /api/recettes?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
**Description:**
Retrieves total revenue (`TotalAmountIn`) grouped by date.

**Query Parameters:**
- `start_date` (optional, format: YYYY-MM-DD): Start date for filtering.
- `end_date` (optional, format: YYYY-MM-DD): End date for filtering.

**Response:**
```json
{
  "recettes": {
    "2024-01-01": 5000,
    "2024-01-02": 3000
  }
}
```

## Example Requests
### Fetch Paginated Data
```
curl -X GET "http://localhost:5000/api/data?page=2&per_page=5"
```

### Get Count with Filters
```
curl -X GET "http://localhost:5000/api/count?codeOffice=123"
```

### Get Recettes for a Date Range
```
curl -X GET "http://localhost:5000/api/recettes?start_date=2024-01-01&end_date=2024-02-01"
```

