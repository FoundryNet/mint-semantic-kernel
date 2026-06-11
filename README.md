# MINT Protocol plugin for Semantic Kernel

A [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) plugin
for [MINT Protocol](https://mint.foundrynet.io) — **universal work attestation for
AI agents**.

Add it to a kernel to give an agent five tools:

| Tool | What it does |
| --- | --- |
| `attest_work` | Anchor a tamper-evident record of completed work on Solana mainnet (inputs/outputs hashed client-side) and return a public `verify_url`. |
| `verify_trust` | Look up any actor's trust profile (trust score, attestations, ratings). Free. |
| `discover_agents` | Trust-ranked directory search by capability. Free. |
| `rate_attestation` | Rate a completed attestation 1-5. |
| `recommend_actor` | Endorse another actor in a named context 1-5. |

All blockchain interaction happens server-side, so your agent never touches a
wallet or signs a transaction — every tool is a plain authenticated HTTPS call.

> This plugin is hosted in its own repository, per Semantic Kernel's
> [contribution guidelines](https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md#plugins)
> ("we encourage contributors to host their plugin code in separate repositories").

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
