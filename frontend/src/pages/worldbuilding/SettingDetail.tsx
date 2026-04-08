import { useParams, useNavigate } from "react-router-dom"
import { ArrowLeft, Edit, Sparkles } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { StatusBadge } from "@/components/status-badge"
import { useFetch } from "@/hooks/use-fetch"
import { worldbuilding } from "@/services/api"

export default function SettingDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: setting, loading } = useFetch(() => worldbuilding.get(id!), [id])

  if (loading) return <div className="space-y-4">{[1, 2].map((i) => <Card key={i} className="h-40 animate-pulse bg-muted" />)}</div>
  if (!setting) return <div className="text-center py-12 text-muted-foreground">设定未找到</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/worldbuilding")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{setting.name}</h1>
            <StatusBadge status={setting.status} />
            <Badge variant="secondary">{setting.category}</Badge>
          </div>
          <p className="text-muted-foreground">{setting.summary}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm"><Edit className="mr-2 h-4 w-4" />编辑</Button>
          <Button variant="outline" size="sm" onClick={() => navigate("/skills")}><Sparkles className="mr-2 h-4 w-4" />AI 审查</Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="md:col-span-2">
          <CardHeader><CardTitle className="text-base">描述</CardTitle></CardHeader>
          <CardContent><p className="text-sm whitespace-pre-wrap">{setting.description || "暂无描述"}</p></CardContent>
        </Card>

        {setting.rules?.length > 0 && (
          <Card>
            <CardHeader><CardTitle className="text-base">规则</CardTitle></CardHeader>
            <CardContent><ul className="list-disc list-inside space-y-1 text-sm">{setting.rules.map((r, i) => <li key={i}>{r}</li>)}</ul></CardContent>
          </Card>
        )}

        {setting.constraints?.length > 0 && (
          <Card>
            <CardHeader><CardTitle className="text-base">约束</CardTitle></CardHeader>
            <CardContent><ul className="list-disc list-inside space-y-1 text-sm">{setting.constraints.map((c, i) => <li key={i}>{c}</li>)}</ul></CardContent>
          </Card>
        )}

        {setting.character_links?.length > 0 && (
          <Card>
            <CardHeader><CardTitle className="text-base">关联角色</CardTitle></CardHeader>
            <CardContent className="space-y-2">
              {setting.character_links.map((l, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <span className="cursor-pointer hover:text-primary" onClick={() => navigate(`/characters/${encodeURIComponent(l.character)}`)}>{l.character}</span>
                  <span className="text-muted-foreground">{l.relation}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {setting.plot_links?.length > 0 && (
          <Card>
            <CardHeader><CardTitle className="text-base">关联剧情</CardTitle></CardHeader>
            <CardContent className="space-y-2">
              {setting.plot_links.map((l, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <span>{l.node}</span><span className="text-muted-foreground">{l.role}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {setting.open_questions?.length > 0 && (
          <Card className="md:col-span-2">
            <CardHeader><CardTitle className="text-base">待解决问题</CardTitle></CardHeader>
            <CardContent><ul className="list-disc list-inside space-y-1 text-sm text-amber-500">{setting.open_questions.map((q, i) => <li key={i}>{q}</li>)}</ul></CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
