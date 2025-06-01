import nox

@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.run("pytest", "test/test_merge.py")