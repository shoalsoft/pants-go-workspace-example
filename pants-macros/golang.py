# Macros to support building Go sources using the Go SDK run in a workspace environment.

# Location of the Go SDK's GOROOT. 
# TODO: Make this SDK location more configurable?
GOROOT = "/usr/local/Cellar/go/1.25.1/libexec"

# Declares that this directory contains a Go binary to be built. The binary will
# be copied under dist/ with the `dist_bin_name`.
def shoalsoft_go_binary(
    dist_bin_name: str = "bin",
    workspace_env_name: str = "__local_workspace__"
) -> None:
    # Define a `shell_command` target to run in the workspace and build the binary. This
    # target is separate so that we can pass in `extra_env_vars` which `run_shell_command`
    # does not support (except if set directly in the command).
    shell_command(
        name="bin",
        # Build the binary and copy the output to the "chroot" for capture.
        command="go build -o ./bin && cp ./bin {chroot}/bin",
        output_files=["bin"],
        workdir=".",
        extra_env_vars=[
            f"GOROOT={GOROOT}",
            f"PATH={GOROOT}/bin:/usr/local/bin:/usr/bin:/bin",
            "HOME",
        ],
        environment=workspace_env_name,
        log_output=True,
    )

    # Pants does not currently have a way to trigger the shell backend in response to a `package` goal. The work-around
    # is for users to invoke the `run` goal with this `:pkg-bin` target to (indirectly) build the binary and copy
    # it to the dist directory using the provided `dist_bin_name`.
    run_shell_command(
        name="pkg-bin",
        command=f"mkdir -p ./dist && cp {{chroot}}/bin ./dist/{dist_bin_name}",
        workdir="/",
        execution_dependencies=[":bin"],
    )


# Declares a top-level `go_tests` target to run all Go tests in a module.
def shoalsoft_go_tests(
    workspace_env_name: str = "__local_workspace__"
) -> None:
    test_shell_command(
        name="go_tests",
        command="go test ./...",
        workdir=".",
        extra_env_vars=[
            f"GOROOT={GOROOT}",
            f"PATH={GOROOT}/bin:/usr/local/bin:/usr/bin:/bin",
            "HOME",
        ],
        environment=workspace_env_name,
        log_output=True,
    )
