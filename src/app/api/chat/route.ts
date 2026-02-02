import { streamText, UIMessage, convertToModelMessages } from "ai";
import { google } from "@ai-sdk/google";
import { initialMessage } from "@/lib/data/system-prompt";

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json();

    const result = await streamText({
      model: google("gemini-2.5-flash"),
      messages: [
        initialMessage,
        ...convertToModelMessages(messages),
      ],
    });

    return result.toUIMessageStreamResponse();
  } catch (error) {
    return new Response("Failed to stream chat completion", { status: 500 });
  }
}