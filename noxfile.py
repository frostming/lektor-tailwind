import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
@nox.parametrize("lektor_version", ["dev", "stable"])
def tests(session: nox.Session, lektor_version: str):
    if lektor_version == "dev":
        session.install("git+https://github.com/lektor/lektor.git")
    else:
        # Install Lektor stable
        session.install("-U", "lektor")

    # Install Pytest
    session.install("-U", "pytest")
    session.install(".")

    # 运行测试
    session.run("pytest", "tests", *session.posargs)
