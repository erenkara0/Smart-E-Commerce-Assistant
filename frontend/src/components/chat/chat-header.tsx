type ChatHeaderProps = {
    isLoading: boolean;
    hasMessages: boolean;
    onNewChat: () => void;
  };
  
  export function ChatHeader({
    isLoading,
    hasMessages,
    onNewChat,
  }: ChatHeaderProps) {
    return (
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
  
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onNewChat}
              disabled={!hasMessages || isLoading}
              className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-medium text-slate-600 transition hover:border-blue-300 hover:bg-blue-50 hover:text-[#2563EB] disabled:cursor-not-allowed disabled:opacity-40"
            >
              Yeni Sohbet
            </button>
  
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  isLoading ? "bg-amber-500" : "bg-green-500"
                }`}
              />
  
              {isLoading ? "Yanıt hazırlanıyor" : "Sistem hazır"}
            </div>
          </div>
        </div>
      </header>
    );
  }