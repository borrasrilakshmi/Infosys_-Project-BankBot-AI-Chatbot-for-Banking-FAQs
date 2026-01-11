def parse_query(query):
    return query.lower().strip()

def test_query_parser():
    query = "  CHECK Balance "
    parsed = parse_query(query)
    assert parsed == "check balance"
