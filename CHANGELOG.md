# Winotify Changelog

All notable changes to this project will be documented in this file.

The format is based on [CHANGELOG.md][CHANGELOG.md]
and this project adheres to [Semantic Versioning][SemVer].

<!-- 
TEMPLATE

## [major.minor.patch] - yyyy-mm-dd

A message that notes the main changes in the update.

### Added

### Changed

### Deprecated

### Fixed

### Removed

### Security

_______________________________________________________________________________
 
-->

<!--
EXAMPLE

## [0.2.0] - 2021-06-02

Lorem Ipsum dolor sit amet.

### Added

- Cat pictures hidden in the library
- Added beeswax to the gears

### Changed

- Updated localisation files

-->

<!--
_______________________________________________________________________________

## [1.1.1] - 2022-09-21

Added GitHub Actions scripts for building executables automatically,
running unit and integration tests, and linting. Also cleaned up the
codebase a lot, without making breaking changes.

### Added

- CI/CD Executable builder
- CI/CD Unit test runner
- CI/CD Linter

### Changed

- Moved stuff from `__init__.py` and `__main__.py` to its own module
- Restructured the `audio` module and how its contents are used in the
  rest of the package

### Fixed

- Fixed some potential file lock-ups

-->

_______________________________________________________________________________

## [1.1.1] - 2022-09-21

Added GitHub Actions scripts for building executables automatically,
running unit and integration tests, and linting. Also cleaned up the
codebase a lot, without making breaking changes.

### Added

- CI/CD Executable builder
- CI/CD Unit test runner
- CI/CD Linter

### Changed

- Moved stuff from `__init__.py` and `__main__.py` to its own module
- Restructured the `audio` module and how its contents are used in the
  rest of the package

### Fixed

- Fixed some potential file lock-ups

_______________________________________________________________________________

## [1.1.0] - 2022-02-07

Minor fixes and new features.

### Added

- Added callback feature

### Changed

- Registry code now supports swapping the executable

_______________________________________________________________________________

## [1.0.4] - 2021-06-02

This is a bug fix release.

### Fixed

- Fixed main console window getting hidden after showing notification

_______________________________________________________________________________

## [1.0.3] - 2021-05-30

This is a bug fix release.

### Added

- Added `winotify-nc` command for no console output

### Fixed

- Fixed `subprocess` problem with `pyinstaller --noconsole`

_______________________________________________________________________________

## [1.0.2] - 2021-05-11

This is a bug fix release.

### Fixed

- Fixed non-English language encoding problem
- Fixed appearing PowerShell window in windowed mode (no console)

_______________________________________________________________________________

## [1.0.1] - 2021-05-02

This is a bug fix release.

### Added

- Added support for invalid characters in xml, such as `<` and `>`

### Fixed

- Fixed omitted `launch` parameter bug

_______________________________________________________________________________

## [1.0.0] - 2021-01-04

This is the initial release of the project.

### Added

- The base project

<!-- markdownlint-configure-file {
    "MD024": false
} -->
<!--
    MD024: No duplicate headings
-->

[CHANGELOG.md]: https://web.archive.org/web/20200714021150/https://changelog.md/
[SemVer]: http://semver.org/
