from clmgr.tests.test_base import run_test_config


def test_comments_java():
    run_test_config("java/", "Comments.java", "comments.yml")


def test_comments_typescript():
    run_test_config("ts/", "comments.component.ts", "comments.yml")


def test_comments_python():
    run_test_config("py/", "comments.py", "comments.yml")


def test_comments_dotnet():
    run_test_config("cs/", "Comments.cs", "comments.yml")
