from parser.parser import StatementParser

def test_sample_parse():
    parser = StatementParser()
    result = parser.parse("samples/chase_sample.pdf")
    assert result.issuer in ["Chase", "Unknown"]
    assert result.last4 is not None
    assert result.total_balance is not None
