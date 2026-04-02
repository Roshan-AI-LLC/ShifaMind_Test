"use client"

import { useState } from "react"
import { Brain, MessageSquare, Menu, X } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { ChatMessage } from "@/components/chat/chat-message"
import { ChatInput } from "@/components/chat/chat-input"
import { ContextSidebar } from "@/components/chat/context-sidebar"

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

const mockMessages: Message[] = [
  {
    id: "1",
    content: "I've analyzed a clinical note for a 58-year-old male with elevated fasting glucose, family history of diabetes, and symptoms of polydipsia and polyuria. The top diagnosis is Type 2 Diabetes Mellitus with 96% confidence.",
    isUser: false,
    timestamp: "2:45 PM",
  },
  {
    id: "2",
    content: "What clinical findings support this diagnosis?",
    isUser: true,
    timestamp: "2:46 PM",
  },
  {
    id: "3",
    content: "Several key findings support the Type 2 Diabetes diagnosis:\n\n1. **Elevated Fasting Glucose** (confidence: 92%) - At 142 mg/dL, this exceeds the diagnostic threshold of 126 mg/dL\n\n2. **Increased Thirst (Polydipsia)** (confidence: 88%) - A classic symptom often accompanying hyperglycemia\n\n3. **Frequent Urination (Polyuria)** (confidence: 85%) - Occurs when glucose spills into urine\n\n4. **Family History** - Strong genetic predisposition to Type 2 DM\n\n5. **Age & BMI** - 58 years old with BMI 28 are typical risk factors\n\nThese findings collectively indicate impaired glucose metabolism characteristic of Type 2 Diabetes.",
    isUser: false,
    timestamp: "2:47 PM",
  },
]

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(mockMessages)
  const [isLoading, setIsLoading] = useState(false)
  const [showContext, setShowContext] = useState(true)
  const [showSidebar, setShowSidebar] = useState(false)

  const handleSendMessage = (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "That's an excellent question. Based on the clinical evidence and the analysis of this case, I would recommend considering additional laboratory workup including HbA1c for glycemic control assessment, lipid panel given the comorbidity findings, and potentially thyroid function tests given the metabolic presentation.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }),
      }
      setMessages((prev) => [...prev, aiMessage])
      setIsLoading(false)
    }, 1500)
  }

  const handleSuggestedQuestion = (question: string) => {
    handleSendMessage(question)
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-8rem)]">
      {/* Desktop Context Sidebar */}
      <div className="hidden sm:block">
        <ContextSidebar isOpen={showContext} />
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
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-gold/20 text-gold border border-gold/30">
              Demo
            </span>
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
                  onClick={() => handleSuggestedQuestion(question)}
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
            {isLoading && (
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
