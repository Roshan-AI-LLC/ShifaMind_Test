"use client"

import { MessageCircle, Sparkles } from "lucide-react"

interface ChatMessageProps {
  content: string
  isUser: boolean
  timestamp: string
}

export function ChatMessage({ content, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 animate-fade-in ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-4 h-4 text-primary" />
        </div>
      )}
      <div className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`max-w-xs lg:max-w-md px-4 py-3 rounded-xl ${
            isUser
              ? "bg-primary text-primary-foreground rounded-br-none"
              : "bg-white/[0.06] text-foreground rounded-bl-none border border-white/[0.08]"
          }`}
        >
          <p className="text-sm leading-relaxed">{content}</p>
        </div>
        <span className="text-xs text-foreground-subtle mt-1">{timestamp}</span>
      </div>
    </div>
  )
}
