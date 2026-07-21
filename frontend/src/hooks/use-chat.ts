"use client";

import { useState } from "react";

import type {
  ChatApiResponse,
  ChatMessage,
} from "@/types/chat";

export function useChat() {
  const [messageInput, setMessageInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage(content: string) {
    const cleanedMessage = content.trim();

    if (!cleanedMessage || isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanedMessage,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setMessageInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: cleanedMessage,
          ...(sessionId ? { session_id: sessionId } : {}),
        }),
      });

      const responseBody =
        (await response.json()) as ChatApiResponse;

      if (
        !response.ok ||
        !responseBody.success ||
        !responseBody.data
      ) {
        throw new Error(
          responseBody.message || "Asistan yanıtı alınamadı.",
        );
      }

      const responseData = responseBody.data;

      setSessionId(responseData.session_id);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: responseData.answer,
        },
      ]);
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Beklenmeyen bir hata oluştu.";

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `Üzgünüm, yanıt oluşturulamadı. ${errorMessage}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function resetChat() {
    if (isLoading) {
      return;
    }

    setMessages([]);
    setSessionId(null);
    setMessageInput("");
  }

  return {
    messageInput,
    setMessageInput,
    messages,
    isLoading,
    sendMessage,
    resetChat,
  };
}