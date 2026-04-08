import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Plus, GripVertical } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"
import { StatusBadge } from "@/components/status-badge"
import { useFetch } from "@/hooks/use-fetch"
import { chapters } from "@/services/api"
import type { ChapterMeta, ChapterStatus } from "@/types"

const columns: { status: ChapterStatus; label: string; color: string }[] = [
  { status: "idea", label: "想法", color: "border-t-zinc-500" },
  { status: "outline", label: "大纲", color: "border-t-blue-500" },
  { status: "draft", label: "草稿", color: "border-t-amber-500" },
  { status: "revise", label: "修订", color: "border-t-purple-500" },
  { status: "final", label: "定稿", color: "border-t-emerald-500" },
  { status: "published", label: "已发布", color: "border-t-cyan-500" },
]

function ChapterCard({ ch, onClick }: { ch: ChapterMeta; onClick: () => void }) {
  return (
    <Card className="cursor-pointer hover:border-primary/50 transition-colors group" onClick={onClick}>
      <CardContent className="p-3 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono text-muted-foreground">{ch.id}</span>
          <GripVertical className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
        <div className="font-medium text-sm truncate">{ch.title || "未命名"}</div>
        {ch.goal && (
          <p className="text-xs text-muted-foreground line-clamp-2">{ch.goal}</p>
        )}
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          {ch.pov && <span>{ch.pov}</span>}
          {ch.word_actual > 0 && <span>{ch.word_actual.toLocaleString()} 字</span>}
        </div>
        {ch.characters_involved?.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {ch.characters_involved.slice(0, 3).map((c) => (
              <Badge key={c} variant="outline" className="text-[10px] px-1 py-0">{c}</Badge>
            ))}
            {ch.characters_involved.length > 3 && (
              <Badge variant="outline" className="text-[10px] px-1 py-0">+{ch.characters_involved.length - 3}</Badge>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default function ChapterBoard() {
  const navigate = useNavigate()
  const { data: chapterList, loading } = useFetch(() => chapters.list())

  const grouped: Record<string, ChapterMeta[]> = {}
  columns.forEach((col) => { grouped[col.status] = [] })
  ;(chapterList ?? []).forEach((ch) => {
    if (grouped[ch.status]) grouped[ch.status].push(ch)
    else grouped[ch.status] = [ch]
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">章节</h1>
          <p className="text-muted-foreground">
            {chapterList?.length ?? 0} 章 · {(chapterList ?? []).reduce((s, c) => s + (c.word_actual || 0), 0).toLocaleString()} 字
          </p>
        </div>
        <Button onClick={() => navigate("/skills")}>
          <Plus className="mr-2 h-4 w-4" />
          新建章节
        </Button>
      </div>

      <ScrollArea className="w-full">
        <div className="flex gap-4 pb-4" style={{ minWidth: columns.length * 280 }}>
          {columns.map((col) => (
            <div key={col.status} className="w-[260px] shrink-0">
              <Card className={`border-t-2 ${col.color}`}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm">{col.label}</CardTitle>
                    <Badge variant="secondary" className="text-xs">
                      {grouped[col.status]?.length ?? 0}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2 min-h-[200px]">
                  {loading ? (
                    <div className="h-20 animate-pulse bg-muted rounded" />
                  ) : grouped[col.status]?.length > 0 ? (
                    grouped[col.status].map((ch) => (
                      <ChapterCard
                        key={ch.id}
                        ch={ch}
                        onClick={() => navigate(`/chapters/${ch.id}`)}
                      />
                    ))
                  ) : (
                    <div className="text-center py-8 text-xs text-muted-foreground">
                      空
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  )
}
