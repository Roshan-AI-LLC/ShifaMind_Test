"use client"

import { useState, useRef, useEffect } from "react"
import { Brain, MessageSquare, Menu, X } from "lucide-react"
import { ChatMessage } from "@/components/chat/chat-message"
import { ChatInput } from "@/components/chat/chat-input"
import { ContextSidebar } from "@/components/chat/context-sidebar"
import { useAuth } from "@/hooks/use-auth"
import { streamChat } from "@/lib/api"

interface Message {
  id: string
  content: string
  isUser: boolean
  timestamp: string
}

const suggestedQuestions = [
  "What clinical findings support this diagnosis?",
  "Are there any differential diagnoses to consider?",
  "What additional tests would you recommend?",
]

function nowTime() {
  return new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })
}

export default function ChatPage() {
  const { session } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | undefined>()
  const [showSidebar, setShowSidebar] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!session?.access_token) return

    const userMsg: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: nowTime(),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    const aiId = (Date.now() + 1).toString()
    // Add a placeholder AI message that we'll stream into
    setMessages((prev) => [
      ...prev,
      { id: aiId, content: "", isUser: false, timestamp: nowTime() },
    ])

    try {
      let accumulated = ""
      for await (const event of streamChat(content, session.access_token, { sessionId })) {
        if (event.type === "token") {
          accumulated += event.content
          setMessages((prev) =>
            prev.map((m) => (m.id === aiId ? { ...m, content: accumulated } : m))
          )
        } else if (event.type === "done") {
          setSessionId(event.session_id)
        } else if (event.type === "error") {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === aiId ? { ...m, content: `Error: ${event.content}` } : m
            )
          )
        }
      }
    } catch (err: any) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === aiId
            ? { ...m, content: `Failed to reach AI service. ${err.message ?? ""}` }
            : m
        )
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-8rem)]">
      {/* Desktop Context Sidebar */}
      <div className="hidden sm:block">
        <ContextSidebar isOpen={true} />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/[0.08]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h1 className="font-medium text-foreground">Clinical Assistant</h1>
              <p className="text-sm text-foreground-muted">Discuss diagnoses and clinical findings</p>
            </div>
          </div>
          <button
            onClick={() => setShowSidebar(!showSidebar)}
            className="sm:hidden p-2 hover:bg-white/[0.08] rounded-lg transition-colors"
          >
            {showSidebar ? (
              <X className="w-5 h-5 text-foreground" />
            ) : (
              <Menu className="w-5 h-5 text-foreground" />
            )}
          </button>
        </div>

        {/* Messages Area */}
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center py-12">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/10 blur-3xl rounded-full" />
              <div className="relative w-20 h-20 rounded-2xl bg-white/[0.06] flex items-center justify-center">
                <Brain className="w-10 h-10 text-primary" />
              </div>
            </div>

            <h2 className="text-xl font-medium text-foreground mt-6">Start a Conversation</h2>
            <p className="text-foreground-muted text-sm mt-1 text-center max-w-md">
              Ask questions about diagnoses, clinical findings, or get recommendations based on your analysis.
            </p>

            <div className="flex flex-wrap justify-center gap-2 mt-6">
              {suggestedQuestions.map((question) => (
                <button
                  key={question}
                  onClick={() => handleSendMessage(question)}
                  className="px-4 py-2 rounded-full bg-white/[0.04] border border-white/[0.08] text-sm text-foreground-muted hover:text-foreground hover:bg-white/[0.08] transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto space-y-4 py-6 px-2">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                content={message.content}
                isUser={message.isUser}
                timestamp={message.timestamp}
              />
            ))}
            {isLoading && messages[messages.length - 1]?.content === "" && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center flex-shrink-0">
                  <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-white/[0.06] border border-white/[0.08]">
                  <span className="text-xs text-foreground-muted">Thinking</span>
                  <span className="text-xs text-primary animate-bounce">•</span>
                  <span className="text-xs text-primary animate-bounce delay-100">•</span>
                  <span className="text-xs text-primary animate-bounce delay-200">•</span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}

        {/* Input Area */}
        <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>

      {/* Mobile Context Sidebar */}
      {showSidebar && (
        <div className="sm:hidden absolute top-0 right-0 h-full w-80 border-l border-white/[0.08] z-50">
          <ContextSidebar onClose={() => setShowSidebar(false)} />
        </div>
      )}
    </div>
  )
}
