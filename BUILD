shoalsoft_go_tests()

experimental_workspace_environment(
    name="workspace",
)

shell_command(
    name="find_goroot",
    command='echo >go.env "GOENV=$(go env GOROOT)"',
    output_files=["go.env"],
    path_env_modify="off",
    extra_env_vars=[
        "PATH",
    ]
)