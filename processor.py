from numbers import Real
from operator import add, mul
from sys import exit
from typing import Any, Callable, Dict, List, Optional, Tuple

Element = float
MatrixElements = List[Element]
MatrixParameters = Tuple[int, int, MatrixElements]
Choice = Tuple[str, Callable[..., Any]]
MenuOptions = Dict[str, Choice]

__all__ = ['Matrix']


class Matrix:
    def __init__(
            self,
            __rows: Optional[int] = None,
            __columns: Optional[int] = None,
            *,
            elements: Optional[MatrixElements] = None,
            alias: Optional[str] = '',
    ) -> None:
        if __rows is None or __columns is None or elements is None:
            __rows, __columns, elements = self.read_matrix_parameters_from_input(alias)
        if len(elements) != (__rows * __columns):
            raise ValueError
        self.rows: int = __rows
        self.columns: int = __columns
        self.elements: MatrixElements = elements

    def __str__(self) -> str:
        return '\n'.join(' '.join(map(str, self.row(r))) for r in range(self.rows))

    def __repr__(self) -> str:
        return f"Matrix {self.rows},{self.columns}({self.elements})"

    def __add__(self, other: Any) -> 'Matrix':
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError
        elements: MatrixElements
        elements = list(add(*pair) for pair in zip(self.elements, other.elements))
        return Matrix(self.rows, self.columns, elements=elements)

    def __mul__(self, other: Any) -> 'Matrix':
        if isinstance(other, Real):
            elements: MatrixElements = list(e * other for e in self.elements)
            return Matrix(self.rows, self.columns, elements=elements)
        else:
            raise NotImplementedError

    @staticmethod
    def read_matrix_parameters_from_input(
            alias: Optional[str] = '',
    ) -> MatrixParameters:
        print(
            "Enter size of", f" {alias} " if alias else " ", "matrix:", sep='', end=' '
        )
        rows, columns = map(int, input().split(' ', 1))
        elements: MatrixElements = list()
        row: MatrixElements
        print("Enter", f" {alias} " if alias else " ", "matrix:", sep='')
        for _ in range(rows):
            row = [float(x) if '.' in x else int(x) for x in input().split()]
            if len(row) != columns:
                raise ValueError
            elements.extend(row)
        return rows, columns, elements

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self.rows, self.columns

    def row(self, n: int = 0) -> MatrixElements:
        if 0 <= n < self.rows:
            return self.elements[n * self.columns: n * self.columns + self.columns:]
        else:
            raise IndexError

    def column(self, n: int = 0) -> MatrixElements:
        if 0 <= n < self.columns:
            return self.elements[n:: self.columns]
        else:
            raise IndexError

    def reinitialize(
            self,
            rows: Optional[int] = None,
            columns: Optional[int] = None,
            elements: Optional[MatrixElements] = None,
            alias: Optional[str] = '',
    ) -> None:
        if rows is None or columns is None or elements is None:
            rows, columns, elements = self.read_matrix_parameters_from_input(alias)
        if len(elements) != (rows * columns):
            raise ValueError
        self.rows = rows
        self.columns = columns
        self.elements = elements

    def matrix_mul(self, other: 'Matrix') -> 'Matrix':
        if not isinstance(other, type(self)):
            raise TypeError
        if self.columns != other.rows:
            raise ValueError
        elements: MatrixElements = list()
        self_row: MatrixElements
        other_column: MatrixElements
        for r in range(self.rows):
            for c in range(other.columns):
                elements.append(
                    sum(mul(*pair) for pair in zip(self.row(r), other.column(c)))
                )
        return Matrix(self.rows, other.columns, elements=elements)

    def transpose_at_main_diagonal(self) -> None:
        elements: MatrixElements = list()
        for c in range(self.columns):
            elements.extend(self.column(c))
        self.reinitialize(self.columns, self.rows, elements=elements)

    def transpose_at_side_diagonal(self) -> None:
        elements: MatrixElements = list()
        for c in reversed(range(self.columns)):
            elements.extend(reversed(self.column(c)))
        self.reinitialize(self.columns, self.rows, elements=elements)

    def transpose_at_vertical_line(self) -> None:
        elements: MatrixElements = list()
        for r in range(self.rows):
            elements.extend(reversed(self.row(r)))
        self.reinitialize(self.rows, self.columns, elements=elements)

    def transpose_at_horizontal_line(self) -> None:
        elements: MatrixElements = list()
        for r in reversed(range(self.rows)):
            elements.extend(self.row(r))
        self.reinitialize(self.rows, self.columns, elements=elements)


def make_choice(options: MenuOptions) -> Choice:
    print(*(f"{num}. {value[0]}" for num, value in options.items()), sep='\n')
    option: str = ''
    while option not in options:
        option = input("Your choice: ")
    return options[option]


def print_result(matrix: Matrix) -> None:
    print("The result is:", matrix, "", sep='\n')


def addition() -> None:
    # Stage #1: Addition
    matrix_a: Matrix = Matrix(alias='first')
    matrix_b: Matrix = Matrix(alias='second')
    matrix: Matrix = matrix_a + matrix_b
    if matrix:
        print_result(matrix)


def multiplication_by_number() -> None:
    # Stage 2: Multiplication by number
    matrix: Matrix = Matrix()
    constant: str = input("Enter constant: ")
    number: float = float(constant) if '.' in constant else int(constant)
    print_result(matrix * number)


def matrix_by_matrix_multiplication() -> None:
    # Stage 3: Matrix by matrix multiplication
    matrix_a: Matrix = Matrix(alias='first')
    matrix_b: Matrix = Matrix(alias='second')
    print_result(matrix_a.matrix_mul(matrix_b))


def transpose_matrix() -> None:
    # Stage 4: Transpose
    matrix: Matrix = Matrix(0, 0, elements=[])
    transpose_options: MenuOptions = {
        '1': ("Main diagonal", matrix.transpose_at_main_diagonal),
        '2': ("Side diagonal", matrix.transpose_at_side_diagonal),
        '3': ("Vertical line", matrix.transpose_at_vertical_line),
        '4': ("Horizontal line", matrix.transpose_at_horizontal_line),
    }
    choice: Choice = make_choice(transpose_options)
    matrix.reinitialize()
    choice[1]()
    print_result(matrix)


def main() -> None:
    menu_options: MenuOptions = {
        '1': ("Add matrices", addition),
        '2': ("Multiply matrix by a constant", multiplication_by_number),
        '3': ("Multiply matrices", matrix_by_matrix_multiplication),
        '4': ("Transpose matrix", transpose_matrix),
        '0': ("Exit", exit),
    }
    while True:
        choice: Choice = make_choice(menu_options)
        try:
            choice[1]()
        except (ValueError, NotImplementedError, TypeError):
            print("The operation cannot be performed.\n")


if __name__ == '__main__':
    main()
