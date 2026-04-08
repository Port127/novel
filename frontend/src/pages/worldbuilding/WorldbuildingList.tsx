import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Plus, Search, Globe, Shield, Zap, Users as UsersIcon, MapPin } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { StatusBadge } from "@/components/status-badge"
import { useFetch } from "@/hooks/use-fetch"
import { worldbuilding } from "@/services/api"

const categoryIcons: Record<string, typeof Globe> = {
  world_rule: Shield,
  power_system: Zap,
  faction: UsersIcon,
  geography: MapPin,
}
const categoryLabels: Record<string, string> = {
  world_rule: "世界规则",
  power_system: "力量体系",
  faction: "阵营",
  geography: "地理",
  lore: "传说",
  terminology: "术语",
  species: "物种",
  artifact: "神器",
}

export default function WorldbuildingList() {
  const navigate = useNavigate()
  const { data: index, loading } = useFetch(() => worldbuilding.index())
  const [search, setSearch] = useState("")
  const [tab, setTab] = useState("all")

  const entries = index?.entries ?? []
  const filtered = entries.filter((e) => {
    const matchSearch = !search || e.name.includes(search) || e.id.includes(search)
    const matchTab = tab === "all" || e.category === tab || e.status === tab
    return matchSearch && matchTab
  })

  const categories = [...new Set(entries.map((e) => e.category))]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">世界观</h1>
          <p className="text-muted-foreground">设定集条目管理</p>
        </div>
        <Button onClick={() => navigate("/skills")}>
          <Plus className="mr-2 h-4 w-4" />
          新建设定
        </Button>
      </div>

      {/* Core Concepts */}
      {index?.core_concepts && index.core_concepts.length > 0 && (
        <div className="grid gap-3 md:grid-cols-3">
          {index.core_concepts.map((c) => (
            <Card key={c.entry_id} className="cursor-pointer hover:border-primary/50 transition-colors" onClick={() => navigate(`/worldbuilding/${c.entry_id}`)}>
              <CardContent className="pt-4">
                <div className="font-semibold text-sm">{c.name}</div>
                <div className="text-xs text-muted-foreground mt-1">{c.one_liner}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="搜索设定..." value={search} onChange={(e) => setSearch(e.target.value)} className="pl-10" />
        </div>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="all">全部 ({entries.length})</TabsTrigger>
          {categories.map((c) => (
            <TabsTrigger key={c} value={c}>
              {categoryLabels[c] || c} ({entries.filter((e) => e.category === c).length})
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value={tab} className="mt-4">
          {loading ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3].map((i) => <Card key={i} className="h-24 animate-pulse bg-muted" />)}
            </div>
          ) : filtered.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filtered.map((entry) => {
                const Icon = categoryIcons[entry.category] ?? Globe
                return (
                  <Card key={entry.id} className="cursor-pointer hover:border-primary/50 transition-colors" onClick={() => navigate(`/worldbuilding/${entry.id}`)}>
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <Icon className="h-5 w-5 text-muted-foreground" />
                          <div>
                            <h3 className="font-semibold">{entry.name}</h3>
                            <p className="text-xs text-muted-foreground">{entry.id}</p>
                          </div>
                        </div>
                        <StatusBadge status={entry.status} />
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          ) : (
            <div className="text-center py-12 text-muted-foreground">暂无匹配的设定条目</div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
