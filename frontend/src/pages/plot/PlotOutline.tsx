import { useState } from "react"
import { Edit, Eye, Sparkles, TrendingUp, BookOpen } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { useFetch } from "@/hooks/use-fetch"
import { plot } from "@/services/api"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as ReTooltip,
} from "recharts"

export default function PlotOutline() {
  const navigate = useNavigate()
  const { data: outline, loading } = useFetch(() => plot.outline())
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState("")

  const handleEdit = () => {
    setDraft(outline?.markdown ?? "")
    setEditing(true)
  }

  const handleSave = async () => {
    try {
      await plot.updateOutline(draft)
      setEditing(false)
      toast.success("大纲已保存")
    } catch (e: unknown) {
      toast.error("保存失败: " + (e as Error).message)
    }
  }

  const structured = outline?.structured
  const pacingData = structured?.pacing_curve?.map((p) => ({
    chapter: p.chapter,
    tension: p.tension,
    note: p.note,
  })) ?? []

  if (loading) return <div className="h-96 animate-pulse bg-muted rounded" />

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">大纲</h1>
          <p className="text-muted-foreground">
            {structured?.premise || "故事大纲与结构"}
          </p>
        </div>
        <div className="flex gap-2">
          {editing ? (
            <>
              <Button variant="outline" size="sm" onClick={() => setEditing(false)}>取消</Button>
              <Button size="sm" onClick={handleSave}>保存</Button>
            </>
          ) : (
            <>
              <Button variant="outline" size="sm" onClick={handleEdit}>
                <Edit className="mr-2 h-4 w-4" />编辑
              </Button>
              <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
                <Sparkles className="mr-2 h-4 w-4" />AI 优化
              </Button>
            </>
          )}
        </div>
      </div>

      <Tabs defaultValue="outline">
        <TabsList>
          <TabsTrigger value="outline"><BookOpen className="mr-1 h-3.5 w-3.5" />大纲</TabsTrigger>
          {structured?.foreshadowing && structured.foreshadowing.length > 0 && (
            <TabsTrigger value="foreshadowing">伏笔追踪</TabsTrigger>
          )}
          {pacingData.length > 0 && (
            <TabsTrigger value="pacing"><TrendingUp className="mr-1 h-3.5 w-3.5" />紧张度曲线</TabsTrigger>
          )}
          {structured?.structure && structured.structure.length > 0 && (
            <TabsTrigger value="structure">结构</TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="outline" className="mt-4">
          {editing ? (
            <Textarea
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              className="min-h-[600px] font-mono text-sm"
            />
          ) : (
            <ScrollArea className="h-[600px] rounded-md border p-6">
              <article className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {outline?.markdown ?? "暂无大纲内容"}
                </ReactMarkdown>
              </article>
            </ScrollArea>
          )}
        </TabsContent>

        <TabsContent value="foreshadowing" className="mt-4">
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-3">
                {structured?.foreshadowing?.map((f) => (
                  <div key={f.id} className="flex items-start gap-4 p-3 rounded-lg border">
                    <Badge variant="outline" className="shrink-0 font-mono">{f.id}</Badge>
                    <div className="flex-1">
                      <p className="text-sm">{f.description}</p>
                      <div className="flex gap-4 mt-1 text-xs text-muted-foreground">
                        <span>埋设: {f.plant_chapter}</span>
                        <span>回收: {f.payoff_chapter || "待定"}</span>
                        {f.confidence && <span>置信度: {f.confidence}</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pacing" className="mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">紧张度曲线</CardTitle></CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={pacingData}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="chapter" className="text-xs" />
                  <YAxis domain={[0, 10]} className="text-xs" />
                  <ReTooltip
                    contentStyle={{ background: "hsl(var(--popover))", border: "1px solid hsl(var(--border))", borderRadius: "8px" }}
                    labelStyle={{ color: "hsl(var(--foreground))" }}
                  />
                  <Area type="monotone" dataKey="tension" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.1} />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="structure" className="mt-4">
          <div className="space-y-4">
            {structured?.structure?.map((act, i) => (
              <Card key={i}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold">{act.act}</h3>
                    <Badge variant="outline">{act.chapters}</Badge>
                  </div>
                  <div className="grid gap-2 sm:grid-cols-2 text-sm">
                    <div><span className="text-muted-foreground">弧线: </span>{act.arc}</div>
                    <div><span className="text-muted-foreground">节奏: </span>{act.pacing}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
