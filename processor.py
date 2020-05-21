from numbers import Real
from operator import add, mul
from sys import exit
from typing import Any, Callable, Dict, List, NoReturn, Optional, Tuple, Union

Element = float
MatrixElements = List[Element]
MatrixParameters = Tuple[int, int, MatrixElements]

__all__ = ['Matrix']


class Matrix:
    __slots__ = ['rows', 'columns', 'elements']

    def __init__(
            self,
            __rows: Optional[int] = None,
            __columns: Optional[int] = None,
            *,
            elements: Optional[MatrixElements] = None,
            alias: Optional[str] = '',
    ) -> None:
        if not (__rows and __columns and elements):
            __rows, __columns, elements = self.read_matrix_parameters_from_input(alias)
        if len(elements) != (__rows * __columns):
            raise ValueError
        self.rows: int = __rows
        self.columns: int = __columns
        self.elements: MatrixElements = elements

    def __str__(self) -> str:
        c = self.columns
        return '\n'.join(
            ' '.join(map(str, self.elements[c * r: c * r + c]))
            for r in range(self.rows)
        )

    def __repr__(self) -> str:
        return f"Matrix {self.rows},{self.columns}({self.elements})"

    def __add__(self, other: Any) -> Union['Matrix', None]:
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

    def matrix_mul(self, other: 'Matrix') -> Union['Matrix', NoReturn]:
        if not isinstance(other, type(self)):
            raise TypeError
        if self.columns != other.rows:
            raise ValueError
        elements: MatrixElements = list()
        self_row: MatrixElements
        other_column: MatrixElements
        for r in range(self.rows):
            first_element: int = r * self.columns
            self_row = self.elements[first_element: first_element + self.columns:]
            for c in range(other.columns):
                other_column = other.elements[c:: other.columns]
                elements.append(sum(mul(*pair) for pair in zip(self_row, other_column)))
        return Matrix(self.rows, other.columns, elements=elements)

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


def print_result(matrix: Matrix) -> None:
    print("The result is:", matrix, "", sep='\n')


def addition() -> None:
    # Stage #1: Addition
    matrix_a: Matrix = Matrix(alias='first')
    matrix_b: Matrix = Matrix(alias='second')
    matrix: Optional[Matrix] = matrix_a + matrix_b
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


def main() -> NoReturn:
    menu_options: Dict[str, Tuple[str, Callable[..., Any]]] = {
        '1': ("Add matrices", addition),
        '2': ("Multiply matrix by a constant", multiplication_by_number),
        '3': ("Multiply matrices", matrix_by_matrix_multiplication),
        '0': ("Exit", exit),
    }
    while True:
        print(*(f"{num}. {value[0]}" for num, value in menu_options.items()), sep='\n')
        choice = input("Your choice: ")
        if choice in menu_options:
            try:
                menu_options[choice][1]()
            except (ValueError, NotImplementedError, TypeError):
                print("The operation cannot be performed.\n")


if __name__ == '__main__':
    main()
