"""Nox configuration for automated development tasks."""

import nox


@nox.session
def tests(session):
    """Run tests with pytest."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    session.run("poetry", "run", "pytest", external=True)


@nox.session
def lint(session):
    """Run linting checks."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    
    # Black formatting check
    session.run("poetry", "run", "black", "--check", "src", "tests", external=True)
    
    # isort import sorting check
    session.run("poetry", "run", "isort", "--check-only", "src", "tests", external=True)
    
    # flake8 linting (priorizando Black, ignorando E501)
    session.run(
        "poetry", "run", "flake8",
        "src", "tests",
        "--max-line-length=88",
        "--extend-ignore=E203,W503,E501",
        external=True
    )


@nox.session
def format(session):
    """Format code with black and isort."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    
    session.run("poetry", "run", "black", "src", "tests", external=True)
    session.run("poetry", "run", "isort", "src", "tests", external=True)


@nox.session
def typecheck(session):
    """Run type checking with mypy."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    session.run("poetry", "run", "mypy", "src", external=True)


@nox.session
def ci(session):
    """Run all CI checks."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    
    # Run all checks
    session.run("poetry", "run", "black", "--check", "src", "tests", external=True)
    session.run("poetry", "run", "isort", "--check-only", "src", "tests", external=True)
    session.run("poetry", "run", "flake8", "src", "tests", "--max-line-length=88", "--extend-ignore=E203,W503,E501", external=True)
    session.run("poetry", "run", "mypy", "src", external=True)
    session.run("poetry", "run", "pytest", external=True)
    
    session.log("✅ All CI checks passed!")


@nox.session
def dev(session):
    """Setup development environment."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    session.run("poetry", "run", "pre-commit", "install", external=True)
    
    session.log("🚀 Development environment ready!")
    session.log("Available commands:")
    session.log("  nox -s tests     # Run tests")
    session.log("  nox -s lint      # Run linting")
    session.log("  nox -s format    # Format code")
    session.log("  nox -s ci        # Run all checks") 


@nox.session
def digitavel(session):
    """Roda apenas os testes do digitavel (unificado, avancado, split)."""
    session.install("poetry")
    session.run("poetry", "install", "--only", "main,dev", external=True)
    session.run(
        "poetry", "run", "pytest",
        "src/tests/test_digitavel.py",
        "src/tests/test_digitavel_avancado.py",
        "src/tests/test_split_digitavel.py",
        external=True
    )


@nox.session
def clean(session):
    """Clean up temporary files."""
    session.run("poetry", "run", "pre-commit", "clean", external=True)
    session.log("✅ Cleaned up temporary files.") 