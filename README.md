# Pansbuild - Go in Workspace Example

## Overview

This repository is a extremely rudimentary example of how to build and test Go code with [Pantsbuild](https://pantsbuild.org) without usnig the Pants Go backend, but rather using the Go SDK directly. The goal is to provice a minimal integration between Pants and Go.

## Setup

1. Enable the shell and adhoc backends by ensuring that `[GLOBAL].backend_packages` in your `pants.toml` includes `pants.backend.shell` and `pants.backend.experimental.adhoc`.

2. Copy the `pants-macros/golang.py` Pants prelude file into your repository. Then set `[GLOBAL].build_file_prelude_globs` in your `pants.toml` to include that file. This exposes two macros to your code `shoalsoft_go_binary` and `shoalsoft_go_tests` (described below).

3. Configure a "workspace" environment by adding an `experimental_workspace_environment` target in the root `BUILD` file. Then set `[environments-preview.names]` in your `pants.toml` to include configure that environment by setting `workspace = "//:workspace"` in that section (assuming the target was itself called `workspace`).

4. Copy the `//:find_goroot` target from this repository into your repository's root BUILD file.

5. In each Go source directory which builds a binary, add a `shoalsoft_go_binary(...)` call to the Pants `BUILD` file in that diretory. Set the `dist_bin_name` on the macro call to be a unique name for the repository (which is used when writing the output under `dist/`).

6. In the BUILD file at the top of the repository, add a call to `shoalsoft_go_tests()`. This creates a `go_tests` target in that `BUILD` file which runs all tests in the Go module rooted at the top of the repository. Note: This does not yet support modules defined in subdirectories.

## Commands

Build a binary:
- On Pants v2.30.x and higher, run `pants package path/to/dir:bin`, then look in `dist/`.
- On prior Pants versions,instead run `pants run path/to/dir:pkg-bin`, then look in `dist/`.

Run tests: `pants test path/to/dir:go_tests`
