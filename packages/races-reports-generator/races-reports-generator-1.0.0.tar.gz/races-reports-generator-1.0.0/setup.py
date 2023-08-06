from setuptools import setup, find_packages

setup(
    name="races-reports-generator",
    version="1.0.0",
    author="Drakosha295",
    description="Just races reports generator",
    packages=find_packages("src"),
    package_dir={"": "src"},
	install_requires=[
        "pytest",
        "numpy"
    ],
	entry_points={"console_scripts": ["races_reports_generator = src.__main__:main"]},
	test_suite="tests",
	include_package_data=True
)