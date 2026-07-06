# Mongo Db Crud Operation in Postman

# Users
---
## Create User

### Request

 ``` json
 {
  "name": "Sneha",
  "email": "sneha1@gmail.com",
  "phone": "7050603040",
  "addresses": [
      {
          "label": "Home",
      "city": "Kanpur",
      "pincode": "000000"
      }
  ]
}
```
### Postman Output

``` json
{
    "inserted_id": "6a4b4d68aa26cc5c22a2a2d3"
}
```
---

---

## Find user

### Get user (Get/user) Postman Output

``` json
[
    {
        "_id": "6a460df5e93c9d3bc43afec8",
        "name": "Virat Kohli",
        "email": "viratkohli1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "London",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-02T07:06:29.737000"
    },
    {
        "_id": "6a46121b72a8351d14dce22c",
        "name": "Rohit Sharma",
        "email": "rohitsharma45@gmail.com",
        "phone": "5060708090",
        "addresses": [
            {
                "label": "Home",
                "city": "Mumbai",
                "pincode": "567890"
            }
        ],
        "created_at": "new Date()"
    },
    {
        "_id": "6a47b9ee55684eb5f0e983b1",
        "name": "Swarnima",
        "email": "swarnima1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "hometown",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-03T13:32:30.069000"
    },
    {
        "_id": "6a47ba2455684eb5f0e983b2",
        "name": "string",
        "email": "string1@gmail.com",
        "phone": "1020304050",
        "addresses": [
            {
                "label": "Home",
                "city": "hometown",
                "pincode": "123456"
            }
        ],
        "created_at": "2026-07-03T13:33:24.255000"
    },
    {
        "_id": "6a4b4d68aa26cc5c22a2a2d3",
        "name": "Sneha",
        "email": "sneha1@gmail.com",
        "phone": "7050603040",
        "addresses": [
            {
                "label": "Home",
                "city": "Kanpur",
                "pincode": "000000"
            }
        ],
        "created_at": "2026-07-06T06:38:32.039000"
    }
]
```
### Get User (Get/user/user_id) Postman Output

```json
{
    "_id": "6a4b4d68aa26cc5c22a2a2d3",
    "name": "Sneha",
    "email": "sneha1@gmail.com",
    "phone": "7050603040",
    "addresses": [
        {
            "label": "Home",
            "city": "Kanpur",
            "pincode": "000000"
        }
    ],
    "created_at": "2026-07-06T06:38:32.039000"
}
```
---

---

## Update User 
### Request

```json
{
  "name": "Sneha",
  "email": "sneha10@gmail.com",
  "phone": "7050603040",
  "addresses": [
      {
          "label": "Home",
          "city": "Noida",
      "pincode": "000000"
      }
  ]
}
```
I updated Email ID

### Put User(Put/users/user_id), Postman Output

```json
{
    "matched": 1,
    "modified": 1
}
```
---
## Delete User

### Request (Delete/users/user_id), Postman Output

```json
{
    "deleted": 1
}
```
---










