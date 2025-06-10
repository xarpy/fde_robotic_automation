import logging
from enum import Enum

import click
from rich.console import Console
from rich.logging import RichHandler

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("rich")


class Limits(Enum):
    """Classe Limits definindo valores default das dimensões"""

    BULKY_LIMIT = 1000000
    WIDTH_LIMIT = 150
    HEIGHT_LIMIT = 150
    LENGTH_LIMIT = 150
    HEAVY_LIMIT = 20


class PackageType(Enum):
    """Classe PackageType definindo valores deafult para os tipos"""

    STANDARD = "STANDARD"
    REJECTED = "REJECTED"
    SPECIAL = "SPECIAL"


class PackageSorter:
    """Package Sorter class"""

    def __init__(self, width: float, height: float, length: float, mass: float) -> None:
        self._width = width
        self._height = height
        self._length = length
        self._mass = mass

    def _validate_units(self) -> None:
        """Function responsible for validate all entry data.
        Raises:
            ValueError: Raise a error if a value is less than 0!
        """
        result = all([self._width > 0, self._height > 0, self._length > 0, self._mass > 0])
        if not result:
            msg = f"Validating units: width={self._width}cm, height={self._height}cm, length={self._length}cm, mass={self._mass}kg"
            console.log(f"[bold yellow]{msg}[/bold yellow]")
            raise ValueError("All dimensions and mass must be positive values.")

    def _is_bulky(self) -> bool:
        """Function responsible for calculate and check if with all dimension
        values the package is bulky.
        Returns:
            bool: Return an boolean based on validation
        """
        volume = self._width * self._height * self._length
        result = any(
            [
                volume >= Limits.BULKY_LIMIT.value,
                self._width >= Limits.WIDTH_LIMIT.value,
                self._height >= Limits.HEIGHT_LIMIT.value,
                self._length >= Limits.LENGTH_LIMIT.value,
            ]
        )
        return result

    def sort(self) -> str:
        """Function responsible for sort and define the package type.
        Returns:
            str: Return an boolean based on validation
        """
        self._validate_units()
        is_heavy = self._mass >= Limits.HEAVY_LIMIT.value
        bulky = self._is_bulky()
        result = PackageType.STANDARD.value
        if bulky and is_heavy:
            result = PackageType.REJECTED.value
        elif bulky or is_heavy:
            result = PackageType.SPECIAL.value
        return result


@click.command()
@click.argument("width", type=float)
@click.argument("height", type=float)
@click.argument("length", type=float)
@click.argument("mass", type=float)
def main(width: float, height: float, length: float, mass: float):
    """Main function responsible to execute the script"""
    console.log("[bold green]Starting the package sorting process...[/bold green]")
    try:
        package = PackageSorter(width, height, length, mass)
        result = package.sort()
        console.log(f"[bold cyan]Package sorted into: {result}[/bold cyan]")
    except ValueError as e:
        console.log(f"[bold red]Error: {e}[/bold red]")


if __name__ == "__main__":
    main()
