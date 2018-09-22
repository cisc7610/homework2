#!/usr/bin/python3

"""Insert data from collectData.py into a neo4j database and query it.
"""

import glob
import json
import neo4j
import neo4j.v1
import neo4j.exceptions
import os.path


dataDir = "data/"
jsonDir = os.path.join(dataDir, "json")

def main():
    populateNeo4j(jsonDir, True)
    queryNeo4j()


def populateNeo4j(jsonDir, clearDb=False):
    "Load the JSON results from google into neo4j"

    driver = neo4j.v1.GraphDatabase.driver(
        "bolt://localhost:7687", auth=neo4j.v1.basic_auth("neo4j", "cisc7610"))
    session = driver.session()

    # From: https://stackoverflow.com/a/29715865/2037288
    deleteQuery = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]-()
    WITH n,r LIMIT 50000
    DELETE n,r
    RETURN count(n) as deletedNodesCount
    """

    # TODO: update insert query to include all necessary entities and
    # relationships at once
    insertQuery = """
    WITH {json} as q
    MERGE (img:Image {url:q.url})
      ON CREATE SET img.isDocument = "true"
      ON MATCH  SET img.isDocument = "true"
    """

    countQuery = """
    MATCH (a) WITH DISTINCT LABELS(a) AS temp, COUNT(a) AS tempCnt
    UNWIND temp AS label
    RETURN label, SUM(tempCnt) AS cnt
    ORDER BY label
    """

    if clearDb:
        result = session.run(deleteQuery)
        for record in result:
            print("Deleted", record["deletedNodesCount"], "nodes")

    loaded = 0
    for jsonFile in glob.glob(os.path.join(jsonDir, '*.json')):
        print("Loading", jsonFile, "into neo4j")
        with open(jsonFile) as jf:
            jsonData = json.load(jf)
            try:
                session.run(insertQuery, {"json": jsonData})
                loaded += 1
            except neo4j.exceptions.ClientError as ce:
                print(" ^^^^ Failed:", str(ce))

    print("\nLoaded", loaded, "JSON documents into Neo4j\n")

    queryNeo4jAndPrintResults(countQuery, session, "Neo4j now contains")

    session.close()


def queryNeo4j():
    driver = neo4j.v1.GraphDatabase.driver(
        "bolt://localhost:7687", auth=neo4j.v1.basic_auth("neo4j", "cisc7610"))
    session = driver.session()

    # 0. Count the total number of images in the database
    query_0 = """
    MATCH (n:Image) RETURN count(n) as cnt
    """
    queryNeo4jAndPrintResults(query_0, session, title="Query 0")
    
    # TODO: 1. Count the total number of JSON documents in the database
    query_1 = """
    """
    queryNeo4jAndPrintResults(query_1, session, title="Query 1")

    # TODO: 2. Count the total number of Images, Labels, Landmarks,
    # Locations, Pages, and WebEntity's in the database.
    query_2 = """
    """
    queryNeo4jAndPrintResults(query_2, session, title="Query 2")

    # TODO: 3. List all of the Images that are associated with the
    # Label with an id of "/m/015kr" (which has the description
    # "bridge") ordered by the score of the association between them
    # from highest to lowest
    query_3 = """
    """
    queryNeo4jAndPrintResults(query_3, session, title="Query 3")

    # TODO: 4. List the 10 most frequent WebEntitys that are applied
    # to the same Images as the Label with an id of "/m/015kr" (which
    # has the description "bridge"). List them in descending order of
    # the number of times they appear, followed by their entityId
    # alphabetically
    query_4 = """
    """
    queryNeo4jAndPrintResults(query_4, session, title="Query 4")

    # TODO: 5. Find Images associated with Landmarks that are not "New
    # York" (id "/m/059rby") or "New York City" (id "/m/02nd ")
    # ordered alphabetically by landmark description and then by image
    # URL.
    query_5 = """
    """
    queryNeo4jAndPrintResults(query_5, session, title="Query 5")

    # TODO: 6. List the 10 Labels that have been applied to the most
    # Images along with the number of Images each has been applied to
    query_6 = """
    """
    queryNeo4jAndPrintResults(query_6, session, title="Query 6")

    # TODO: 7. List the 10 Pages that are linked to the most Images
    # through the webEntities.pagesWithMatchingImages JSON property
    # along with the number of Images linked to each one. Sort them by
    # count (descending) and then by page URL.
    query_7 = """
    """
    queryNeo4jAndPrintResults(query_7, session, title="Query 7")

    # TODO: 8. List the 10 pairs of Images that appear on the most
    # Pages together through the webEntities.pagesWithMatchingImages
    # JSON property. Order them by the number of pages that they
    # appear on together (descending), then by the URL of the
    # first. Make sure that each pair is only listed once regardless
    # of which is first and which is second.
    query_8 = """
    """
    queryNeo4jAndPrintResults(query_8, session, title="Query 8")

    # All done!
    session.close()


def queryNeo4jAndPrintResults(query, session, title="Running query:"):
    print()
    print(title)
    print(query)

    if not query.strip():
        return
    
    for record in session.run(query):
        print(" " * 4, end="")
        for field in record:
            print(record[field], end="\t")
        print()


if __name__ == '__main__':
    main()
