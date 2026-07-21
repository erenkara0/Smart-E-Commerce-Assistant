type ChatWelcomeProps = {
    suggestedQuestions: string[];
    onQuestionSelect: (question: string) => void;
  };
  
  export function ChatWelcome({
    suggestedQuestions,
    onQuestionSelect,
  }: ChatWelcomeProps) {
    return (
      <div className="m-auto max-w-xl text-center">
        <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50 text-2xl font-bold text-[#2563EB]">
          M
        </div>
  
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Size nasıl yardımcı olabilirim?
        </h1>
  
        <p className="mt-3 text-sm leading-6 text-slate-500 sm:text-base">
          Ürün, fiyat, stok ve teknik özellikler hakkında mağaza verilerine
          dayalı sorular sorabilirsiniz.
        </p>
  
        <div className="mt-8 grid gap-3 text-left sm:grid-cols-2">
          {suggestedQuestions.map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => onQuestionSelect(question)}
              className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    );
  }