from setuptools import setup, find_packages

setup(
    name="instagram_comment_sentiment_analysis",
    version="0.1.0",
    description="A Python project for analyzing the sentiment of Instagram comments",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "nltk",
        "transformers",
        "torch",
        "emoji",
        "fastapi",
        "uvicorn",
        "pydantic",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "httpx",  # For FastAPI testing
        ],
    },
    python_requires=">=3.8",
)