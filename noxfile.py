import nox


@nox.session
def black(session):
    session.install("black")
    session.run("black", "src", "setup.py", "noxfile.py", "tests")


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "src")


@nox.session
def tests(session):
    session.install("pytest")
    session.install("pytest-cov")
    session.install("-e", ".")
    session.run("pytest", "--cov=src", "tests")


@nox.session
def build_docs(session):
    session.install("-r", "requirements-docs.txt")
    session.install("-e", ".")
    session.run(
        "sphinx-apidoc",
        "-o",
        "docs/reference",
        "--separate",
        "-a",
        "-f",
        "src/pymetager",
    )
