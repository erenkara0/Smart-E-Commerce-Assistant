export default function Home() {
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
            <span className="h-2.5 w-2.5 rounded-full bg-green-500" />
            Sistem hazır
          </div>
        </div>
      </header>

      <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-5xl flex-col px-4 py-6 sm:px-6">
        <section className="flex flex-1 flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-1 items-center justify-center p-6">
            <div className="max-w-xl text-center">
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
                <button
                  type="button"
                  className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                >
                  Oyun için laptop önerir misin?
                </button>

                <button
                  type="button"
                  className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                >
                  Stokta bulunan ASUS modelleri neler?
                </button>

                <button
                  type="button"
                  className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                >
                  En yüksek puanlı ürün hangisi?
                </button>

                <button
                  type="button"
                  className="rounded-2xl border border-slate-200 p-4 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                >
                  Bütçeme uygun ürün önerir misin?
                </button>
              </div>
            </div>
          </div>

          <div className="border-t border-slate-200 bg-white p-4 sm:p-6">
            <form className="mx-auto flex max-w-3xl items-end gap-3">
              <label htmlFor="chat-message" className="sr-only">
                Mesajınız
              </label>

              <textarea
                id="chat-message"
                name="message"
                rows={1}
                placeholder="Ürünler hakkında bir soru sorun..."
                className="min-h-12 flex-1 resize-none rounded-2xl border border-slate-300 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-[#2563EB] focus:ring-4 focus:ring-blue-100"
              />

              <button
                type="button"
                className="h-12 rounded-2xl bg-[#2563EB] px-5 text-sm font-medium text-white transition hover:bg-[#1E40AF]"
              >
                Gönder
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