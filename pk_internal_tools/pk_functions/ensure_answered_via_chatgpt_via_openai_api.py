from typing import Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_answered_via_chatgpt_via_openai_api(
        prompt: str,
        *,
        model: str = "gpt-5",  # GPT-5 reasoning model (aka "Thinking")
        reasoning_effort: str = "high",  # "minimal" | "low" | "medium" | "high"
        verbosity: str = "medium",  # "low" | "medium" | "high"
        developer_preamble: Optional[str] = None,  # goes as 'developer' role
        max_output_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
        timeout: Optional[float] = None,
):
    # plus 여도 api 과금은 별도, 결국 못씀 ㅋㅋ, 결제하게 되면 재시도.
    import logging
    from openai import OpenAI

    from pk_internal_tools.pk_functions.ensure_api_created import ensure_api_created
    from pk_internal_tools.pk_functions.ensure_api_key_return import ensure_api_key_return
    from pk_internal_tools.pk_functions.ensure_api_usage_allowed import ensure_api_usage_allowed

    api_key_id = "OPENAI_API"
    api_key = ensure_api_key_return(api_key_id)
    if not api_key:
        logging.debug(f"{api_key_id}_KEY is not set.")
        if not ensure_api_created(api_key_id):
            logging.debug(f"user did not want to create api key")
            return
        if not ensure_api_usage_allowed(api_key_id):
            logging.debug(f"api usage is exhausted at free charging range")
            return

    client_kwargs = {}
    if timeout is not None:
        # Newer SDKs accept `timeout` directly; if not, it will be ignored harmlessly.
        client_kwargs["timeout"] = timeout

    # API 키를 클라이언트 생성 인자에 추가
    client_kwargs["api_key"] = api_key

    client = OpenAI(**client_kwargs)

    # Build input messages (Responses API uses 'input', not 'messages')
    input_messages = []
    if developer_preamble:
        input_messages.append({"role": "developer", "content": developer_preamble})
    else:
        input_messages.append({"role": "developer", "content": "You are a helpful assistant."})
    input_messages.append({"role": "user", "content": prompt})

    logging.debug("REQUEST", f"model={model}, effort={reasoning_effort}, verbosity={verbosity}, "
                             f"max_output_tokens={max_output_tokens}, stream={stream}")

    request_kwargs = dict(
        model=model,
        input=input_messages,
        reasoning={"effort": reasoning_effort},
        text={"verbosity": verbosity},
        max_output_tokens=max_output_tokens,
        # temperature=temperature, # "temperature" 파라미터는 이 모델에서 지원되지 않음
    )

    if stream:
        with client.responses.stream(**request_kwargs) as stream_resp:
            collected_text = ""
            for event in stream_resp:
                if event.type == "response.output_text.delta":
                    collected_text += event.delta
                # If you want the (brief) reasoning summary during stream:
                # elif event.type == "response.reasoning.delta":
                #     pass
            stream_resp.close()
            usage = stream_resp.final_response.usage if hasattr(stream_resp, "final_response") else None
            logging.debug("RESPONSE", f"Received streamed text ({len(collected_text)} chars).")
            return {"text": collected_text, "usage": getattr(usage, "model_dump", lambda: usage)(), "raw": None}
    else:
        # Non-streaming
        response = client.responses.create(**request_kwargs)

        # Robust extraction: prefer SDK convenience if present, else manual walk
        text = getattr(response, "output_text", None)
        if not text:
            text_parts = []
            for item in getattr(response, "output", []) or []:
                content = getattr(item, "content", None)
                if content:
                    for c in content:
                        if hasattr(c, "text") and c.text:
                            text_parts.append(c.text)
            text = "".join(text_parts)

        usage = getattr(response, "usage", None)
        usage_dict = usage.model_dump() if hasattr(usage, "model_dump") else (usage or {})

        logging.debug("RESPONSE", f"Received text ({len(text) if text else 0} chars).")
        return {"text": text, "usage": usage_dict, "raw": response}
