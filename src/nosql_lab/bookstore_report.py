#!/usr/bin/env python3

import os
import logging
import pymongo
from pymongo.errors import PyMongoError

'''reads the credentials from the shell envirometn'''
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")



def main ():
    """ Connects to MongoDB client and reports the amount of authors and selected authors name, book, and publication date"""
    logging.basicConfig(
        level=logging.INFO, 
        format="%(levelname)s: %(message)s"
    )

    client = None

    try:
        #checking if all the environment variables are met before proceeding
        if not all((
            MONGODB_ATLAS_URL, 
            MONGODB_ATLAS_USER, 
            MONGODB_ATLAS_PWD
        )):
            raise ValueError("All three environment variables need to be set.")
    
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000
        )
        #verifies the connection as been connected
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas.")

        #selects bookstore database and authors and books collections
        database = client['bookstore']
        authors = database['authors']
        books = database['books']

        #list of author values in the collection 
        author_ids = ["author_001", "author_002", "author_003", "author_004", "author_005"]

        #counts the amount of authors in the iteration and then prints it
        author_count = authors.count_documents({
            "_id": {"$in": author_ids}
        })
        print(f"Authors: {author_count}")

        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})
            # if author is not found, prints a error statement
            if author is None:
                logging.error("Author was not found.", author_id)
                continue

            print(f"\n{author['name']}")

            #retrieves the author the matches the book
            matched_books = books.find({"author_ids": author_id})

            for book in matched_books:
                print(f"  {book['title']} ({book['published_year']})")

    except (PyMongoError, ValueError) as error:
        logging.error("Bookstore report failed: %s", error)

    finally:
        # Close the client whether the report succeeds or fails
        if client is not None:
            try:
                client.close()
                logging.info("MongoDB closed.")
            except PyMongoError as error:
                logging.error("Could not close client: %s", error)





if __name__ == "__main__":
    main()