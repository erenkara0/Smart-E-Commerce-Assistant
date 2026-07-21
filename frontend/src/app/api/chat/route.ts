import { NextResponse } from "next/server";

import { API_BASE_URL } from "@/lib/api";

type ChatRequestBody = {
  message?: unknown;
  session_id?: unknown;
};

export async function POST(request: Request) {
  let body: ChatRequestBody;

  try {
    body = (await request.json()) as ChatRequestBody;
  } catch {
    return NextResponse.json(
      {
        success: false,
        message: "Geçersiz istek gövdesi.",
        data: null,
      },
      { status: 400 },
    );
  }

  const message =
    typeof body.message === "string" ? body.message.trim() : "";

  const sessionId =
    typeof body.session_id === "string"
      ? body.session_id.trim()
      : "";

  if (!message) {
    return NextResponse.json(
      {
        success: false,
        message: "Mesaj boş olamaz.",
        data: null,
      },
      { status: 400 },
    );
  }

  const backendPayload = {
    message,
    ...(sessionId ? { session_id: sessionId } : {}),
  };

  try {
    const backendResponse = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(backendPayload),
      cache: "no-store",
    });

    const responseBody = await backendResponse.json().catch(() => null);

    if (!backendResponse.ok) {
      return NextResponse.json(
        responseBody ?? {
          success: false,
          message: "Backend isteği tamamlanamadı.",
          data: null,
        },
        { status: backendResponse.status },
      );
    }

    return NextResponse.json(responseBody);
  } catch {
    return NextResponse.json(
      {
        success: false,
        message: "Backend servisine bağlanılamadı.",
        data: null,
      },
      { status: 502 },
    );
  }
}