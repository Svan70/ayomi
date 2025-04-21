import pytest
from fastapi.testclient import TestClient

from .constants import InvalidExpression, Operators
from .core import compute_expression, parse_expression
from .main import app
from .models import Operation, convert_operations_to_csv


class TestComputeExpression:

    def test_basic_operations(self):
        assert compute_expression("5 3 +") == 8.0
        assert compute_expression("10 4 -") == 6.0
        assert compute_expression("6 7 *") == 42.0
        assert compute_expression("20 5 /") == 4.0
        assert compute_expression("2 3 **") == 8.0

    def test_complex_expressions(self):
        # (5 + 3) * 2 = 16
        assert compute_expression("5 3 + 2 *") == 16.0
        # 3 + (4 * 2) = 11
        assert compute_expression("3 4 2 * +") == 11.0
        # (7 - 3) / 2 = 2
        assert compute_expression("7 3 - 2 /") == 2.0
        # 5 + ((1 + 2) * 4) = 17
        assert compute_expression("5 1 2 + 4 * +") == 17.0

    def test_nested_operations(self):
        # ((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1)) = 5
        assert compute_expression("15 7 1 1 + - / 3 * 2 1 1 + + -") == 5.0

    def test_invalid_expressions(self):
        # Not enough operands
        with pytest.raises(InvalidExpression):
            compute_expression("5 +")

        # Too many operands
        with pytest.raises(InvalidExpression):
            compute_expression("5 3 2 +")

        # Invalid expression format
        with pytest.raises(InvalidExpression):
            compute_expression("5 3 + 2")


class TestParseExpression:

    def test_parse_basic_operations(self):
        result = parse_expression("5 3 +")
        assert result == [5.0, 3.0, Operators.ADD]

        result = parse_expression("10 4 -")
        assert result == [10.0, 4.0, Operators.MINUS]

        result = parse_expression("6 7 *")
        assert result == [6.0, 7.0, Operators.MUL]

        result = parse_expression("20 5 /")
        assert result == [20.0, 5.0, Operators.DIV]

        result = parse_expression("2 3 **")
        assert result == [2.0, 3.0, Operators.POW]

    def test_parse_complex_expressions(self):
        result = parse_expression("5 3 + 2 *")
        assert result == [5.0, 3.0, Operators.ADD, 2.0, Operators.MUL]

        # More complex
        result = parse_expression("15 7 1 1 + - / 3 * 2 1 1 + + -")
        expected = [
            15.0,
            7.0,
            1.0,
            1.0,
            Operators.ADD,
            Operators.MINUS,
            Operators.DIV,
            3.0,
            Operators.MUL,
            2.0,
            1.0,
            1.0,
            Operators.ADD,
            Operators.ADD,
            Operators.MINUS,
        ]
        assert result == expected

    def test_parse_invalid_expressions(self):
        """Test parsing invalid expressions."""
        # Invalid token
        with pytest.raises(InvalidExpression):
            parse_expression("5 3 &")

        # Invalid number
        with pytest.raises(InvalidExpression):
            parse_expression("5 abc +")

    def test_parse_empty_expression(self):
        """Test parsing an empty expression."""
        with pytest.raises(InvalidExpression):
            parse_expression("")


class TestComputeExpressionRoute:

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_compute_expression_valid(self, client):
        response = client.post("/compute-expression", json={"expression": "5 3 +"})
        assert response.status_code == 200
        assert response.json() == {"result": 8.0}

    def test_compute_expression_invalid(self, client):
        response = client.post("/compute-expression", json={"expression": "5 3 + - -"})
        assert response.status_code == 400


class TestConvertOperationsToCSV:

    def test_empty_operations_list(self):
        operations = []
        csv_output = convert_operations_to_csv(operations)

        expected_output = "id;expression;result\r\n"
        assert csv_output == expected_output

    def test_multiple_operations(self):
        operations = [
            Operation(id=1, expression="5 3 +", result=8.0),
            Operation(id=2, expression="10 4 -", result=6.0),
            Operation(id=3, expression="6 7 *", result=42.0),
            Operation(id=4, expression="20 5 /", result=4.0),
            Operation(id=5, expression="2 3 **", result=8.0),
        ]

        csv_output = convert_operations_to_csv(operations)

        expected_output = (
            "id;expression;result\r\n"
            "1;5 3 +;8.0\r\n"
            "2;10 4 -;6.0\r\n"
            "3;6 7 *;42.0\r\n"
            "4;20 5 /;4.0\r\n"
            "5;2 3 **;8.0\r\n"
        )

        assert csv_output == expected_output
