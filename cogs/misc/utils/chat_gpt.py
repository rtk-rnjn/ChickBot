from __future__ import annotations

import config
import openai as ai

ai.api_key = config.OPENAI_TOKEN


def askgpt(user_text):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = ai.Completion.create(
        engine="text-davinci-003", temperature=0.777, prompt=user_text, max_tokens=1024
    )

    return completions["choices"][0]["text"]
