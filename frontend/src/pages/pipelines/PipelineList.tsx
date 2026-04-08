import { useNavigate } from "react-router-dom"
import {
  BookOpen, FileEdit, Wrench, ScanSearch, ShieldCheck,
  GitBranch, NotebookPen, Settings2,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const pipelines = [
  {
    name: "大纲初建",
    skill: "pipeline-outline-bootstrap",
    description: "从草稿或想法出发，经过素材消化、确认、结构推导，产出初版大纲与基础设定",
    icon: BookOpen,
    tags: ["大纲", "设定", "初始化"],
    output: "可写大纲",
  },
  {
    name: "大纲优化",
    skill: "pipeline-outline-polish",
    description: "审查并补强现有大纲，联动世界观与一致性检查，输出更稳的剧情骨架",
    icon: FileEdit,
    tags: ["大纲", "审查", "优化"],
    output: "优化大纲",
  },
  {
    name: "设定整固",
    skill: "pipeline-setting-consolidate",
    description: "审查设定集，清理 tentative 堆积，补足设定缺口",
    icon: Settings2,
    tags: ["世界观", "设定", "确认"],
    output: "稳定设定集",
  },
  {
    name: "笔记分拣",
    skill: "pipeline-note-triage",
    description: "读取混合笔记，按内容类型自动分拣到角色、剧情、设定等模块",
    icon: NotebookPen,
    tags: ["笔记", "分类", "归档"],
    output: "笔记归档",
  },
  {
    name: "章节开局",
    skill: "pipeline-chapter-kickoff",
    description: "编排章节创建、状态推进和对应情节点补全，产出可直接开写的新章节",
    icon: BookOpen,
    tags: ["章节", "创建", "大纲"],
    output: "可开写章节",
  },
  {
    name: "草稿打磨",
    skill: "pipeline-draft-polish",
    description: "对草稿执行结构审查、人物声音检查与去 AI 感处理",
    icon: Wrench,
    tags: ["章节", "审查", "质量"],
    output: "可修订草稿",
  },
  {
    name: "连续性闸口",
    skill: "pipeline-continuity-gate",
    description: "汇总关系、时间线和跨模块一致性检查，生成修复清单",
    icon: GitBranch,
    tags: ["一致性", "检查", "修复"],
    output: "修复清单",
  },
  {
    name: "合规闸口",
    skill: "pipeline-compliance-gate",
    description: "串联借鉴登记、风险检查和范围报告，形成可追溯的合规闸口",
    icon: ShieldCheck,
    tags: ["合规", "风险", "发布"],
    output: "发前闸口",
  },
]

export default function PipelineList() {
  const navigate = useNavigate()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">流水线</h1>
        <p className="text-muted-foreground">8 个预置工作流，一键编排复杂操作</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {pipelines.map((p) => (
          <Card key={p.skill} className="hover:border-primary/50 transition-colors">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                    <p.icon className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-base">{p.name}</CardTitle>
                    <CardDescription className="text-xs">{p.skill}</CardDescription>
                  </div>
                </div>
                <Badge variant="outline" className="text-xs shrink-0">{p.output}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">{p.description}</p>
              <div className="flex items-center justify-between">
                <div className="flex gap-1">
                  {p.tags.map((t) => <Badge key={t} variant="secondary" className="text-xs">{t}</Badge>)}
                </div>
                <Button size="sm" onClick={() => navigate("/skills")}>
                  运行
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
