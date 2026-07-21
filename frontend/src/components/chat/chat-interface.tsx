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
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <ChatHeader
        isLoading={isLoading}
        hasMessages={messages.length > 0}
        onNewChat={resetChat}
      />

      <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-5xl flex-col px-4 py-6 sm:px-6">
        <section className="flex flex-1 flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-1 overflow-y-auto p-6">
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