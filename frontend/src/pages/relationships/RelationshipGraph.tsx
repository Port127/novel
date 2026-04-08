import { useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { useFetch } from "@/hooks/use-fetch"
import { relationships, characters as charApi } from "@/services/api"
import type { Relationship, CharacterEntry } from "@/types"

function strengthToColor(s: number) {
  if (s >= 4) return "border-emerald-500 bg-emerald-500/10"
  if (s >= 3) return "border-blue-500 bg-blue-500/10"
  if (s >= 2) return "border-amber-500 bg-amber-500/10"
  return "border-zinc-500 bg-zinc-500/10"
}

export default function RelationshipGraph() {
  const navigate = useNavigate()
  const { data: rels, loading: rLoading } = useFetch(() => relationships.list())
  const { data: chars, loading: cLoading } = useFetch(() => charApi.list())
  const { data: events } = useFetch(() => relationships.events())

  const loading = rLoading || cLoading

  const charMap = useMemo(() => {
    const m: Record<string, CharacterEntry> = {}
    chars?.forEach((c) => { m[c.name] = c })
    return m
  }, [chars])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">关系图谱</h1>
        <p className="text-muted-foreground">
          {rels?.length ?? 0} 组关系 · {events?.length ?? 0} 个事件
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Relationship Cards */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-lg font-semibold">关系列表</h2>
          {loading ? (
            <div className="space-y-3">{[1, 2, 3].map((i) => <Card key={i} className="h-24 animate-pulse bg-muted" />)}</div>
          ) : rels && rels.length > 0 ? (
            <div className="grid gap-3 sm:grid-cols-2">
              {rels.map((rel, i) => (
                <Card key={i} className={`border-l-4 ${strengthToColor(rel.strength)}`}>
                  <CardContent className="pt-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className="font-semibold cursor-pointer hover:text-primary"
                        onClick={() => navigate(`/characters/${encodeURIComponent(rel.pair[0])}`)}
                      >
                        {rel.pair[0]}
                      </span>
                      <Badge variant="outline" className="text-xs">{rel.type}</Badge>
                      <span
                        className="font-semibold cursor-pointer hover:text-primary"
                        onClick={() => navigate(`/characters/${encodeURIComponent(rel.pair[1])}`)}
                      >
                        {rel.pair[1]}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground">{rel.dynamic}</p>
                    {rel.tension_source && (
                      <p className="text-xs text-amber-500 mt-1">张力: {rel.tension_source}</p>
                    )}
                    <div className="flex items-center gap-1 mt-2">
                      {Array.from({ length: 5 }).map((_, j) => (
                        <div
                          key={j}
                          className={`h-1.5 w-6 rounded-full ${j < rel.strength ? "bg-primary" : "bg-muted"}`}
                        />
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-muted-foreground">暂无关系数据</div>
          )}
        </div>

        {/* Recent Events */}
        <div>
          <h2 className="text-lg font-semibold mb-4">关系事件</h2>
          <ScrollArea className="h-[500px]">
            <div className="space-y-3">
              {events && events.length > 0 ? events.slice(0, 20).map((evt, i) => (
                <Card key={i}>
                  <CardContent className="pt-3 pb-3">
                    <div className="flex items-center gap-2 text-xs mb-1">
                      <Badge variant="outline" className="text-[10px]">{evt.chapter}</Badge>
                      <span className="text-muted-foreground">{evt.type}</span>
                    </div>
                    <p className="text-sm font-medium">
                      {evt.characters[0]} ↔ {evt.characters[1]}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">{evt.change}</p>
                    {evt.cause && <p className="text-xs mt-0.5">原因: {evt.cause}</p>}
                  </CardContent>
                </Card>
              )) : (
                <p className="text-sm text-muted-foreground text-center py-8">暂无事件</p>
              )}
            </div>
          </ScrollArea>
        </div>
      </div>
    </div>
  )
}
