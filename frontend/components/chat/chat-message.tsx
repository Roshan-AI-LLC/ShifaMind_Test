"use client"

import type { Components } from "react-markdown"
import ReactMarkdown from "react-markdown"
import remarkBreaks from "remark-breaks"
import { Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

interface ChatMessageProps {
  content: string
  isUser: boolean
  timestamp: string
}

/** LLMs often glue `###` to the previous sentence without a newline — fix for proper heading blocks. */
function normalizeAssistantMarkdown(raw: string): string {
  let s = raw
  // `text:### Heading` or `text.### Heading` → break before heading
  s = s.replace(/([^\n#])(#{1,3}\s+[^\n]+)/g, (_, before: string, heading: string) => {
    if (/[#*`\[]/.test(before)) return `${before}${heading}`
    return `${before}\n\n${heading}`
  })
  // `**a**###` rare edge
  s = s.replace(/\*\*([^*]+)\*\*(#{1,3}\s)/g, "**$1**\n\n$2")
  return s.trim()
}

const mdComponents: Components = {
  h1: ({ className, ...props }) => (
    <h1
      className={cn(
        "text-base font-semibold text-foreground mt-4 mb-2 first:mt-0 pb-1 border-b border-white/[0.08]",
        className
      )}
      {...props}
    />
  ),
  h2: ({ className, ...props }) => (
    <h2 className={cn("text-sm font-semibold text-foreground mt-3.5 mb-2 first:mt-0", className)} {...props} />
  ),
  h3: ({ className, ...props }) => (
    <h3 className={cn("text-sm font-semibold text-primary mt-3 mb-1.5 first:mt-0", className)} {...props} />
  ),
  p: ({ className, ...props }) => (
    <p className={cn("mb-2.5 last:mb-0 text-sm leading-relaxed text-foreground/95", className)} {...props} />
  ),
  ul: ({ className, ...props }) => (
    <ul
      className={cn("list-disc pl-4 mb-2.5 space-y-1 text-sm text-foreground/95 marker:text-primary/80", className)}
      {...props}
    />
  ),
  ol: ({ className, ...props }) => (
    <ol
      className={cn("list-decimal pl-4 mb-2.5 space-y-1 text-sm text-foreground/95 marker:text-primary/80", className)}
      {...props}
    />
  ),
  li: ({ className, ...props }) => <li className={cn("leading-relaxed pl-0.5", className)} {...props} />,
  strong: ({ className, ...props }) => (
    <strong className={cn("font-semibold text-foreground", className)} {...props} />
  ),
  em: ({ className, ...props }) => <em className={cn("italic text-foreground-muted", className)} {...props} />,
  blockquote: ({ className, ...props }) => (
    <blockquote
      className={cn(
        "border-l-2 border-primary/50 pl-3 my-2 text-foreground-muted text-sm italic",
        className
      )}
      {...props}
    />
  ),
  hr: () => <hr className="my-4 border-white/[0.1]" />,
  a: ({ className, href, children, ...props }) => (
    <a
      href={href}
      className={cn("text-primary underline underline-offset-2 hover:text-primary/80", className)}
      target="_blank"
      rel="noopener noreferrer"
      {...props}
    >
      {children}
    </a>
  ),
  code: ({ className, children, ...props }) => {
    const isFenced = typeof className === "string" && /language-[\w-]+/.test(className)
    if (isFenced) {
      return (
        <code
          className={cn("block font-mono text-[0.8125rem] leading-relaxed text-foreground/95", className)}
          {...props}
        >
          {children}
        </code>
      )
    }
    return (
      <code
        className={cn(
          "px-1.5 py-0.5 rounded-md bg-white/[0.08] text-[0.8125rem] font-mono text-gold/90",
          className
        )}
        {...props}
      >
        {children}
      </code>
    )
  },
  pre: ({ className, children, ...props }) => (
    <pre
      className={cn(
        "my-2 p-3 rounded-lg bg-black/40 border border-white/[0.08] overflow-x-auto text-[0.8125rem] leading-relaxed",
        className
      )}
      {...props}
    >
      {children}
    </pre>
  ),
}

export function ChatMessage({ content, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 animate-fade-in ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
          <Sparkles className="w-4 h-4 text-primary" />
        </div>
      )}
      <div className={cn("flex flex-col min-w-0", isUser ? "items-end max-w-[85%]" : "items-start max-w-[min(100%,42rem)]")}>
        <div
          className={cn(
            "w-full px-4 py-3 rounded-xl",
            isUser
              ? "bg-primary text-primary-foreground rounded-br-none"
              : "bg-white/[0.06] text-foreground rounded-bl-none border border-white/[0.08]"
          )}
        >
          {isUser ? (
            <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">{content}</p>
          ) : (
            <div className="[&_p:first-child]:mt-0 [&_ul:last-child]:mb-0 [&_ol:last-child]:mb-0">
              <ReactMarkdown remarkPlugins={[remarkBreaks]} components={mdComponents}>
                {normalizeAssistantMarkdown(content)}
              </ReactMarkdown>
            </div>
          )}
        </div>
        <span className="text-xs text-foreground-subtle mt-1">{timestamp}</span>
      </div>
    </div>
  )
}
