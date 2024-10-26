# Contributing

We’re excited that you want to contribute! This project is a learning journey for everyone involved, and we welcome improvements, bug fixes, or new features. Whether you're a beginner or experienced developer, your input matters.

## How to Contribute

1. Fork the Repository

Click the **Fork** button on the repository page to create your copy.

2. Clone Your Fork

```bash
git clone https://github.com/your-username/super-mario-clone.git
cd super-mario-clone
```

3. Set Up Your Environment

Make sure you’re using a virtual environment with Pygame, Ruff, and Black installed.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

4. Create a New Branch

```bash
git checkout -b feature-name
```

## Code Style Guidelines

Ruff: Run Ruff to catch linting issues.

```bash
ruff check path/to/main
```

Black: Ensure your code is formatted properly with Black.

```bash
    black path/to/main
```

## Making a Pull Request

1. Stage and commit your changes:

```bash
git add .
git commit -m "Add: [Description of your change]"
```

2. Push your branch:
```bash
    git push origin feature-name
```
3. Open a pull request on the original repository.

## What to Include in Your PR
- A clear description of the change or feature.
- Screenshots or videos, if applicable.
- Make sure the code is properly formatted and linted.

## Reporting Issues

If you encounter any bugs or want to suggest features, please open an Issue on the repository. Be sure to include:

- A detailed description of the issue or feature.
- Steps to reproduce, if it’s a bug.
- Any relevant screenshots or logs.

## Code of Conduct

We want this project to be a learning experience for everyone. Please keep conversations respectful and constructive. We're all here to improve and have fun building together. 😊

Thank you for contributing!
