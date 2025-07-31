# GitHub Workflows

This directory contains the GitHub Actions workflows for the fastapi-secure-errors project.

## Workflows

### 1. Tests (`tests.yml`)
- **Trigger**: Push to main/develop branches, Pull requests
- **Purpose**: Run tests and generate coverage reports
- **Actions**: 
  - Install dependencies with uv
  - Run pytest with coverage
  - Upload coverage to Codecov

### 2. Release (`release.yml`)
- **Trigger**: When a GitHub release is published
- **Purpose**: Build and package the project for distribution
- **Actions**:
  - Run tests to ensure quality
  - Build the package using `uv build`
  - Upload package artifacts (wheel and source distribution)

### 3. Create Release (`create-release.yml`)
- **Trigger**: Manual workflow dispatch
- **Purpose**: Create a new release with version bumping
- **Inputs**:
  - `version`: The version number for the release (e.g., "1.0.0")
  - `release_type`: Either "release" or "prerelease"
- **Actions**:
  - Update version in pyproject.toml
  - Run tests
  - Build package
  - Commit version bump
  - Create GitHub release

## Usage

### Creating a Release

1. **Using the Create Release Workflow** (Recommended):
   - Go to the Actions tab in GitHub
   - Select "Create Release" workflow
   - Click "Run workflow"
   - Enter the version number and release type
   - Click "Run workflow"

2. **Manual Release**:
   - Create a new tag: `git tag v1.0.0`
   - Push the tag: `git push origin v1.0.0`
   - Create a release in GitHub UI using that tag

### Artifacts

The release workflow generates the following artifacts:
- **Source distribution** (`.tar.gz`): Contains the source code
- **Wheel distribution** (`.whl`): Ready-to-install binary package

These artifacts are automatically attached to the GitHub release and can be downloaded or used for PyPI publishing.

## Future Enhancements

- [ ] Add PyPI publishing to the release workflow
- [ ] Add security scanning with CodeQL
- [ ] Add dependency updates with Dependabot
- [ ] Add changelog generation
