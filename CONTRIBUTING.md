# Contributing to fastapi-secure-errors

Thank you for your interest in contributing to `fastapi-secure-errors`! We welcome contributions from the community and appreciate your help in making this library better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Security Considerations](#security-considerations)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/fastapi-secure-errors.git
   cd fastapi-secure-errors
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/ciscomonkey/fastapi-secure-errors.git
   ```

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Make sure you have it installed.

1. **Install dependencies**:
   ```bash
   uv sync --all-extras
   ```

2. **Install the package in development mode**:
   ```bash
   uv pip install -e .
   ```

3. **Verify your setup** by running the tests:
   ```bash
   uv run pytest tests/ -v
   ```

## Making Changes

1. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make your changes** following the coding standards below

3. **Write or update tests** for your changes

4. **Update documentation** if needed (README.md, docstrings, etc.)

5. **Test your changes**:
   ```bash
   # Run all tests
   uv run pytest tests/ -v
   
   # Run tests with coverage
   uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v
   
   # Run tests quickly (stop on first failure)
   uv run pytest tests/ -x
   ```

## Testing

We maintain high test coverage and all contributions should include appropriate tests.

### Test Structure

- Unit tests for individual components: `tests/test_*.py`
- Integration tests: `tests/test_integration.py`
- All tests should be runnable with `pytest`

### Writing Tests

- Use descriptive test names that explain what is being tested
- Test both success and failure scenarios
- Test edge cases and error conditions
- For security-related features, ensure tests verify that sensitive information is not leaked

### Running Tests

```bash
# All tests with verbose output
uv run pytest tests/ -v

# Tests with coverage report
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v

# Run a specific test file
uv run pytest tests/test_handlers.py -v

# Run tests matching a pattern
uv run pytest tests/ -k "test_secure" -v
```

## Submitting Changes

1. **Ensure all tests pass**:
   ```bash
   uv run pytest tests/ -v
   ```

2. **Commit your changes** with a clear commit message:
   ```bash
   git commit -m "Add feature: description of what you added"
   # or
   git commit -m "Fix: description of what you fixed"
   ```

3. **Push to your fork**:
   ```bash
   git push origin your-branch-name
   ```

4. **Create a Pull Request** on GitHub with:
   - A clear title describing the change
   - A detailed description of what was changed and why
   - References to any related issues
   - Screenshots or examples if applicable

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use type hints where appropriate
- Write clear, self-documenting code with meaningful variable names
- Add docstrings to public functions and classes

### Code Organization

- Keep functions focused and single-purpose
- Use appropriate abstractions and avoid code duplication
- Organize imports: standard library, third-party, local imports
- Maintain consistent file and directory structure

### Documentation

- Update docstrings for any modified functions or classes
- Update README.md if adding new features or changing behavior
- Include inline comments for complex logic
- Provide examples in docstrings where helpful

## Security Considerations

Since this library is focused on security, please pay special attention to:

1. **Information Disclosure**: Ensure no sensitive information is leaked in error messages, logs, or responses
2. **Input Validation**: Validate all inputs and handle edge cases securely
3. **Default Security**: Make secure behavior the default, with opt-in for less secure options
4. **Testing Security Features**: Write tests that verify security properties, not just functionality

### Security-Related Changes

For changes that affect security behavior:

1. **Explain the security implications** in your PR description
2. **Include tests** that verify the security properties
3. **Document any security trade-offs** or considerations
4. **Consider backward compatibility** and whether changes should be opt-in

## Issue Reporting

When reporting issues:

1. **Check existing issues** first to avoid duplicates
2. **Use a clear, descriptive title**
3. **Provide detailed steps to reproduce** the issue
4. **Include relevant code examples** or error messages
5. **Specify your environment** (Python version, FastAPI version, etc.)

## Feature Requests

When suggesting new features:

1. **Explain the use case** and why it would be valuable
2. **Consider security implications** of the proposed feature
3. **Suggest how it might be implemented** if you have ideas
4. **Be open to discussion** about alternative approaches

## Release Process

For maintainers creating releases:

1. **Ensure all tests pass** and the main branch is ready for release
2. **Use the Create Release workflow**:
   - Go to Actions → Create Release
   - Click "Run workflow"
   - Enter the version number (e.g., `1.0.0`)
   - Select release type (release or prerelease)
3. **The workflow will**:
   - Run tests to ensure everything works
   - Update the version in `pyproject.toml`
   - Build the package
   - Create a GitHub release with the built artifacts
4. **After release**, the Release workflow will automatically:
   - Build the package distributions
   - Upload them as artifacts to the release

### Manual Version Bump (Alternative)

You can also manually bump the version using uv:

```bash
uv version 1.0.0
```

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Start a discussion in the repository
- Reach out to the maintainers

Thank you for contributing to `fastapi-secure-errors`!
