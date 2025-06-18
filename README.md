# Address Book API

A FastAPI application for managing addresses with coordinates. This application allows users to create, read, update, and delete addresses, as well as find addresses within a specified distance from given coordinates.


## Setup Instructions

####  Using Docker Compose

```bash
# Build and run with docker-compose
docker-compose up

# Stop the application
docker-compose down
```

The application will be available at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## API Endpoints

### 1. Create Address
- **POST** `/address/add/`
- Request body: JSON with address fields (street, city, state, postal_code, country, latitude, longitude)
- Response: The created address object

### 2. Get All Addresses
- **GET** `/address/list/`
- Query parameters:
  - `skip` (optional, default: 0): Number of records to skip
  - `limit` (optional, default: 100): Maximum number of records to return
- Response: List of address objects

### 3. Get Address by ID
- **GET** `/address/{address_id}`
- Path parameter: `address_id` (integer)
- Response: The address object with the specified ID

### 4. Update Address
- **PUT** `/address/update/{address_id}`
- Path parameter: `address_id` (integer)
- Request body: JSON with any address fields to update (all optional)
- Response: The updated address object

### 5. Delete Address
- **DELETE** `/address/delete/{address_id}`
- Path parameter: `address_id` (integer)
- Response: Success message if deleted

### 6. Find Nearby Addresses
- **GET** `/address/list/nearby/`
- Query parameters:
  - `latitude` (required): Target latitude
  - `longitude` (required): Target longitude
  - `distance_km` (optional, default: 10.0): Search radius in kilometers
- Response: List of address objects within the specified distance


## Database

The application uses SQLite as the database. The database file (`address_book.db`) will be created automatically when you first run the application.

When using Docker, the database file is persisted using a volume mount, so your data will be preserved between container restarts.


## Distance Calculation

The nearby search functionality uses the geodesic distance calculation from the `geopy` library, which provides accurate distance calculations on the Earth's surface.
