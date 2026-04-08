import { useState, useCallback } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { ArrowLeft, Save, Sparkles, Eye, Edit } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { StatusBadge } from "@/components/status-badge"
import { useFetch } from "@/hooks/use-fetch"
import { chapters } from "@/services/api"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { toast } from "sonner"

export default function ChapterEditor() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: chapter, loading } = useFetch(() => chapters.get(id!), [id])
  const [content, setContent] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [mode, setMode] = useState<"edit" | "preview">("edit")

  const currentContent = content ?? chapter?.content ?? ""

  const handleSave = useCallback(async () => {
    if (!id || content === null) return
    setSaving(true)
    try {
      await chapters.updateContent(id, content)
      toast.success("保存成功")
    } catch (e: unknown) {
      toast.error("保存失败: " + (e as Error).message)
    } finally {
      setSaving(false)
    }
  }, [id, content])

  if (loading) return <div className="h-96 animate-pulse bg-muted rounded" />
  if (!chapter) return <div className="text-center py-12 text-muted-foreground">章节未找到</div>

  const meta = chapter.meta

  return (
    <div className="space-y-4 h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 shrink-0">
        <Button variant="ghost" size="icon" onClick={() => navigate("/chapters")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3">
            <span className="font-mono text-sm text-muted-foreground">{meta.id}</span>
            <h1 className="text-xl font-bold truncate">{meta.title || "未命名"}</h1>
            <StatusBadge status={meta.status} />
          </div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground mt-0.5">
            {meta.pov && <span>视角: {meta.pov}</span>}
            {meta.word_actual > 0 && <span>{meta.word_actual.toLocaleString()} 字</span>}
            {meta.goal && <span className="truncate">目标: {meta.goal}</span>}
          </div>
        </div>
        <div className="flex gap-2 shrink-0">
          <Button variant="outline" size="sm" onClick={() => setMode(mode === "edit" ? "preview" : "edit")}>
            {mode === "edit" ? <Eye className="mr-2 h-4 w-4" /> : <Edit className="mr-2 h-4 w-4" />}
            {mode === "edit" ? "预览" : "编辑"}
          </Button>
          <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
            <Sparkles className="mr-2 h-4 w-4" />
            AI 打磨
          </Button>
          <Button size="sm" onClick={handleSave} disabled={saving || content === null}>
            <Save className="mr-2 h-4 w-4" />
            {saving ? "保存中..." : "保存"}
          </Button>
        </div>
      </div>

      {/* Editor Area */}
      <div className="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-3 min-h-0">
          {mode === "edit" ? (
            <Textarea
              value={currentContent}
              onChange={(e) => setContent(e.target.value)}
              className="h-full w-full resize-none font-mono text-sm leading-relaxed"
              placeholder="开始写作..."
            />
          ) : (
            <ScrollArea className="h-full rounded-md border p-6">
              <article className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{currentContent}</ReactMarkdown>
              </article>
            </ScrollArea>
          )}
        </div>

        {/* Side Panel */}
        <div className="hidden lg:block min-h-0">
          <ScrollArea className="h-full">
            <div className="space-y-4">
              {meta.summary && (
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-xs">摘要</CardTitle></CardHeader>
                  <CardContent><p className="text-xs text-muted-foreground">{meta.summary}</p></CardContent>
                </Card>
              )}

              {meta.characters_involved?.length > 0 && (
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-xs">登场角色</CardTitle></CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-1">
                      {meta.characters_involved.map((c) => (
                        <Badge key={c} variant="outline" className="text-xs cursor-pointer" onClick={() => navigate(`/characters/${encodeURIComponent(c)}`)}>
                          {c}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {(meta.hooks_planted?.length > 0 || meta.hooks_revealed?.length > 0) && (
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-xs">伏笔</CardTitle></CardHeader>
                  <CardContent className="space-y-2">
                    {meta.hooks_planted?.map((h) => (
                      <div key={h} className="text-xs"><Badge variant="outline" className="text-[10px] mr-1">埋</Badge>{h}</div>
                    ))}
                    {meta.hooks_revealed?.map((h) => (
                      <div key={h} className="text-xs"><Badge className="text-[10px] mr-1">收</Badge>{h}</div>
                    ))}
                  </CardContent>
                </Card>
              )}

              <Card>
                <CardHeader className="pb-2"><CardTitle className="text-xs">字数</CardTitle></CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{currentContent.length.toLocaleString()}</div>
                  {meta.word_target > 0 && (
                    <div className="mt-1">
                      <div className="flex justify-between text-xs text-muted-foreground mb-1">
                        <span>目标 {meta.word_target.toLocaleString()}</span>
                        <span>{Math.round((currentContent.length / meta.word_target) * 100)}%</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-muted overflow-hidden">
                        <div className="h-full rounded-full bg-primary transition-all" style={{ width: `${Math.min(100, (currentContent.length / meta.word_target) * 100)}%` }} />
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </ScrollArea>
        </div>
      </div>
    </div>
  )
}
