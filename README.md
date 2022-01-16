# Shopify Backend Developer Intern  Challenge - Summer 2022
**TASK:** Build an inventory tracking web application for a logistics company. We are looking for a web application that meets the requirements listed below, along with one additional feature, with the options also listed below.

**Chosen Feature:** Push a button export product data to a CSV


## Running the App
1. Follow the [Docker docs](https://docs.docker.com/get-docker/) to download Docker for your system (Linux users require this [link](https://docs.docker.com/compose/install/) as well for docker compose)
2. Clone the repository from Github
3. Navigate to the Project directory and run:
```
docker-compose up
```
4. At this point the application is usable and will be running at `localhost:5000`, you should see a message like:
```
api-dev     |  * Serving Flask app 'run.py' (lazy loading)
api-dev     |  * Environment: docker
api-dev     |  * Debug mode: off
api-dev     |  * Running on all addresses.
api-dev     |    WARNING: This is a development server. Do not use it in a production deployment.
api-dev     |  * Running on http://172.19.0.3:5000/ (Press CTRL+C to quit)
```

## Running the test suite
A [Postman](https://www.postman.com/chalky-devs/workspace/shopify-backend-intern-summer-2022/overview) test suite was created for ease of use. All endpoints are testing against localhost.

To run the Postman test suite:
1. Download the Postman Desktop app [link](https://learning.postman.com/docs/getting-started/installation-and-updates/)
2. Create an account in the Postman app
3. Import the file `postman_collection.json` in the repository
4. Run the collection

## API Documentation
All endpoints here have a base URL of `http://localhost:5000` when running the docker services.
### Endpoints
[Create Item](): `POST /items`

[Update Item](): `PATCH /items/<item_id>`

[Get Items](): `GET /items`

[Delete Item](): `DELETE /items/<item_id>`

[Export Item Table to CSV](): `GET /items/export`

---

## Endpoint Documentation
### Create Item
---

**URL**: `/items`

**Method**: `POST`
#### Success Response
**Code**: `201 Created`

**Example Payload**

In the body of the request, the itemname and price fields are required.
```
# payload body
{
    "itemname":"shoe",
    "price": 120.0
}
```
The price and quantity fields can also be specified. But additional fields will cause an error.
```
{
    "itemname":"water bottle",
    "price": 40.0,
    "quantity": 1
}
```
```
{
    "itemname":"chocolate",
    "price": 1.40,
    "quantity": 110,
    "description": "A sweet and decadent treat"
}
```
#### Error Response
**Code**: `400 Bad Request`

**Example Response**


```
{
    "error": "Malformed payload. Additional properties are not allowed ('hello' was unexpected)"
}
```
```
{
    "error": "Malformed payload. 'f' is not of type 'number'"
}
```

### Update Item
---

**URL**: `/items/<item_id>`

**Method**: `PATCH`

#### Success Response
**Code**: `200 OK`

**Example Payload**

The quantity, price, description or itemname are changeable. Additional fields will cause an error.
```
{
    "quantity":3
}
```
```
{
    "itemname":"banana",
    "price": 0.99,
    "description": "Monkeys go bananas for these!"
}
```

#### Error Response
**Code**: `404 Not Found`

**Example Response**


```
{
    "error": "Resource not found. Item ID '4' does not exist"
}
```


### Get Items
---

**URL**: `/items`

**Method**: `GET`

#### Success Response
**Code**: `200 OK`

**Example Response**

All items from the Item table are returned as a response.
```
[
  {
    "description": "", 
    "id": 1, 
    "itemname": "shoe", 
    "price": 120.0, 
    "quantity": 3
  }, 
  {
    "description": "", 
    "id": 2, 
    "itemname": "laptop", 
    "price": 1500.0, 
    "quantity": 0
  }, 
  {
    "description": "", 
    "id": 3, 
    "itemname": "water bottle", 
    "price": 40.0, 
    "quantity": 1
  }
]
```

### Delete Item
---

**URL**: `/items/<item_id>`

**Method**: `DELETE`

#### Success Response
**Code**: `204 No Content`

#### Error Response

**Code**: `404 Not Found`

**Example Response**


```
{
    "error": "Resource not found. Item ID '0' does not exist"
}
```

### Export Item Table to CSV
---

**URL**: `/items/export`

**Method**: `GET`
#### Success Response
**Code**: `200 OK`

**Example Response**


```
id,itemname,price,quantity,description
1,laptop,1500.0,0,
2,shoe,120.0,0,"Better than barefoot"
```