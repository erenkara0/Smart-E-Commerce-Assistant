export type ChatMessage = {
    id: string;
    role: "user" | "assistant";
    content: string;
  };
  
  export type ChatResponseData = {
    session_id: string;
    answer: string;
  };
  
  export type ChatApiResponse = {
    success: boolean;
    message: string;
    data: ChatResponseData | null;
  };