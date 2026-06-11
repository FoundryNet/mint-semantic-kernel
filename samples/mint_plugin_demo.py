# Copyright (c) FoundryNet.
"""Demo: give a Semantic Kernel agent MINT Protocol work attestation.

Run:
    export OPENAI_API_KEY=sk-...
    export MINT_API_KEY=fnet_...        # from https://mint.foundrynet.io
    python samples/mint_plugin_demo.py
"""

import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.contents.chat_history import ChatHistory

from mint_semantic_kernel import MintPlugin


async def main() -> None:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id="chat", ai_model_id="gpt-4o-mini"))
    kernel.add_plugin(MintPlugin(name="sk-demo-agent"), plugin_name="mint")

    settings = OpenAIChatPromptExecutionSettings(service_id="chat")
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    chat = kernel.get_service("chat")
    history = ChatHistory()
    history.add_user_message(
        "Attest that you completed a 'code_review' (summary: reviewed PR #1234), "
        "then show me my MINT trust profile."
    )

    result = await chat.get_chat_message_content(
        chat_history=history, settings=settings, kernel=kernel
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
