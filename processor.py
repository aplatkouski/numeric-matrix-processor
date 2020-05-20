from typing import Any, List, Optional, Tuple, Union

MatrixElements = List[int]

__all__ = ['Matrix']


class Matrix:
    __slots__ = ['rows', 'columns', 'elements']

    def __init__(
            self,
            __rows: Optional[int] = None,
            __columns: Optional[int] = None,
            *,
            elements: Optional[MatrixElements] = None,
    ) -> None:
        if not (__rows and __columns and elements):
            __rows, __columns, elements = self.read_matrix_params_from_input()
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
        if self.rows != other.rows or self.columns != other.columns:
            # this is requirement of task
            print("ERROR")
            return None
        elements: MatrixElements = list(map(sum, zip(self.elements, other.elements)))
        return Matrix(self.rows, self.columns, elements=elements)

    @staticmethod
    def read_matrix_params_from_input() -> Tuple[int, int, MatrixElements]:
        rows, columns = map(int, input().split(' ', 1))
        elements: MatrixElements = list()
        for _ in range(rows):
            row: List[int] = list(map(int, input().split()))
            if len(row) != columns:
                raise ValueError
            elements.extend(row)
        return rows, columns, elements


def addition() -> None:
    matrix_a: Matrix = Matrix()
    matrix_b: Matrix = Matrix()
    matrix = matrix_a + matrix_b
    if matrix:
        print(matrix)


if __name__ == '__main__':
    addition()
