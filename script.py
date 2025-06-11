import csv
import logging
from enum import Enum
from typing import Any

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

    def __init__(self) -> None:
        self._package_data = self._ingest_csv()
        self._result_data = {
            "standard": {"total": 0, "percentage": 0.0},
            "rejected": {"total": 0, "percentage": 0.0},
            "special": {"total": 0, "percentage": 0.0},
        }

    @staticmethod
    def _ingest_csv() -> list[dict[str, Any]]:
        """Method responsible to ingest a csv and converting the data
        Returns:
            list[dict[str, Any]]: Return a list with all information converted.
        """
        data = csv.DictReader(open("packages.csv"))
        result = [item for item in data]
        return result

    def _validate_units(self, package: dict[str, Any]) -> dict[str, float]:
        """Function responsible for validate all entry data.
        Args:
            package (dict[str, Any]): Receives the package data.
        Returns:
            dict[str, float]: Returns converted values as floats
        Raises:
            ValueError: Raise a error if a value is not a valid number or is
            less than or equal to 0.
        """
        fields = ["width", "height", "length", "mass"]
        converted_values = {}

        for field in fields:
            value = package.get(field) or package.get(field.capitalize())
            try:
                if value is None or value == "" or str(value).strip().lower() == "none":
                    raise ValueError(
                        f"The value of the ‘{field}’ field must be a valid number! Value received: {value}"
                    )

                number = float(value)
                converted_values[field] = number

            except (ValueError, TypeError):
                raise ValueError(f"The value of the ‘{field}’ field must be a valid number! Value received: {value}")

        for field, value in converted_values.items():
            if value <= 0:
                msg = "Validating units: width={}cm, height={}cm, length={}cm, mass={}kg".format(
                    converted_values["width"],
                    converted_values["height"],
                    converted_values["length"],
                    converted_values["mass"],
                )
                console.log(f"[bold yellow]{msg}[/bold yellow]")
                raise ValueError("All dimensions and mass must be positive values.")

        return converted_values

    def _is_bulky(self, package: dict[str, Any]) -> bool:
        """Function responsible for calculate and check if with all dimension
        values the package is bulky.
        Returns:
            bool: Return an boolean based on validation
        """
        volume = package["width"] * package["height"] * package["length"]
        result = any(
            [
                volume >= Limits.BULKY_LIMIT.value,
                package["width"] >= Limits.WIDTH_LIMIT.value,
                package["height"] >= Limits.HEIGHT_LIMIT.value,
                package["length"] >= Limits.LENGTH_LIMIT.value,
            ]
        )
        return result

    def sort(self) -> dict[str, Any]:
        """Function responsible for sort and define the package type.
        Returns:
            dict[str, Any]: Return the result data with package counts
            and percentages
        """
        error_count = 0
        processed_count = 0
        total_packages = len(self._package_data)

        console.log(f"[bold blue]Processing {total_packages} packages...[/bold blue]")

        for i, data in enumerate(self._package_data, 1):
            try:
                converted_data = self._validate_units(data)
                bulky = self._is_bulky(converted_data)
                is_heavy = converted_data["mass"] >= Limits.HEAVY_LIMIT.value
                result = PackageType.STANDARD.value

                if bulky and is_heavy:
                    result = PackageType.REJECTED.value
                elif bulky or is_heavy:
                    result = PackageType.SPECIAL.value

                self._result_data[result.lower()]["total"] += 1
                processed_count += 1

            except ValueError as e:
                error_count += 1
                console.log(f"[bold red]❌ Error in the package {i}: {e}[/bold red]")
                continue

        console.log("[bold yellow]📊 Process report:[/bold yellow]")
        console.log(f"[bold yellow]   • Total packages: {total_packages}[/bold yellow]")
        console.log(f"[bold yellow]   • Packages processed: {processed_count}[/bold yellow]")
        console.log(f"[bold yellow]   • Packages with error: {error_count}[/bold yellow]")

        if error_count > 0:
            console.log(f"[bold yellow]⚠️ {error_count} packages were ignored due to validation errors[/bold yellow]")

        self._calculate_percentage()
        return self._result_data

    def _calculate_percentage(self):
        """Method responsible to create the percentage based on totals values
        for package each type"""
        total_processed = sum(item["total"] for item in self._result_data.values())
        if total_processed > 0:
            for item in self._result_data.values():
                percentage_value = (item["total"] / total_processed) * 100
                item["percentage"] = f"{percentage_value:.2f}%"
        else:
            console.log("[bold red]No package has been processed successfully![/bold red]")


@click.command()
def main():
    """Main function responsible to execute the script"""
    console.log("[bold green]Starting the package sorting process...[/bold green]")
    try:
        package_types = [item.value for item in PackageType]
        package = PackageSorter()
        result = package.sort()

        console.log("[bold green]" + "=" * 50 + "[/bold green]")
        console.log("[bold green]📦 FINAL RESULTS[/bold green]")
        console.log("[bold green]" + "=" * 50 + "[/bold green]")

        for type_value in package_types:
            value = result[type_value.lower()]
            console.log(f"[bold cyan]📋 Package type: {type_value}[/bold cyan]")
            console.log(f"[bold cyan]📊 Package total: {value['total']}[/bold cyan]")
            console.log(f"[bold cyan]📈 Package percentage: {value['percentage']}[/bold cyan]")
            console.log("")
            console.log("[bold green]✅ Processing completed successfully![/bold green]")

    except Exception as e:
        console.log(f"[bold red]💥 Critical error: {e}[/bold red]")
        raise


if __name__ == "__main__":
    main()
