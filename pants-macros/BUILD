shell_command(
    name="gofmt",
    command='source {chroot}/go.env && "$GOROOT/bin/gofmt" -l -w "$@"',
    workdir="/",
    execution_dependencies=[
        "//:find_goroot",
    ],
)

code_quality_tool(
    name="gofmt_tool",
    runnable=":gofmt",
    file_glob_include=["**/*.go"],
    args=[],
)