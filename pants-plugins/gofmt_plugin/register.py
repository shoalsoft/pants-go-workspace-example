from pants.backend.adhoc.code_quality_tool import CodeQualityToolRuleBuilder

def rules():
    # Configure `gofmt` as a formatter.
    fmt_cfg = CodeQualityToolRuleBuilder(
        goal="fmt",
        target="//pants-macros:gofmt_tool",
        name="gofmt",
        scope="gofmt_tool",
    )
    return fmt_cfg.rules()