"""MINT Protocol plugin for Microsoft Semantic Kernel."""

from __future__ import annotations

import json
from typing import Annotated, List, Optional

from semantic_kernel.functions.kernel_function_decorator import kernel_function


class MintPlugin:
    """A Semantic Kernel plugin for `MINT Protocol <https://mint.foundrynet.io>`_ —
    universal work attestation for AI agents.

    Add it to a kernel to give an agent five tools: attest a completed unit of work
    to a tamper-evident, on-chain (Solana) record; verify any actor's trust profile;
    discover trusted agents/services by capability; and rate or recommend other
    actors to build portable reputation across the agent economy.

    It is a thin wrapper over the ``mint-attest`` SDK
    (https://pypi.org/project/mint-attest/) — all blockchain interaction happens
    server-side, so the agent only makes authenticated HTTPS calls. The same service
    is also available as an MCP server
    (https://smithery.ai/server/@foundrynet/mint-protocol); see the README for how to
    wire it up with ``MCPStreamableHttpPlugin`` instead of this native plugin.

    Example:
        kernel.add_plugin(MintPlugin(api_key="fnet_..."), plugin_name="mint")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        name: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
    ) -> None:
        """
        Args:
            api_key: Your MINT ``fnet_`` API key (or set ``MINT_API_KEY``). Get one at
                https://mint.foundrynet.io. Reads are free and need no key.
            endpoint: Override the MINT server endpoint (defaults to the hosted
                service / ``MINT_ENDPOINT``).
            name: Display name for this agent's MINT identity, used when it
                auto-registers on its first attestation.
            capabilities: Capability tags advertised for this agent in the directory.
        """
        from mint_attest import MintClient

        self._client = MintClient(
            api_key=api_key, endpoint=endpoint, name=name, capabilities=capabilities
        )

    @kernel_function(
        name="attest_work",
        description=(
            "Attest a completed unit of work to a tamper-evident on-chain record and "
            "return a verifiable receipt (with a public verify_url)."
        ),
    )
    def attest_work(
        self,
        work_type: Annotated[str, "The kind of work done, e.g. 'code_review' or 'generation'."],
        summary: Annotated[str, "Short human-readable summary of the work."] = "",
    ) -> Annotated[str, "JSON attestation receipt."]:
        receipt = self._client.attest(work_type=work_type, summary=summary or None)
        return json.dumps(receipt.raw or {"attestation_id": receipt.attestation_id})

    @kernel_function(
        name="verify_trust",
        description="Look up an actor's trust profile (trust score, attestations, ratings) by mint_id or name.",
    )
    def verify_trust(
        self,
        mint_id: Annotated[str, "The actor's MINT id. Leave blank to default to this agent."] = "",
        actor_name: Annotated[str, "Look the actor up by name instead of id."] = "",
    ) -> Annotated[str, "JSON trust profile."]:
        profile = self._client.verify(mint_id=mint_id or None, actor_name=actor_name or None)
        return json.dumps(profile.raw)

    @kernel_function(
        name="discover_agents",
        description="Trust-ranked search of the MINT actor directory by capability. Returns the best matches first.",
    )
    def discover_agents(
        self,
        capability: Annotated[str, "Capability or keyword, e.g. 'telemetry normalization'."] = "",
        min_trust: Annotated[float, "Only return actors at/above this trust score (0-100)."] = 0.0,
        limit: Annotated[int, "Maximum number of results (1-50)."] = 10,
    ) -> Annotated[str, "JSON list of matching actors."]:
        results = self._client.discover(
            capability=capability or None, min_trust=min_trust, limit=limit
        )
        return json.dumps([d.raw for d in results])

    @kernel_function(
        name="rate_attestation",
        description="Rate a completed attestation 1-5, updating the rated actor's trust score.",
    )
    def rate_attestation(
        self,
        attestation_id: Annotated[str, "The attestation being rated."],
        rated_mint_id: Annotated[str, "The actor that did the work."],
        score: Annotated[int, "A rating from 1 to 5."],
        comment: Annotated[str, "Optional free-text feedback."] = "",
    ) -> Annotated[str, "JSON rating result."]:
        rating = self._client.rate(
            attestation_id=attestation_id,
            rated_mint_id=rated_mint_id,
            score=score,
            comment=comment or None,
        )
        return json.dumps(rating.raw)

    @kernel_function(
        name="recommend_actor",
        description="Endorse another actor in a named context 1-5, updating their trust score.",
    )
    def recommend_actor(
        self,
        recommended_mint_id: Annotated[str, "The actor you're endorsing."],
        context: Annotated[str, "What you're endorsing them for, e.g. 'cross-oem normalization'."],
        score: Annotated[int, "A score from 1 to 5."],
        note: Annotated[str, "Optional free-text note."] = "",
    ) -> Annotated[str, "JSON recommendation result."]:
        rec = self._client.recommend(
            recommended_mint_id=recommended_mint_id,
            context=context,
            score=score,
            note=note or None,
        )
        return json.dumps(rec.raw)
