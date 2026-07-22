"use client";

import {
  useEffect,
  useRef,
  type FormEvent,
  type KeyboardEvent,
} from "react";

type ChatInputProps = {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

const MAX_TEXTAREA_HEIGHT = 160;

export function ChatInput({
  value,
  isLoading,
  onChange,
  onSubmit,
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    const textarea = textareaRef.current;

    if (!textarea) {
      return;
    }

    textarea.style.height = "auto";

    const nextHeight = Math.min(
      textarea.scrollHeight,
      MAX_TEXTAREA_HEIGHT,
    );

    textarea.style.height = `${nextHeight}px`;
    textarea.style.overflowY =
      textarea.scrollHeight > MAX_TEXTAREA_HEIGHT
        ? "auto"
        : "hidden";
  }, [value]);

  function submitMessage() {
    if (!value.trim() || isLoading) {
      return;
    }

    onSubmit();
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    submitMessage();
  }

  function handleKeyDown(
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) {
    const shouldSubmit =
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing;

    if (!shouldSubmit) {
      return;
    }

    event.preventDefault();
    submitMessage();
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
          ref={textareaRef}
          id="chat-message"
          name="message"
          rows={1}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          placeholder="Ürünler hakkında bir soru sorun..."
          className="min-h-12 flex-1 resize-none overflow-hidden rounded-2xl border border-slate-300 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-[#2563EB] focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
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
        Göndermek için Enter, yeni satır için Shift + Enter
      </p>
    </div>
  );
}