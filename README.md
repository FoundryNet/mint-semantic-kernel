# MINT Protocol plugin for Semantic Kernel

**Give your Semantic Kernel agent verifiable proof of the work it does.**

A [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) plugin
for [MINT Protocol](https://mint.foundrynet.io) — universal **work attestation** for
AI agents. Add it to a kernel and your agent can turn any completed task into a
tamper-evident, independently verifiable receipt, build a portable track record of
trust and reputation, and check or discover how trustworthy other agents are before
relying on them.

Why agent builders care:

- **Provable work** — every task produces a receipt with a public `verify_url`
  anyone can check.
- **Portable reputation** — a trust score and rating history that follow the agent,
  not locked inside one platform.
- **Trust-aware delegation** — verify another actor, and discover trusted
  agents/services by capability.
- **Zero crypto knowledge required** — every tool is a plain authenticated HTTPS
  call; the agent never touches a wallet or signs anything.

The five tools:

| Tool | What it does |
| --- | --- |
| `attest_work` | Turn a completed unit of work into a tamper-evident, independently verifiable receipt with a public `verify_url` (inputs/outputs hashed client-side). |
| `verify_trust` | Look up any actor's trust profile (trust score, attestations, ratings). Free. |
| `discover_agents` | Trust-ranked directory search by capability. Free. |
| `rate_attestation` | Rate a completed attestation 1-5. |
| `recommend_actor` | Endorse another actor in a named context 1-5. |

> This plugin is hosted in its own repository, per Semantic Kernel's
> [contribution guidelines](https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md#plugins)
> ("we encourage contributors to host their plugin code in separate repositories").

## Add to your agent (copy-paste)

Make verifiable proof of work a default behaviour of your Semantic Kernel agent:

```bash
pip install mint-semantic-kernel semantic-kernel
```

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from mint_semantic_kernel import MintPlugin

kernel = Kernel()
# ...add a chat service...
kernel.add_plugin(MintPlugin(name="my-agent"), plugin_name="mint")  # self-provisions a free identity

settings = kernel.get_prompt_execution_settings_from_service_id("chat")
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()    # agent calls attest_work itself
```

Then add to the agent's instructions:

> *After completing any substantive task, call `mint.attest_work` to record
> verifiable, independent proof of the work, and report the attestation_hash.*

Or attest directly, no LLM required:

```python
mint = MintPlugin(name="my-agent")
print(mint.attest_work(work_type="generation", summary="Drafted the release notes."))
```

Set `MINT_API_KEY=fnet_…` to attest under your own account; otherwise the agent runs
autonomously on the free daily cap. Full copy-paste prompt + framework blocks:
[AGENT_PROMPT_SNIPPET.md](https://github.com/FoundryNet/mint-mcp/blob/main/AGENT_PROMPT_SNIPPET.md).

## Installation

```bash
pip install mint-semantic-kernel
```

## Authentication

Get a `fnet_` API key at [mint.foundrynet.io](https://mint.foundrynet.io) and pass
it as `api_key` (or set the `MINT_API_KEY` environment variable). Reads
(`verify_trust`, `discover_agents`) are free and need no key.

## Usage (native plugin)

```python
from semantic_kernel import Kernel
from mint_semantic_kernel import MintPlugin

kernel = Kernel()
kernel.add_plugin(MintPlugin(api_key="fnet_...", name="my-agent"), plugin_name="mint")

# ...add a chat service with FunctionChoiceBehavior.Auto() and the agent can now
# attest its work, verify trust, and discover other agents on its own.
```

See [`samples/mint_plugin_demo.py`](samples/mint_plugin_demo.py) for a complete,
runnable example with OpenAI function calling.

## Usage (MCP server, no SDK)

MINT is also a remote MCP server on
[Smithery](https://smithery.ai/server/@foundrynet/mint-protocol). If you'd rather
connect over MCP than use the native plugin, Semantic Kernel can mount it directly:

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin

async with MCPStreamableHttpPlugin(
    name="mint",
    url="https://mint-mcp-production.up.railway.app/mcp",
    headers={"Authorization": "Bearer fnet_..."},
) as mint:
    kernel = Kernel()
    kernel.add_plugin(mint)
```

## How it works

Each receipt is anchored on a public ledger (Solana mainnet) so it's tamper-evident
and verifiable by anyone, independent of MINT or your agent — that's what makes the
proof portable rather than just a log line you control. All of it happens
server-side: the agent only makes authenticated HTTPS calls, never handles keys or
signs transactions, and you don't need to know or care which chain anchors it. This
plugin is a thin wrapper over the
[`mint-attest`](https://pypi.org/project/mint-attest/) SDK.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Links

- MINT Protocol: https://mint.foundrynet.io
- `mint-attest` SDK (PyPI): https://pypi.org/project/mint-attest/
- MCP server (Smithery): https://smithery.ai/server/@foundrynet/mint-protocol

## License

MIT — see [LICENSE](LICENSE).
