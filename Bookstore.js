// Step 2: 
// use bookstore 
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
db.authors.find()
db.books.find()

// Step 6: insert two new books
db.books.insertMany([
  {
    title: "Great Expectations",
    published_year: 1861,
    author_ids: ["author_004"]
  },
  {
    title: "Harry Potter and the Philosopher's Stone",
    published_year: 1997,
    author_ids: ["author_005"]
  }
]);

// Step 7: add missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "Charles Dickens",
    nationality: "British",
      bio: {
      short: "British author best known for the Harry Potter series",
      long: "J.K. Rowling created the Harry Potter series, which follows a young wizards adventures and explores friendship, courage, and good versus evil."
    }
  },
  {
    _id: "author_005",
    name: "J.K. Rowling",
    nationality: "British",
    bio: {
      short: "British author of novels, comics, and screen work.",
      long: "Neil Gaiman is a British author whose work crosses novels, comics, and film. He wrote American Gods on his own and Good Omens with Terry Pratchett."
    }
  },
]);
// Step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_002", "author_005"] } })
