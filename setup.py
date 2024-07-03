import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
__version__ = "0.0.0"

REPO_NAME = "Algorithmic"
AUTHOR_USER_NAME = "GL3MON"
SRC_REPO = "Algorithmic"
AUTHOR_EMAIL = "harisshragavarchives@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Multi-Agent System designed to tackle complex coding challenges requiring high-level reasoning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir = {"": "src"},
    packages= setuptools.find_packages(where="src"),
)