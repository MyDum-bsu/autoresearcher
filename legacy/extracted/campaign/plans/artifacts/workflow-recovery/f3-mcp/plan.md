# F3 MCP resume investigation

Task aro-discovery-k4t; owner explicitly requested diagnosis and resolution of `Cannot resume aro-ogu-to-aro-formal-v3-support: Required tool is unavailable: mcp__searcharvester__search`.

Observed parent run `8d7a9e60-882c-4e89-8a58-429e7f62771f` is interrupted at statement review. Do not relaunch agents, edit snapshots/journals or discard saved progress. Read-only inspection found installed pi-extensible-workflows 6.3.0 snapshots every root-reachable tool (234 here), then requires the entire set on cold resume. This exceeds F3's local requirements. Pi MCP documentation states servers connect asynchronously; codemode discovery waits for them. A transient registration/readiness mismatch is the leading startup explanation, not a demonstrated permanent server outage.

Feedback: compare frozen tool names with the current catalog after supported MCP discovery; execute the missing search tool once with a harmless public query; exercise installed reachableTools and the exact missing-tool condition with pending versus ready inventories. No private data, credentials or MCP configuration contents in evidence.

Current server discovery and one actual search succeeded. Validate the full frozen set, record the evidence and explain supported recovery. Installed host-recovery only exposes interrupted-run resume through the interactive /workflow picker; workflow_resume is budget_exhausted-only. Do not misuse it, mutate run state or create a replacement mathematical run merely to avoid one UI operation.

No global code/package/config changes, mathematical-source edits or live scientific status. The startup race itself is not fixed in installed code by catalog discovery. A durable extension change would need a separately tested MCP-readiness wait or a narrower verified capability requirement, preserving genuine missing-tool rejection. Agent tools selectors alone do not narrow the root launch snapshot in 6.3.0.
