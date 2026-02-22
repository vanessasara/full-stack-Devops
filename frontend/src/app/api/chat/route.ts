import { streamText } from "ai";

const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || "http://localhost:8000";

// Don't cache the response - always get fresh data
export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Handle different message formats from AI SDK useChat
    let userMessage = "";
    let sessionId: string | null = null;
    let pageContext: string | null = null;
    let selectedText: string | null = null;

    // Format 1: useChat with messages array - check the last message
    if (body.messages && Array.isArray(body.messages) && body.messages.length > 0) {
      const lastMessage = body.messages[body.messages.length - 1];

      // Check if content is a string
      if (typeof lastMessage.content === "string") {
        userMessage = lastMessage.content;
      }
      // Check if content is an object with parts
      else if (lastMessage.content && typeof lastMessage.content === "object") {
        if (lastMessage.content.parts && Array.isArray(lastMessage.content.parts)) {
          userMessage = lastMessage.content.parts.map((p: any) => p.text || "").join("");
        } else if (lastMessage.content.text) {
          userMessage = lastMessage.content.text;
        }
      }
    }

    // Format 2: Direct sendMessage from ChatWidget with { text, sessionId, context }
    if (!userMessage && body.text) {
      userMessage = body.text;
    }

    // Extract context - these may come from different places depending on the request
    sessionId = body.sessionId || body.id || null;
    pageContext = body.context?.page_context || null;
    selectedText = body.context?.selected_text || null;

    // Also check headers for page context (useful for initial context)
    const headerPageContext = req.headers.get("X-Page-Context");
    if (headerPageContext && !pageContext) {
      pageContext = headerPageContext;
    }

    if (!userMessage || userMessage.trim() === "") {
      return new Response(JSON.stringify({
        error: "No message provided",
        receivedBody: Object.keys(body)
      }), { status: 400 });
    }

    // Build headers for backend request
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    
    // Add page context to headers if available
    if (pageContext) {
      headers["X-Page-Context"] = pageContext;
    }

    // Call Python backend (non-streaming)
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/chat`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        message: userMessage,
        session_id: sessionId,
        page_context: pageContext,
        selected_text: selectedText,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    // Use streamText to properly format the response for useChat
    // This uses AI SDK's data stream format which useChat expects
    return streamText({
      text: data.response,
    }).toDataStreamResponse();

  } catch (error) {
    console.error("Chat API error:", error);
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : "Failed to process chat",
      }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
