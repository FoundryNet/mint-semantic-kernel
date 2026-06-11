import json

from semantic_kernel import Kernel

from mint_semantic_kernel import MintPlugin


def test_construct_carries_key():
    plugin = MintPlugin(api_key="fnet_test_key", name="test-agent")
    assert plugin._client.api_key == "fnet_test_key"


def test_methods_are_kernel_functions():
    for fn in ["attest_work", "verify_trust", "discover_agents", "rate_attestation", "recommend_actor"]:
        method = getattr(MintPlugin, fn)
        assert getattr(method, "__kernel_function__", False) is True


def test_registers_on_kernel():
    kernel = Kernel()
    kernel.add_plugin(MintPlugin(api_key="fnet_test_key"), plugin_name="mint")
    plugin = kernel.plugins["mint"]
    assert "attest_work" in plugin.functions
    assert "verify_trust" in plugin.functions
    assert "discover_agents" in plugin.functions


def test_discover_returns_json(monkeypatch):
    plugin = MintPlugin(api_key="fnet_test_key")
    monkeypatch.setattr(plugin._client, "discover", lambda **kw: [])
    assert json.loads(plugin.discover_agents(capability="rag")) == []
