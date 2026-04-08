import { useState, useRef, useEffect, useCallback } from "react"
import { Sparkles, Send, Loader2, BookOpen, Trash2, ChevronDown } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel,
} from "@/components/ui/dropdown-menu"
import { useFetch } from "@/hooks/use-fetch"
import { skills as skillsApi, llm } from "@/services/api"
import { useAppStore } from "@/stores/app-store"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import type { SkillMessage, SkillInfo } from "@/types"

const skillCategories: Record<string, string> = {
  chapter: "章节", character: "角色", plot: "大纲", worldbuilding: "世界观",
  timeline: "时间线", relationship: "关系", quality: "质量", compliance: "合规",
  pipeline: "流水线", project: "项目", material: "素材", style: "风格",
}

export default function SkillRunner() {
  const { llmConfig } = useAppStore()
  const { data: skillList } = useFetch(() => skillsApi.list())
  const [messages, setMessages] = useState<SkillMessage[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [streaming, setStreaming] = useState("")
  const [selectedSkill, setSelectedSkill] = useState<SkillInfo | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" })
  }, [messages, streaming])

  const handleSend = useCallback(async () => {
    if (!input.trim() && !selectedSkill) return

    const userMsg: SkillMessage = { role: "user", content: input.trim() }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput("")
    setLoading(true)
    setStreaming("")

    try {
      let response: Response

      if (selectedSkill) {
        response = await skillsApi.execute(selectedSkill.name, { query: input.trim() })
      } else {
        const apiMessages = newMessages.map((m) => ({ role: m.role, content: m.content }))
        response = await llm.chat(apiMessages)
      }

      if (!response.ok) {
        throw new Error(`${response.status}: ${await response.text()}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let fullContent = ""

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const chunk = decoder.decode(value, { stream: true })

          const lines = chunk.split("\n")
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6)
              if (data === "[DONE]") continue
              try {
                const parsed = JSON.parse(data)
                const delta = parsed.choices?.[0]?.delta?.content ?? parsed.content ?? ""
                fullContent += delta
                setStreaming(fullContent)
              } catch {
                fullContent += data
                setStreaming(fullContent)
              }
            }
          }
        }
      } else {
        const json = await response.json()
        fullContent = json.choices?.[0]?.message?.content ?? json.content ?? JSON.stringify(json)
      }

      setMessages([...newMessages, { role: "assistant", content: fullContent }])
      setStreaming("")
    } catch (e: unknown) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: `错误: ${(e as Error).message}\n\n请检查设置页面的 LLM 配置。` },
      ])
      setStreaming("")
    } finally {
      setLoading(false)
    }
  }, [input, messages, selectedSkill])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const grouped: Record<string, SkillInfo[]> = {}
  skillList?.forEach((s) => {
    const cat = s.category || "other"
    if (!grouped[cat]) grouped[cat] = []
    grouped[cat].push(s)
  })

  const configured = !!llmConfig.api_url && !!llmConfig.api_token

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4 shrink-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI 助手</h1>
          <p className="text-muted-foreground">
            {selectedSkill ? `当前: ${selectedSkill.name}` : "自由对话或选择技能"}
          </p>
        </div>
        <div className="flex gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <BookOpen className="mr-2 h-4 w-4" />
                选择技能
                <ChevronDown className="ml-2 h-3 w-3" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-72 max-h-96 overflow-y-auto" align="end">
              <DropdownMenuItem onClick={() => setSelectedSkill(null)}>
                <Sparkles className="mr-2 h-4 w-4" />
                自由对话
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              {Object.entries(grouped).map(([cat, skills]) => (
                <div key={cat}>
                  <DropdownMenuLabel className="text-xs">
                    {skillCategories[cat] || cat}
                  </DropdownMenuLabel>
                  {skills.map((s) => (
                    <DropdownMenuItem key={s.name} onClick={() => setSelectedSkill(s)}>
                      <div className="truncate">
                        <div className="font-medium text-sm">{s.name}</div>
                        <div className="text-xs text-muted-foreground truncate">{s.description}</div>
                      </div>
                    </DropdownMenuItem>
                  ))}
                </div>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
          {messages.length > 0 && (
            <Button variant="outline" size="sm" onClick={() => { setMessages([]); setStreaming("") }}>
              <Trash2 className="mr-2 h-4 w-4" />
              清空
            </Button>
          )}
        </div>
      </div>

      {!configured && (
        <Card className="mb-4 border-amber-500/50 bg-amber-500/5 shrink-0">
          <CardContent className="pt-4">
            <p className="text-sm text-amber-500">
              尚未配置 LLM。请前往 <a href="/settings" className="underline font-medium">设置页面</a> 配置 API URL 和 Token。
            </p>
          </CardContent>
        </Card>
      )}

      {/* Messages */}
      <ScrollArea className="flex-1 min-h-0 rounded-md border p-4" ref={scrollRef}>
        <div className="space-y-4">
          {messages.length === 0 && !streaming && (
            <div className="text-center py-16 text-muted-foreground">
              <Sparkles className="mx-auto h-12 w-12 mb-4 opacity-50" />
              <h3 className="text-lg font-semibold">开始对话</h3>
              <p className="text-sm mt-1">输入问题或选择一个技能开始</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-lg px-4 py-3 ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted"
              }`}>
                {msg.role === "assistant" ? (
                  <article className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                  </article>
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
          {streaming && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg px-4 py-3 bg-muted">
                <article className="prose prose-sm dark:prose-invert max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{streaming}</ReactMarkdown>
                </article>
              </div>
            </div>
          )}
          {loading && !streaming && (
            <div className="flex justify-start">
              <div className="rounded-lg px-4 py-3 bg-muted">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="mt-4 shrink-0">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={selectedSkill ? `向 ${selectedSkill.name} 发送指令...` : "输入消息... (Shift+Enter 换行)"}
            className="resize-none min-h-[44px] max-h-32"
            rows={1}
          />
          <Button onClick={handleSend} disabled={loading || (!input.trim() && !selectedSkill)} className="shrink-0">
            <Send className="h-4 w-4" />
          </Button>
        </div>
        {selectedSkill && (
          <div className="flex items-center gap-2 mt-2">
            <Badge variant="secondary">{selectedSkill.name}</Badge>
            <span className="text-xs text-muted-foreground">{selectedSkill.description}</span>
          </div>
        )}
      </div>
    </div>
  )
}
