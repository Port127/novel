import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import {
  FileText, Users, Globe, BookOpen, Clock,
  TrendingUp, AlertTriangle, CheckCircle2,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { StatCard } from "@/components/stat-card"
import { StatusBadge } from "@/components/status-badge"
import { projects as projectApi, characters, chapters, worldbuilding } from "@/services/api"
import { useAppStore } from "@/stores/app-store"
import type { ProjectMeta, ProjectState, ChapterMeta, CharacterEntry } from "@/types"

export default function Dashboard() {
  const navigate = useNavigate()
  const currentProject = useAppStore((s) => s.currentProject)
  const [meta, setMeta] = useState<ProjectMeta | null>(null)
  const [state, setState] = useState<ProjectState | null>(null)
  const [chapterList, setChapterList] = useState<ChapterMeta[]>([])
  const [characterList, setCharacterList] = useState<CharacterEntry[]>([])
  const [settingCount, setSettingCount] = useState(0)

  useEffect(() => {
    projectApi.current().then(({ meta: m, state: s }) => { setMeta(m); setState(s) }).catch(() => {})
    chapters.list().then(setChapterList).catch(() => {})
    characters.list().then(setCharacterList).catch(() => {})
    worldbuilding.index().then((idx) => setSettingCount(idx.entries?.length ?? 0)).catch(() => {})
  }, [currentProject?.name])

  const wordCount = meta?.writing?.current_word_count ?? chapterList.reduce((s, c) => s + (c.word_actual || 0), 0)
  const chapterCount = chapterList.length
  const draftCount = chapterList.filter((c) => c.status === "draft").length
  const finalCount = chapterList.filter((c) => c.status === "final" || c.status === "published").length
  const recentChapters = [...chapterList].sort((a, b) => b.updated.localeCompare(a.updated)).slice(0, 5)

  const statusGroups: Record<string, number> = {}
  chapterList.forEach((c) => { statusGroups[c.status] = (statusGroups[c.status] || 0) + 1 })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          {meta?.name ?? currentProject?.name ?? "小说工作台"}
        </h1>
        <p className="text-muted-foreground mt-1">
          {meta?.genre}{meta?.sub_genre?.length ? ` · ${meta.sub_genre.join(" / ")}` : ""}
          {state?.current_focus ? ` — ${state.current_focus}` : ""}
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="总字数" value={wordCount.toLocaleString()} icon={FileText} description={`目标 ${(meta?.writing?.target_word_count ?? 0).toLocaleString()} 字`} />
        <StatCard title="章节" value={chapterCount} icon={BookOpen} description={`${finalCount} 已完成 · ${draftCount} 草稿中`} />
        <StatCard title="角色" value={characterList.length} icon={Users} description={`${characterList.filter((c) => c.role === "protagonist").length} 主角 · ${characterList.filter((c) => c.role === "supporting").length} 配角`} />
        <StatCard title="设定条目" value={settingCount} icon={Globe} />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Chapter Status Distribution */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">章节状态分布</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(statusGroups).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <StatusBadge status={status} />
                <div className="flex items-center gap-2">
                  <div className="w-24 h-2 rounded-full bg-muted overflow-hidden">
                    <div
                      className="h-full rounded-full bg-primary transition-all"
                      style={{ width: `${(count / chapterCount) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium w-6 text-right">{count}</span>
                </div>
              </div>
            ))}
            {chapterCount === 0 && (
              <p className="text-sm text-muted-foreground">暂无章节数据</p>
            )}
          </CardContent>
        </Card>

        {/* Recent Chapters */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base">最近更新章节</CardTitle>
              <CardDescription>最近编辑的章节</CardDescription>
            </div>
            <Button variant="outline" size="sm" onClick={() => navigate("/chapters")}>
              查看全部
            </Button>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[240px]">
              <div className="space-y-3">
                {recentChapters.map((ch) => (
                  <div
                    key={ch.id}
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent/50 cursor-pointer transition-colors"
                    onClick={() => navigate(`/chapters/${ch.id}`)}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{ch.id}</span>
                        <span className="text-muted-foreground truncate">{ch.title}</span>
                      </div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        {ch.pov && `视角: ${ch.pov}`}
                        {ch.word_actual > 0 && ` · ${ch.word_actual.toLocaleString()} 字`}
                      </div>
                    </div>
                    <StatusBadge status={ch.status} />
                  </div>
                ))}
                {recentChapters.length === 0 && (
                  <p className="text-sm text-muted-foreground text-center py-8">
                    暂无章节，开始创作吧
                  </p>
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">快捷操作</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="h-auto py-4 flex-col gap-2" onClick={() => navigate("/chapters")}>
              <FileText className="h-5 w-5" />
              <span>新建章节</span>
            </Button>
            <Button variant="outline" className="h-auto py-4 flex-col gap-2" onClick={() => navigate("/characters")}>
              <Users className="h-5 w-5" />
              <span>管理角色</span>
            </Button>
            <Button variant="outline" className="h-auto py-4 flex-col gap-2" onClick={() => navigate("/skills")}>
              <TrendingUp className="h-5 w-5" />
              <span>AI 助手</span>
            </Button>
            <Button variant="outline" className="h-auto py-4 flex-col gap-2" onClick={() => navigate("/quality")}>
              <CheckCircle2 className="h-5 w-5" />
              <span>质量检查</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
