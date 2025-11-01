shell_command(
    name="find_goroot",
    command='mkdir -p {chroot}/pants-macros && echo "export GOROOT=$(go env GOROOT)" >{chroot}/pants-macros/go.env',
    output_files=["go.env"],
    root_output_directory=".",
    outputs_match_mode="all",
    path_env_modify="off",
    extra_env_vars=[
        "PATH",
    ]
)

shell_command(
    name="gofmt",
    command='source {chroot}/go.env && "$GOROOT/bin/gofmt" -l -w "$@"',
    workdir="/",
    execution_dependencies=[
        "//pants-macros:find_goroot",
    ],
)

code_quality_tool(
    name="gofmt_tool",
    runnable=":gofmt",
    file_glob_include=["**/*.go"],
    args=[],
)