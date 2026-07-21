"use client";

import { useState, type FormEvent } from "react";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type ChatApiResponse = {
  success: boolean;
  message: string;
  data: {
    session_id: string;
    answer: string;
  } | null;
};

const suggestedQuestions = [
  "Oyun için laptop önerir misin?",
  "Stokta bulunan ASUS modelleri neler?",
  "En yüksek puanlı ürün hangisi?",
  "Bütçeme uygun ürün önerir misin?",
];

export default function Home() {
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

      const chatData = responseBody.data;

      setSessionId(chatData.session_id);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: chatData.answer,
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

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(messageInput);
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#2563EB] text-lg font-bold text-white">
              M
            </div>

            <div>
              <p className="text-lg font-semibold">MikroAsistan</p>
              <p className="text-sm text-slate-500">
                Akıllı e-ticaret asistanı
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-slate-600">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                isLoading ? "bg-amber-500" : "bg-green-500"
              }`}
            />
            {isLoading ? "Yanıt hazırlanıyor" : "Sistem hazır"}
          </div>
        </div>
      </header>

      <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-5xl flex-col px-4 py-6 sm:px-6">
        <section className="flex flex-1 flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-1 overflow-y-auto p-6">
            {messages.length === 0 ? (
              <div className="m-auto max-w-xl text-center">
                <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50 text-2xl font-bold text-[#2563EB]">
                  M
                </div>

                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                  Size nasıl yardımcı olabilirim?
                </h1>

                <p className="mt-3 text-sm leading-6 text-slate-500 sm:text-base">
                  Ürün, fiyat, stok ve teknik özellikler hakkında mağaza
                  verilerine dayalı sorular sorabilirsiniz.
                </p>

                <div className="mt-8 grid gap-3 text-left sm:grid-cols-2">
                  {suggestedQuestions.map((question) => (
                    <button
                      key={question}
                      type="button"
                      onClick={() => void sendMessage(question)}
                      className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="flex w-full flex-col gap-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={
                      message.role === "user"
                        ? "ml-auto max-w-[80%] whitespace-pre-wrap rounded-2xl rounded-br-md bg-[#2563EB] px-4 py-3 text-sm leading-6 text-white"
                        : "mr-auto max-w-[80%] whitespace-pre-wrap rounded-2xl rounded-bl-md bg-slate-100 px-4 py-3 text-sm leading-6 text-slate-800"
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
              </div>
            )}
          </div>

          <div className="border-t border-slate-200 bg-white p-4 sm:p-6">
            <form
              onSubmit={handleSubmit}
              className="mx-auto flex max-w-3xl items-end gap-3"
            >
              <label htmlFor="chat-message" className="sr-only">
                Mesajınız
              </label>

              <textarea
                id="chat-message"
                name="message"
                rows={1}
                value={messageInput}
                onChange={(event) =>
                  setMessageInput(event.target.value)
                }
                disabled={isLoading}
                placeholder="Ürünler hakkında bir soru sorun..."
                className="min-h-12 flex-1 resize-none rounded-2xl border border-slate-300 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-[#2563EB] focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
              />

              <button
                type="submit"
                disabled={!messageInput.trim() || isLoading}
                className="h-12 rounded-2xl bg-[#2563EB] px-5 text-sm font-medium text-white transition hover:bg-[#1E40AF] disabled:cursor-not-allowed disabled:bg-slate-300"
              >
                {isLoading ? "Bekleyin" : "Gönder"}
              </button>
            </form>

            <p className="mt-3 text-center text-xs text-slate-400">
              Yanıtlar yalnızca mağaza veri setindeki bilgilere göre
              oluşturulur.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}