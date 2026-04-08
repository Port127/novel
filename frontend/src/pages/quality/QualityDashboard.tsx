import { useNavigate } from "react-router-dom"
import { ShieldCheck, Sparkles, BarChart3 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useFetch } from "@/hooks/use-fetch"
import { quality } from "@/services/api"
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts"

const dimensionLabels: Record<string, string> = {
  cliche: "套话", sentence: "句式", metaphor: "比喻",
  description: "描写", dialogue: "对白", transition: "转折", psychology: "心理",
}

function gradeColor(grade: string) {
  if (grade === "A" || grade === "A+") return "text-emerald-500"
  if (grade === "B" || grade === "B+") return "text-blue-500"
  if (grade === "C" || grade === "C+") return "text-amber-500"
  return "text-red-500"
}

export default function QualityDashboard() {
  const navigate = useNavigate()
  const { data: reports, loading } = useFetch(() => quality.aiTrace())

  const latestReport = reports?.[reports.length - 1]

  const radarData = latestReport
    ? Object.entries(latestReport.dimensions).map(([key, value]) => ({
        dimension: dimensionLabels[key] || key,
        score: value,
        fullMark: 10,
      }))
    : []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">写作质量</h1>
          <p className="text-muted-foreground">AI 痕迹检测与文风审计</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
            <ShieldCheck className="mr-2 h-4 w-4" />
            运行检测
          </Button>
          <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
            <Sparkles className="mr-2 h-4 w-4" />
            去 AI 改写
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2">{[1, 2].map((i) => <Card key={i} className="h-60 animate-pulse bg-muted" />)}</div>
      ) : latestReport ? (
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Score Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">最近检测 — {latestReport.chapter_id}</CardTitle>
              <CardDescription>{latestReport.checked_at}</CardDescription>
            </CardHeader>
            <CardContent className="flex items-center gap-8">
              <div className="text-center">
                <div className={`text-5xl font-bold ${gradeColor(latestReport.grade)}`}>
                  {latestReport.grade}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  得分 {latestReport.score}/100
                </div>
              </div>
              <div className="flex-1 space-y-2">
                {latestReport.top_issues?.map((issue, i) => (
                  <div key={i} className="flex items-center gap-2 text-sm">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    {issue}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Radar Chart */}
          {radarData.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base">七维评分</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <RadarChart data={radarData}>
                    <PolarGrid className="stroke-muted" />
                    <PolarAngleAxis dataKey="dimension" className="text-xs" />
                    <PolarRadiusAxis domain={[0, 10]} tick={false} />
                    <Radar dataKey="score" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.2} />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* History */}
          {reports && reports.length > 1 && (
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="text-base">检测历史</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {reports.map((r, i) => (
                    <div key={i} className="flex items-center justify-between p-3 rounded-lg border">
                      <div className="flex items-center gap-3">
                        <Badge variant="outline">{r.chapter_id}</Badge>
                        <span className={`text-lg font-bold ${gradeColor(r.grade)}`}>{r.grade}</span>
                        <span className="text-sm text-muted-foreground">{r.score}/100</span>
                      </div>
                      <span className="text-xs text-muted-foreground">{r.checked_at}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      ) : (
        <div className="text-center py-16">
          <BarChart3 className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold">暂无质量检测数据</h3>
          <p className="text-muted-foreground mt-1">使用 AI 助手对章节运行检测</p>
          <Button className="mt-4" onClick={() => navigate("/skills")}>
            <Sparkles className="mr-2 h-4 w-4" />
            开始检测
          </Button>
        </div>
      )}
    </div>
  )
}
