# Macros to support building Go sources using the Go SDK run in a workspace environment.

# Declares that this directory contains a Go binary to be built. The binary will
# be copied under dist/ with the `dist_bin_name`.
def shoalsoft_go_binary(
    dist_bin_name: str = "bin",
    workspace_env_name: str = "__local_workspace__"
) -> None:
    if "/" in dist_bin_name:
        raise ValueError(f"The `dist_bin_name` field cannot contain the `/`  path separator.")

    # Define a target to run in the workspace and build the binary. If Pants supports `package_shell_command`, then
    # it is used for the binary's target. On older Pants versions, two targets are made instead: a `shell_command`
    # to build the binary and a `run_shell_command` target to trigger the build.
    if "package_shell_command" in globals():
        target_type = package_shell_command
        create_pkg_bin_target = False
    else:
        target_type = shell_command
        create_pkg_bin_target = True

    # Build the binary and copy the output to the "chroot" for capture.
    target_type(
        name="bin",
        command=f"source {{chroot}}/go.env && go build -o './{dist_bin_name}' && cp './{dist_bin_name}' '{{chroot}}/{dist_bin_name}'",
        execution_dependencies=[
            "//:find_goroot",
        ],
        output_files=[dist_bin_name],
        workdir=".",
        path_env_modify="off",
        extra_env_vars=[
            "PATH",
            "HOME",
        ],
        environment=workspace_env_name,
        log_output=True,
    )

    # Older versions of Pants do not have a way to trigger the shell backend in response to a `package` goal.
    # The work-around is for users to invoke the `run` goal with this `:pkg-bin` target to (indirectly) build
    # the binary and copy it to the dist directory using the provided `dist_bin_name`.
    if create_pkg_bin_target:
        run_shell_command(
            name="pkg-bin",
            command=f"mkdir -p ./dist && cp {{chroot}}/{dist_bin_name} ./dist/{dist_bin_name}",
            workdir="/",
            execution_dependencies=[":bin"],
        )


# Declares a top-level `go_tests` target to run all Go tests in a module.
def shoalsoft_go_tests(
    workspace_env_name: str = "__local_workspace__"
) -> None:
    test_shell_command(
        name="go_tests",
        command="source {chroot}/go.env && go test ./...",
        execution_dependencies=[
            "//:find_goroot",
        ],
        workdir=".",
        path_env_modify="off",
        extra_env_vars=[
            "PATH",
            "HOME",
        ],
        environment=workspace_env_name,
        log_output=True,
    )
