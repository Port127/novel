import { useNavigate } from "react-router-dom"
import { ShieldAlert, FileCheck, Sparkles } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useFetch } from "@/hooks/use-fetch"
import { compliance } from "@/services/api"

const levelColors: Record<string, string> = {
  low: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  medium: "bg-amber-500/10 text-amber-500 border-amber-500/20",
  high: "bg-red-500/10 text-red-500 border-red-500/20",
}

export default function ComplianceReport() {
  const navigate = useNavigate()
  const { data: inspirations, loading: iLoading } = useFetch(() => compliance.inspirations())
  const { data: risks, loading: rLoading } = useFetch(() => compliance.risks())

  const loading = iLoading || rLoading

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">合规检查</h1>
          <p className="text-muted-foreground">借鉴登记与风险监控</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
          <Sparkles className="mr-2 h-4 w-4" />
          运行合规闸口
        </Button>
      </div>

      <Tabs defaultValue="risks">
        <TabsList>
          <TabsTrigger value="risks">
            <ShieldAlert className="mr-1 h-3.5 w-3.5" />
            风险报告 ({risks?.length ?? 0})
          </TabsTrigger>
          <TabsTrigger value="inspirations">
            <FileCheck className="mr-1 h-3.5 w-3.5" />
            借鉴登记 ({inspirations?.length ?? 0})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="risks" className="mt-4">
          {loading ? (
            <div className="space-y-3">{[1, 2].map((i) => <Card key={i} className="h-24 animate-pulse bg-muted" />)}</div>
          ) : risks && risks.length > 0 ? (
            <div className="space-y-3">
              {risks.map((r, i) => (
                <Card key={i}>
                  <CardContent className="pt-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{r.chapter_id}</Badge>
                        <Badge className={levelColors[r.level]}>{r.level.toUpperCase()}</Badge>
                      </div>
                      <span className="text-xs text-muted-foreground">{r.checked_at}</span>
                    </div>
                    {r.issues?.length > 0 && (
                      <div className="space-y-1 mt-2">
                        {r.issues.map((issue, j) => (
                          <div key={j} className="flex items-center gap-2 text-sm">
                            <span className="h-1.5 w-1.5 rounded-full bg-red-500" />
                            {issue}
                          </div>
                        ))}
                      </div>
                    )}
                    {r.suggestions?.length > 0 && (
                      <div className="space-y-1 mt-2">
                        {r.suggestions.map((s, j) => (
                          <div key={j} className="flex items-center gap-2 text-sm text-muted-foreground">
                            <span className="h-1.5 w-1.5 rounded-full bg-blue-500" />
                            {s}
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-muted-foreground">暂无风险报告</div>
          )}
        </TabsContent>

        <TabsContent value="inspirations" className="mt-4">
          {loading ? (
            <div className="space-y-3">{[1, 2].map((i) => <Card key={i} className="h-20 animate-pulse bg-muted" />)}</div>
          ) : inspirations && inspirations.length > 0 ? (
            <div className="space-y-3">
              {inspirations.map((insp, i) => (
                <Card key={i}>
                  <CardContent className="pt-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="outline">{insp.chapter_id}</Badge>
                      <span className="text-sm font-medium">{insp.material_id}</span>
                    </div>
                    {insp.dimensions?.length > 0 && (
                      <div className="flex gap-1 mb-1">
                        {insp.dimensions.map((d) => <Badge key={d} variant="secondary" className="text-xs">{d}</Badge>)}
                      </div>
                    )}
                    {insp.note && <p className="text-xs text-muted-foreground">{insp.note}</p>}
                    <p className="text-xs text-muted-foreground mt-1">{insp.date}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-muted-foreground">暂无借鉴登记</div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
