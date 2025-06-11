
# Package Sort Challenge

[![Python Version][python-image]][python-url]

A simple Python script to sort packages based on dimensions (width, height, length) and mass. We have a version on Repl.it, you can take look on there: [Repl.it](https://replit.com/@xarpy/fderoboticautomation#script.py)

## Installation

### Local Environment Setup

1. **Create a virtual environment** using your preferred dependency manager. For more information on dependency managers, follow this [link](https://ahmed-nafies.medium.com/pip-pipenv-poetry-or-conda-7d2398adbac9).

2. **Install dependencies**:

   Navigate to the project folder and install the dependencies using **pip**:

   ```sh
   pip install --upgrade pip
   pip install -r requirements/dev.txt
   ```

3. **Run the project**:

   After installing the dependencies, run the script with:

   ```sh
   python script.py <arg1> <arg2> <arg3> <arg4>
   ```

### Docker Setup

If you prefer to run the project in a containerized environment, follow these steps:

1. **Ensure Docker Compose is installed**.

2. **Build and run the container**:

   ```sh
   docker-compose up --build
   ```

## Usage

This project follows **Clean Code** and **SOLID** principles to ensure readability and maintainability. For more details, check out the resources section below.

### Formatters and Linters

We use the following tools to maintain code quality:

* [Flake8](https://flake8.pycqa.org/en/latest/index.html) - Linter
* [Black](https://black.readthedocs.io/en/stable/) - Code formatter
* [Isort](https://isort.readthedocs.io/en/latest/) - Imports sorter

**Coding Style Conventions**:

- **snake_case** for variables, functions, and methods.
- **PascalCase** for classes.
- Configuration variables should be written in **UPPERCASE**.

### Project Structure

The project is organized according to the principles of **Clean Code** and **SOLID**. Here's a summary of the structure:

```sh
./
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── script.py
└── tests.py
```

### Tests

The project uses **pytest** for unit testing. Here’s how you can run the tests in both local and containerized environments.

#### Local Environment

1. **List available tests**:

   ```sh
   pytest --co
   ```

2. **Run all tests**:

   ```sh
   pytest tests/
   ```

3. **Run a specific test module**:

   ```sh
   pytest tests/<module-you-want-to-test>.py
   ```

4. **Run a specific test function in a module**:

   ```sh
   pytest tests/<module-you-want-to-test>.py::<function_name>
   ```

#### Container Environment

1. **List available tests inside the container**:

   ```sh
   docker-compose run app pytest --co
   ```

2. **Run all tests inside the container**:

   ```sh
   docker-compose run app pytest tests/
   ```

3. **Run a specific test module inside the container**:

   ```sh
   docker-compose run app pytest tests/<module-you-want-to-test>.py
   ```

4. **Run a specific test function inside the container**:

   ```sh
   docker-compose run app pytest tests/<module-you-want-to-test>.py::<function_name>
   ```

## Resources and Documentation

Here are some useful links for setting up the environment and understanding the tools used:

* [Pip (Python Package Installer)](https://pip.pypa.io/en/stable/)
* [Pre-commit hooks](https://pre-commit.com/index.html)
* [EditorConfig](https://editorconfig.org/)
* [Pip Tools](https://github.com/jazzband/pip-tools)
* [Click Documentation](https://click.palletsprojects.com/en/8.1.x/)
* [Docker Documentation](https://docs.docker.com/get-started/)
* [Docker Compose Documentation](https://docs.docker.com/compose/)

## Contributing

We welcome contributions! Please feel free to submit a pull request. For major changes, open an issue first to discuss your suggestions.

When contributing, make sure to:

- Follow the code style guidelines.
- Add or update tests where appropriate.

[python-url]: https://www.python.org/dev/peps/pep-0596/
[python-image]: https://img.shields.io/badge/python-v3.12-blue
