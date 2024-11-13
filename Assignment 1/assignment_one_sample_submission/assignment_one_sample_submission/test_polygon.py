from polygon import polygon
from pytest import fixture

"""
IMPORTANT: This file requires pytest-mock is installed: `pip install pytest-mock`.
"""

class TestPolygon:

    @fixture
    def triangle_stub1(self, mocker):
        return mocker.patch('polygon.triang', return_value="Scale")

    @fixture
    def quadrilateral_stub1(self,  mocker):
        return mocker.patch('polygon.quadrilateral', return_value="IrrQuad")

    @fixture
    def output_fixture(self, capsys):
        polygon([1,2,2,4,5,3,5,4])
        out, err = capsys.readouterr()
        return out.strip()

    def test_open_file(self):
        try:
            with open("README.md", 'r') as file:
                file.read()
            assert True is True
        except FileNotFoundError:
            assert True is False

    def test_int_input(self):
        assert polygon(1)== "Input is not a list"

    def test_float_input(self):
        assert polygon(0.5)== "Input is not a list"

    def test_string_input(self):
        assert polygon("notPoly")== "Input is not a list"

    def test_EC1(self):
        assert polygon([1])== "Not a polygon"

    def test_EC2_with_triangle_stub(self, triangle_stub1):
        # Call the polygon function, which will use the stubbed triang function
        result = polygon([1, 2, 3])

        # Assert that the triang function was called with the correct arguments
        triangle_stub1.assert_called_once_with(1, 2, 3)

    def test_EC3_with_quadrilateral_stub(self, quadrilateral_stub1):
        # Call the polygon function, which will use the stubbed quadrilateral function
        result = polygon([1, 2, 3, 4])

        # Assert that the quadrilateral function was called with the correct arguments
        quadrilateral_stub1.assert_called_once_with(1, 2, 3, 4)

    def test_EC4_four(self):
        assert polygon([1, 2, 3, 4, 5])== "Large Polygon"

    def test_EC4_with_output(self, output_fixture, capsys):
        assert output_fixture == "This is a large polygon"
