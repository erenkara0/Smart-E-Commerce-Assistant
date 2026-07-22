"use client";

import { useEffect, useRef } from "react";

import type { ChatMessage } from "@/types/chat";

type ChatMessageListProps = {
  messages: ChatMessage[];
  isLoading: boolean;
};

export function ChatMessageList({
  messages,
  isLoading,
}: ChatMessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  return (
    <div className="flex w-full flex-col gap-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={
            message.role === "user"
              ? "ml-auto min-w-0 max-w-[85%] whitespace-pre-wrap break-words [overflow-wrap:anywhere] rounded-2xl rounded-br-md bg-[#2563EB] px-4 py-3 text-sm leading-6 text-white sm:max-w-[80%]"
              : "mr-auto min-w-0 max-w-[85%] whitespace-pre-wrap break-words [overflow-wrap:anywhere] rounded-2xl rounded-bl-md bg-slate-100 px-4 py-3 text-sm leading-6 text-slate-800 sm:max-w-[80%]"
          }
        >
          {message.content}
        </div>
      ))}

      {isLoading && (
        <div className="mr-auto max-w-[80%] rounded-2xl rounded-bl-md bg-slate-100 px-4 py-3 text-sm text-slate-500">
          Yanıt hazırlanıyor...
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}