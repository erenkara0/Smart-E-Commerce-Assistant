"use client";

import type { FormEvent } from "react";

type ChatInputProps = {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

export function ChatInput({
  value,
  isLoading,
  onChange,
  onSubmit,
}: ChatInputProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
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
          value={value}
          onChange={(event) => onChange(event.target.value)}
          disabled={isLoading}
          placeholder="Ürünler hakkında bir soru sorun..."
          className="min-h-12 flex-1 resize-none rounded-2xl border border-slate-300 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-[#2563EB] focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
        />

        <button
          type="submit"
          disabled={!value.trim() || isLoading}
          className="h-12 rounded-2xl bg-[#2563EB] px-5 text-sm font-medium text-white transition hover:bg-[#1E40AF] disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isLoading ? "Bekleyin" : "Gönder"}
        </button>
      </form>

      <p className="mt-3 text-center text-xs text-slate-400">
        Yanıtlar yalnızca mağaza veri setindeki bilgilere göre oluşturulur.
      </p>
    </div>
  );
}