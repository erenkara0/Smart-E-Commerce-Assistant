"use client";

import { ChatHeader } from "@/components/chat/chat-header";
import { ChatInput } from "@/components/chat/chat-input";
import { ChatMessageList } from "@/components/chat/chat-message-list";
import { ChatWelcome } from "@/components/chat/chat-welcome";
import { useChat } from "@/hooks/use-chat";

const suggestedQuestions = [
  "Oyun için laptop önerir misin?",
  "Stokta bulunan ASUS modelleri neler?",
  "En yüksek puanlı ürün hangisi?",
  "Bütçeme uygun ürün önerir misin?",
];

export function ChatInterface() {
  const {
    messageInput,
    setMessageInput,
    messages,
    isLoading,
    sendMessage,
    resetChat,
  } = useChat();

  return (
    <div className="flex min-h-dvh flex-col overflow-x-hidden bg-slate-100 text-slate-900">
      <ChatHeader
        isLoading={isLoading}
        hasMessages={messages.length > 0}
        onNewChat={resetChat}
      />

      <main className="mx-auto flex min-h-0 w-full max-w-5xl flex-1 flex-col px-3 py-3 sm:px-6 sm:py-6">
        <section className="flex min-h-0 flex-1 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm sm:rounded-3xl">
          <div className="flex min-h-0 flex-1 overflow-y-auto p-4 sm:p-6">
            {messages.length === 0 ? (
              <ChatWelcome
                suggestedQuestions={suggestedQuestions}
                onQuestionSelect={(question) =>
                  void sendMessage(question)
                }
              />
            ) : (
              <ChatMessageList
                messages={messages}
                isLoading={isLoading}
              />
            )}
          </div>

          <ChatInput
            value={messageInput}
            isLoading={isLoading}
            onChange={setMessageInput}
            onSubmit={() => void sendMessage(messageInput)}
          />
        </section>
      </main>
    </div>
  );
}