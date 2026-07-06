# Week 7 Assignment
# CRUD Operation

---
## Insert
### Insert User Query

```json
db.users.insertOne({
  name: "Mr.Kieko",
  email: "kieko1@gmail.com",
  phone: "1234567890",
  addresses: [{label: "Home", city: "Hmirpur", pincode: "000000"}],
  created_at: new Date()
})
```
### Output

```json
{
  "_id": {
    "$oid": "6a4b82ed2d810ac969846c31"
  },
  "name": "Mr.Kieko",
  "email": "kieko1@gmail.com",
  "phone": "1234567890",
  "addresses": [
    {
      "label": "Home",
      "city": "Hmirpur",
      "pincode": "000000"
    }
  ],
  "created_at": {
    "$date": "2026-07-06T10:26:53.268Z"
  }
}
```
### Inset Movie Query

``` json
db.movies.insertOne({
  title: "Dhurandhar",
  genre: ["Action", "Thriller"],
  cast: ["Ranveer Singh", "Akshay Khanna", "Sanjay Dutt", "Arjun Rampal", "Sara Ali Khan"],
  duration_min: 180,
  release_date: new Date("2026-01-15"),
  language: "Hindi"
})
```

### Output

```json
{
  "_id": {
    "$oid": "6a4b89503ac2189cde989edd"
  },
  "title": "Dhurandhar",
  "genre": [
    "Action",
    "Thriller"
  ],
  "cast": [
    "Ranveer Singh",
    "Akshay Khanna",
    "Sanjay Dutt",
    "Arjun Rampal",
    "Sara Ali Khan"
  ],
  "duration_min": 180,
  "release_date": {
    "$date": "2026-01-15T00:00:00.000Z"
  },
  "language": "Hindi"
}
```
### insert movie Query

```json
   db.theaters.insertOne({
  name: "PVR Saket",
  city: "Delhi",
  screens: [
    { screen_no: 1, capacity: 120, type: "IMAX" },
    { screen_no: 2, capacity: 80, type: "Standard" }
  ]
})
```
### Output
```json
{
  "_id": {
    "$oid": "6a46260672a8351d14dce234"
  },
  "name": "PVR Saket",
  "city": "Delhi",
  "screens": [
    {
      "screen_no": "1",
      "capacity": "120",
      "type": "IMAX"
    },
    {
      "screen_no": "2",
      "capacity": "80",
      "type": "Standard"
    }
  ]
}
```
### Insert Show Query

```json
db.shows.insertOne({
  movie_id: ObjectId("6a4b89503ac2189cde989edd"),
  theater_id: ObjectId("6a46260672a8351d14dce234"),
  screen_no: 1,
  start_time: new Date("2026-07-10T18:00:00Z"),
  price: 300,
  seat_map: [
    { seat_no: "A1", status: "available" },
    { seat_no: "A2", status: "available" }
  ]
})
```
### output

```json
{
  "_id": {
    "$oid": "6a4b934e3ac2189cde989ede"
  },
  "movie_id": {
    "$oid": "6a4b89503ac2189cde989edd"
  },
  "theater_id": {
    "$oid": "6a46260672a8351d14dce234"
  },
  "screen_no": 1,
  "start_time": {
    "$date": "2026-07-10T18:00:00.000Z"
  },
  "price": 300,
  "seat_map": [
    {
      "seat_no": "A1",
      "status": "available"
    },
    {
      "seat_no": "A2",
      "status": "available"
    }
  ]
}
```
### Insert Booking Query

```json
db.bookings.insertOne({
  user_id: ObjectId("6a4b82ed2d810ac969846c31"),
  show_id: ObjectId("6a4b934e3ac2189cde989ede"),
  seats_booked: ["A1"],
  total_amount: 300,
  payment: { status: "success", method: "UPI", txn_id: "TXN001" },
  booked_at: new Date()
})
```
### Output

```json
{
  "_id": {
    "$oid": "6a4b95403ac2189cde989edf"
  },
  "user_id": {
    "$oid": "6a4b82ed2d810ac969846c31"
  },
  "show_id": {
    "$oid": "6a4b934e3ac2189cde989ede"
  },
  "seats_booked": [
    "A1"
  ],
  "total_amount": 300,
  "payment": {
    "status": "success",
    "method": "UPI",
    "txn_id": "TXN001"
  },
  "booked_at": {
    "$date": "2026-07-06T11:45:04.037Z"
  }
}
```
### Insert Review Query
```json
db.reviews.insertOne({
  movie_id: ObjectId("6a4b89503ac2189cde989edd"),
  user_id: ObjectId("6a4b82ed2d810ac969846c31"),
  rating: 4,
  comment: "Great action, amazing movie",
  created_at: new Date()
})
```
### Output
```json
{
  "_id": {
    "$oid": "6a4b963e3ac2189cde989ee0"
  },
  "movie_id": {
    "$oid": "6a4b89503ac2189cde989edd"
  },
  "user_id": {
    "$oid": "6a4b82ed2d810ac969846c31"
  },
  "rating": 4,
  "comment": "Great action, amazing movie",
  "created_at": {
    "$date": "2026-07-06T11:49:18.913Z"
  }
}
```
### Insert AI Summeries Query
```json
db.ai_summaries.insertOne({
  movie_id: ObjectId("6a4b89503ac2189cde989edd"),
  summary_text: "Viewers loved the action sequences, an plot twist amzing",
  sentiment: "mixed",
  based_on_review_ids: [ObjectId("6a4b97002d810ac969846c60")],
  model_used: "claude-sonnet-5",
  generated_at: new Date()
})
```
### Output
```json
{
  acknowledged: true,
  insertedId: ObjectId('6a4b96ed3ac2189cde989ee1')
}
```


---
---

## Read

### Read User Query
```javascript
db.users.find({ name: "Mr.Kieko" })
```
### Output
```json
[
  {
    "_id": { "$oid": "6a4b82ed2d810ac969846c31" },
    "name": "Mr.Kieko",
    "email": "kieko1@gmail.com",
    "phone": "1234567890",
    "addresses": [
      { "label": "Home", "city": "Hmirpur", "pincode": "000000" }
    ],
    "created_at": { "$date": "2026-07-06T10:26:53.268Z" }
  }
]
```

### Read Movie Query
```javascript
db.movies.find({ title: "Dhurandhar" })
```
### Output
```json
[
  {
    "_id": { "$oid": "6a4b89503ac2189cde989edd" },
    "title": "Dhurandhar",
    "genre": ["Action", "Thriller"],
    "cast": ["Ranveer Singh", "Akshay Khanna", "Sanjay Dutt", "Arjun Rampal", "Sara Ali Khan"],
    "duration_min": 180,
    "release_date": { "$date": "2026-01-15T00:00:00.000Z" },
    "language": "Hindi"
  }
]
```

### Read Theater Query
```javascript
db.theaters.find({ city: "Delhi" })
```
### Output
```json
[
  {
    "_id": { "$oid": "6a46260672a8351d14dce234" },
    "name": "PVR Saket",
    "city": "Delhi",
    "screens": [
      { "screen_no": 1, "capacity": 120, "type": "IMAX" },
      { "screen_no": 2, "capacity": 80, "type": "Standard" }
    ]
  }
]
```

### Read Show Query (available seats only)
```javascript
db.shows.findOne(
  { _id: ObjectId("6a4b934e3ac2189cde989ede") },
  { seat_map: { $elemMatch: { status: "available" } } }
)
```
### Output
```json
{
  "_id": { "$oid": "6a4b934e3ac2189cde989ede" },
  "seat_map": [
    { "seat_no": "A1", "status": "available" }
  ]
}
```

### Read Booking Query (JOIN-like using $lookup)
```javascript
db.bookings.aggregate([
  { $lookup: { from: "users", localField: "user_id", foreignField: "_id", as: "user_info" } }
])
```
### Output
```json
[
  {
    "_id": { "$oid": "6a4b95403ac2189cde989edf" },
    "user_id": { "$oid": "6a4b82ed2d810ac969846c31" },
    "show_id": { "$oid": "6a4b934e3ac2189cde989ede" },
    "seats_booked": ["A1"],
    "total_amount": 300,
    "payment": { "status": "success", "method": "UPI", "txn_id": "TXN001" },
    "booked_at": { "$date": "2026-07-06T11:45:04.037Z" },
    "user_info": [
      {
        "_id": { "$oid": "6a4b82ed2d810ac969846c31" },
        "name": "Mr.Kieko",
        "email": "kieko1@gmail.com",
        "phone": "1234567890"
      }
    ]
  }
]
```

### Read Review Query (JOIN-like using $lookup)
```javascript
db.reviews.aggregate([
  { $lookup: { from: "users", localField: "user_id", foreignField: "_id", as: "user_info" } }
])
```
### Output
```json
[
  {
    "_id": { "$oid": "6a4b963e3ac2189cde989ee0" },
    "movie_id": { "$oid": "6a4b89503ac2189cde989edd" },
    "user_id": { "$oid": "6a4b82ed2d810ac969846c31" },
    "rating": 4,
    "comment": "Great action, amazing movie",
    "created_at": { "$date": "2026-07-06T11:49:18.913Z" },
    "user_info": [
      {
        "_id": { "$oid": "6a4b82ed2d810ac969846c31" },
        "name": "Mr.Kieko",
        "email": "kieko1@gmail.com"
      }
    ]
  }
]
```

### Read AI Summary Query (JOIN-like using $lookup)
```javascript
db.ai_summaries.aggregate([
  { $lookup: { from: "movies", localField: "movie_id", foreignField: "_id", as: "movie_info" } }
])
```
### Output
```json
[
  {
    "_id": { "$oid": "6a4b96ed3ac2189cde989ee1" },
    "movie_id": { "$oid": "6a4b89503ac2189cde989edd" },
    "summary_text": "Viewers loved the action sequences, an plot twist amzing",
    "sentiment": "mixed",
    "based_on_review_ids": [{ "$oid": "6a4b97002d810ac969846c60" }],
    "model_used": "claude-sonnet-5",
    "generated_at": { "$date": "2026-07-06T11:52:00.000Z" },
    "movie_info": [
      {
        "_id": { "$oid": "6a4b89503ac2189cde989edd" },
        "title": "Dhurandhar",
        "language": "Hindi"
      }
    ]
  }
]
```

---

## Update

### Update User Query
```javascript
db.users.updateOne(
  { _id: ObjectId("6a4b82ed2d810ac969846c31") },
  { $set: { phone: "9999999999" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update Movie Query
```javascript
db.movies.updateOne(
  { _id: ObjectId("6a4b89503ac2189cde989edd") },
  { $set: { duration_min: 175 } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update Theater Query
```javascript
db.theaters.updateOne(
  { _id: ObjectId("6a46260672a8351d14dce234"), "screens.screen_no": 1 },
  { $set: { "screens.$.type": "4DX" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update Show Query (mark seat A1 as booked)
```javascript
db.shows.updateOne(
  { _id: ObjectId("6a4b934e3ac2189cde989ede"), "seat_map.seat_no": "A1" },
  { $set: { "seat_map.$.status": "booked" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update Booking Query
```javascript
db.bookings.updateOne(
  { _id: ObjectId("6a4b95403ac2189cde989edf") },
  { $set: { "payment.status": "refunded" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update Review Query
```javascript
db.reviews.updateOne(
  { _id: ObjectId("6a4b963e3ac2189cde989ee0") },
  { $set: { rating: 5, comment: "Loved it even more on rewatch!" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

### Update AI Summary Query
```javascript
db.ai_summaries.updateOne(
  { _id: ObjectId("6a4b96ed3ac2189cde989ee1") },
  { $set: { sentiment: "positive" } }
)
```
### Output
```json
{ "acknowledged": true, "matchedCount": 1, "modifiedCount": 1 }
```

---

## Delete

### Delete Review Query
```javascript
db.reviews.deleteOne({ _id: ObjectId("6a4b963e3ac2189cde989ee0") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

### Delete Booking Query
```javascript
db.bookings.deleteOne({ _id: ObjectId("6a4b95403ac2189cde989edf") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```


### Delete Show Query
```javascript
db.shows.deleteOne({ _id: ObjectId("6a4b934e3ac2189cde989ede") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

### Delete AI Summary Query
```javascript
db.ai_summaries.deleteOne({ _id: ObjectId("6a4b96ed3ac2189cde989ee1") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

### Delete Theater Query
```javascript
db.theaters.deleteOne({ _id: ObjectId("6a46260672a8351d14dce234") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

### Delete Movie Query
```javascript
db.movies.deleteOne({ _id: ObjectId("6a4b89503ac2189cde989edd") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

### Delete User Query
```javascript
db.users.deleteOne({ _id: ObjectId("6a4b82ed2d810ac969846c31") })
```
### Output
```json
{ "acknowledged": true, "deletedCount": 1 }
```

---