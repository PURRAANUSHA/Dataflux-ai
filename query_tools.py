def explain_query(sql):

    explanation = f"""
    This SQL query does the following:

    {sql}

    It retrieves data from the dataset and returns the result.
    """

    return explanation