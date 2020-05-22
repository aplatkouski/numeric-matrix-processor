from math import sqrt
from numbers import Real
from operator import add, mul
from sys import exit
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

Element = float
MatrixElements = List[Element]
MatrixParameters = Tuple[int, int, MatrixElements]
Choice = Tuple[str, Callable[..., Any]]
MenuOptions = Dict[str, Choice]

__all__ = ['Matrix']


class Matrix:
    """A class to represent a matrix with implementation of basic operations."""

    def __init__(
            self,
            __rows: Optional[int] = None,
            __columns: Optional[int] = None,
            *,
            elements: Optional[MatrixElements] = None,
            alias: Optional[str] = '',
    ) -> None:
        """The constructor for Matrix class.

        If at least one variable from `__rows`, `__columns` or `elements`
        is missing, CLI will be launched to get all parameters from user.

        Args:
            __rows: number of rows.
            __columns: number of columns.
            elements: elements of matrix as a list of numbers.
            alias: matrix alias used on CLI when getting other matrix
                parameters from user.

        Raises:
            ValueError: if number of elements calculated as
                a multiplication `__rows` and `__columns` is not equal
                to the number of elements in the variable `elements`.

        """
        if __rows is None or __columns is None or elements is None:
            __rows, __columns, elements = self._read_matrix_parameters_from_input(alias)
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
        elif isinstance(other, type(self)):
            if self.columns != other.rows:
                raise ValueError
            elements = list()
            self_row: MatrixElements
            other_column: MatrixElements
            for r in range(self.rows):
                for c in range(other.columns):
                    elements.append(
                        sum(mul(*pair) for pair in zip(self.row(r), other.column(c)))
                    )
            return Matrix(self.rows, other.columns, elements=elements)
        else:
            raise TypeError

    @staticmethod
    def _read_matrix_parameters_from_input(
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

    @staticmethod
    def _submatrix(*, square_matrix: MatrixElements, i: int, j: int) -> MatrixElements:
        """Return square submatrix formed by deleting the `i`th row and `j`th column.

        Note:
            All arguments are keyword-only arguments.

        Args:
            square_matrix: square matrix as a list of numbers.
            i: row number from 0 to `size` - 1.
            j: column number from 0 to `size` - 1.

        Returns:
            The square submatrix as a list of numbers.

        Raises:
            IndexError: if `i` or `j` less than zero or
                `i` or `j` greater than or equal to `size`

        """
        size: int = int(sqrt(len(square_matrix)))
        if 0 <= i < size and 0 <= j < size:
            elements: MatrixElements = list()
            for r in range(size):
                if r != i:
                    row = square_matrix[r * size: r * size + size:]
                    # skip element in `j` column
                    elements.extend(row[:j] + row[j + 1:])
            return elements
        else:
            raise IndexError

    @staticmethod
    def _determinant(*, square_matrix: MatrixElements) -> float:
        """Return determinant that computed from a square matrix using the Laplace expansion.

        Args:
            square_matrix: square matrix as a list of numbers.
                It's keyword-only argument.

        Returns:
            The scalar value.

        """
        size: int = int(sqrt(len(square_matrix)))
        if size != 2:
            # compute sum of (i, j) minors (first minors)
            return sum(
                Matrix._determinant(
                    square_matrix=Matrix._submatrix(
                        square_matrix=square_matrix, i=0, j=j
                    )
                )
                * (-1) ** j
                * square_matrix[j]
                for j in range(size)
                # skip `zero` elements
                if square_matrix[j]
            )
        else:
            return (
                    square_matrix[0] * square_matrix[3]
                    - square_matrix[1] * square_matrix[2]
            )

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Return dimensions of matrix as tuple of number of rows and number of columns"""
        return self.rows, self.columns

    @property
    def determinant(self) -> float:
        """Return determinant (scalar value) of matrix"""
        if self.elements and self.rows == self.columns:
            if len(self.elements) == 1:
                return self.elements[0]
            return self._determinant(square_matrix=self.elements)
        else:
            raise AttributeError

    def row(self, n: int = 0) -> MatrixElements:
        """Return `n`-row of matrix.

        Args:
            n: row number from 0 to number of rows - 1.

        Returns:
            row as a list of elements.

        Raises:
            IndexError: if `n` less than zero or greater than or equal to
                number of rows.

        """
        if 0 <= n < self.rows:
            return self.elements[n * self.columns: n * self.columns + self.columns:]
        else:
            raise IndexError

    def column(self, n: int = 0) -> MatrixElements:
        """Return `n`-column of matrix.

        Args:
            n: column number from 0 to number of columns - 1.

        Returns:
            column as a list of elements.

        Raises:
            IndexError: if `n` less than zero or greater than or equal to
                number of columns.

        """
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
        """Rewrite current matrix parameters after some operations or at request

        Todo:
            * rewrite this function or __init__, because it duplicates __init__
        """
        if rows is None or columns is None or elements is None:
            rows, columns, elements = self._read_matrix_parameters_from_input(alias)
        if len(elements) != (rows * columns):
            raise ValueError
        self.rows = rows
        self.columns = columns
        self.elements = elements

    def transpose(self, *, kind: str = "main diagonal") -> None:
        transpose_kinds: Dict[str, Callable[..., Any]] = {
            "main diagonal": self.transpose_at_main_diagonal,
            "side diagonal": self.transpose_at_side_diagonal,
            "vertical line": self.transpose_at_vertical_line,
            "horizontal line": self.transpose_at_horizontal_line,
        }
        if kind.lower() in transpose_kinds:
            transpose_kinds[kind]()
        else:
            raise NotImplementedError

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


def print_result(result: Union[Matrix, float]) -> None:
    print("The result is:", result, "", sep='\n')


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
    print_result(matrix_a * matrix_b)


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


def calculate_determinant() -> None:
    # Stage 5: Determined!
    matrix: Matrix = Matrix()
    print_result(matrix.determinant)


def main() -> None:
    menu_options: MenuOptions = {
        '1': ("Add matrices", addition),
        '2': ("Multiply matrix by a constant", multiplication_by_number),
        '3': ("Multiply matrices", matrix_by_matrix_multiplication),
        '4': ("Transpose matrix", transpose_matrix),
        '5': ("Calculate a determinant", calculate_determinant),
        '0': ("Exit", exit),
    }
    while True:
        choice: Choice = make_choice(menu_options)
        try:
            choice[1]()
        except (AttributeError, IndexError, NotImplementedError, TypeError, ValueError):
            print("The operation cannot be performed.\n")


if __name__ == '__main__':
    main()
