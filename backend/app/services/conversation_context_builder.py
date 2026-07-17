def build_conversation_history(
    messages: list[dict[str, str | int]],
) -> str:
    if not messages:
        return ""

    history_parts: list[str] = []

    for message in messages:
        role = str(message["role"])
        content = str(message["content"])

        role_label = "Kullanıcı" if role == "user" else "Asistan"
        history_parts.append(f"{role_label}: {content}")

    return "\n".join(history_parts)


def build_retrieval_query(
    current_message: str,
    messages: list[dict[str, str | int]],
) -> str:
    previous_user_messages = [
        str(message["content"])
        for message in messages
        if message["role"] == "user"
    ]

    query_parts = [
        *previous_user_messages,
        current_message.strip(),
    ]

    return " ".join(query_parts)