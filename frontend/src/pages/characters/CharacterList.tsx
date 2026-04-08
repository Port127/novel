import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Plus, Search, Users, Swords, UserCircle, UserMinus } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useFetch } from "@/hooks/use-fetch"
import { characters } from "@/services/api"
import type { CharacterEntry } from "@/types"

const roleConfig: Record<string, { label: string; icon: typeof Users; color: string }> = {
  protagonist: { label: "主角", icon: Users, color: "text-amber-500" },
  antagonist: { label: "反派", icon: Swords, color: "text-red-500" },
  supporting: { label: "配角", icon: UserCircle, color: "text-blue-500" },
  minor: { label: "路人", icon: UserMinus, color: "text-zinc-500" },
}

function CharacterCard({ char, onClick }: { char: CharacterEntry; onClick: () => void }) {
  const role = roleConfig[char.role] ?? roleConfig.minor
  const Icon = role.icon
  return (
    <Card className="cursor-pointer hover:border-primary/50 transition-colors group" onClick={onClick}>
      <CardContent className="pt-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <Icon className={`h-5 w-5 ${role.color}`} />
            </div>
            <div>
              <h3 className="font-semibold group-hover:text-primary transition-colors">
                {char.name}
              </h3>
              <p className="text-xs text-muted-foreground">{char.archetype || role.label}</p>
            </div>
          </div>
          <Badge variant="outline" className={role.color}>{role.label}</Badge>
        </div>
        <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
          {char.first_appearance && <span>初登场: {char.first_appearance}</span>}
          {char.affiliation?.length > 0 && (
            <span>阵营: {char.affiliation.join(", ")}</span>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default function CharacterList() {
  const navigate = useNavigate()
  const { data: charList, loading } = useFetch(() => characters.list())
  const [search, setSearch] = useState("")
  const [activeTab, setActiveTab] = useState("all")

  const filtered = (charList ?? []).filter((c) => {
    const matchSearch = !search || c.name.includes(search) || c.archetype?.includes(search)
    const matchRole = activeTab === "all" || c.role === activeTab
    return matchSearch && matchRole
  })

  const counts = {
    all: charList?.length ?? 0,
    protagonist: charList?.filter((c) => c.role === "protagonist").length ?? 0,
    supporting: charList?.filter((c) => c.role === "supporting").length ?? 0,
    antagonist: charList?.filter((c) => c.role === "antagonist").length ?? 0,
    minor: charList?.filter((c) => c.role === "minor").length ?? 0,
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">角色</h1>
          <p className="text-muted-foreground">管理你的故事角色</p>
        </div>
        <Button onClick={() => navigate("/skills")}>
          <Plus className="mr-2 h-4 w-4" />
          新建角色
        </Button>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="搜索角色..." value={search} onChange={(e) => setSearch(e.target.value)} className="pl-10" />
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="all">全部 ({counts.all})</TabsTrigger>
          <TabsTrigger value="protagonist">主角 ({counts.protagonist})</TabsTrigger>
          <TabsTrigger value="supporting">配角 ({counts.supporting})</TabsTrigger>
          <TabsTrigger value="antagonist">反派 ({counts.antagonist})</TabsTrigger>
          <TabsTrigger value="minor">路人 ({counts.minor})</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="mt-4">
          {loading ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="h-32 animate-pulse bg-muted" />
              ))}
            </div>
          ) : filtered.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filtered.map((char) => (
                <CharacterCard
                  key={char.name}
                  char={char}
                  onClick={() => navigate(`/characters/${encodeURIComponent(char.name)}`)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-muted-foreground">
              {search ? "没有匹配的角色" : "暂无角色，使用 AI 助手创建第一个角色"}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
