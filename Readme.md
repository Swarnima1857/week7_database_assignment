# Week 7 Assignment


# Schema Design with Embed vs Reference Justification


- **Embed** when the data is bounded in size, always read together with its parent, and doesn't need to be queried independently.
- **Reference** when the data grows unbounded, is shared across multiple parents, or is updated independently of the parent.

### 1. `users`
```json
{
  "name": "Mr.Kieko",
  "email": "kieko1@gmail.com",
  "phone": "1234567890",
  "addresses": [ { "label": "Home", "city": "Hmirpur", "pincode": "000000" } ],
  "created_at": "..."
}
```
- **`addresses` → Embedded.** A user has only a handful of addresses (1-3), they are always displayed together with the user's profile, and are never queried independently across users. Embedding avoids an unnecessary extra lookup.
- **Bookings/reviews are NOT embedded here.** A user can make hundreds of bookings over time — embedding them would make the `users` document grow unbounded and eventually risk hitting MongoDB's 16MB document size limit. Instead, bookings/reviews **reference** the user's `_id`.

### 2. `movies`
```json
{
  "title": "Dhurandhar",
  "genre": ["Action", "Thriller"],
  "cast": ["Ranveer Singh", "Akshay Khanna", ...],
  "duration_min": 180,
  "release_date": "...",
  "language": "Hindi"
}
```
- **`genre` and `cast` → Embedded.** Both are small, fixed-size arrays that are always shown together with the movie details on any movie page. There's no need to query "all movies with actor X" often enough to justify a separate collection, and even if we did, `$unwind`/`$match` on the array handles it fine.

### 3. `theaters`
```json
{
  "name": "PVR Saket",
  "city": "Delhi",
  "screens": [
    { "screen_no": 1, "capacity": 120, "type": "IMAX" },
    { "screen_no": 2, "capacity": 80, "type": "Standard" }
  ]
}
```
- **`screens` → Embedded.** A theater has a small, bounded number of screens (typically 1-15). They never change independently of the theater and are always fetched together when displaying theater info. Embedding avoids a join for a very common read.

### 4. `shows`
```json
{
  "movie_id": "ObjectId(...)",
  "theater_id": "ObjectId(...)",
  "screen_no": 1,
  "start_time": "...",
  "price": 300,
  "seat_map": [ { "seat_no": "A1", "status": "available" } ]
}
```
- **`movie_id`, `theater_id` → Referenced.** The same movie plays in hundreds of shows across many theaters, and each theater hosts hundreds of shows. Embedding the full movie or theater document into every show would massively duplicate data — and if a movie's title were corrected, we'd have to update every single show document. Referencing keeps a single source of truth.
- **`seat_map` → Embedded.** A show has a bounded number of seats (usually under 300), and the whole seat map is read and updated together as **one atomic unit** whenever a seat is booked. MongoDB's single-document atomic update (`updateOne` with a positional `$` operator) is ideal for this "lock this seat" pattern — no separate transaction needed.

### 5. `bookings`
```json
{
  "user_id": "ObjectId(...)",
  "show_id": "ObjectId(...)",
  "seats_booked": ["A1"],
  "total_amount": 300,
  "payment": { "status": "success", "method": "UPI", "txn_id": "TXN001" },
  "booked_at": "..."
}
```
- **`user_id`, `show_id` → Referenced.** A booking belongs to exactly one user and one show, but each user/show can have MANY bookings. The "many" side always references the "one" side — never the other way around, or the parent document would grow unbounded.
- **`seats_booked`, `payment` → Embedded.** Both are small, specific to this one booking, never reused elsewhere, and always needed together whenever this booking/receipt is displayed. No benefit to normalizing them out.

### 6. `reviews`
```json
{
  "movie_id": "ObjectId(...)",
  "user_id": "ObjectId(...)",
  "rating": 4,
  "comment": "Great action, amazing movie",
  "created_at": "..."
}
```
- **`movie_id`, `user_id` → Referenced.** A popular movie can receive thousands of reviews — embedding them inside the `movies` document would risk the 16MB size limit and slow down a simple movie-title lookup that doesn't need any reviews at all.

### 7. `ai_summaries`
```json
{
  "movie_id": "ObjectId(...)",
  "summary_text": "...",
  "sentiment": "mixed",
  "based_on_review_ids": ["ObjectId(...)"],
  "model_used": "claude-sonnet-5",
  "generated_at": "..."
}
```
- **`movie_id` → Referenced.** One summary maps to one movie, but summaries can be regenerated/versioned independently of the movie document (e.g., when new reviews come in or a better model is used).
- **`based_on_review_ids` → Referenced array, not embedded.** The underlying reviews already exist as full documents in the `reviews` collection — embedding them again here would duplicate data. We only keep pointers for traceability/auditing of what the AI summarized.
- **Kept as its own separate collection** (not embedded inside `movies`) because AI summaries need independent versioning/history as new reviews arrive — this is much easier to manage as separate documents than as a repeatedly-mutated sub-field inside `movies`.

---

# Crud Operations
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