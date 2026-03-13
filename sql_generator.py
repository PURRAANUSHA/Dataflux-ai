def generate_sql(query):

    query = query.lower()

    if "average price" in query:
        return "SELECT AVG(price) FROM dataset"

    if "show all" in query:
        return "SELECT * FROM dataset"

    return "SELECT * FROM dataset LIMIT 10"