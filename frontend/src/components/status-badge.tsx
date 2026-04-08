import { Badge } from "@/components/ui/badge"
import type { ChapterStatus } from "@/types"

const statusConfig: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  idea: { label: "想法", variant: "outline" },
  outline: { label: "大纲", variant: "secondary" },
  draft: { label: "草稿", variant: "default" },
  revise: { label: "修订", variant: "default" },
  final: { label: "定稿", variant: "default" },
  published: { label: "已发布", variant: "default" },
  tentative: { label: "待确认", variant: "outline" },
  confirmed: { label: "已确认", variant: "default" },
  deprecated: { label: "已废弃", variant: "destructive" },
  drafting: { label: "写作中", variant: "default" },
  revising: { label: "修订中", variant: "secondary" },
  completed: { label: "已完成", variant: "default" },
  suspended: { label: "暂停", variant: "destructive" },
}

const statusColors: Record<string, string> = {
  idea: "bg-zinc-500/10 text-zinc-500 border-zinc-500/20",
  outline: "bg-blue-500/10 text-blue-500 border-blue-500/20",
  draft: "bg-amber-500/10 text-amber-500 border-amber-500/20",
  revise: "bg-purple-500/10 text-purple-500 border-purple-500/20",
  final: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  published: "bg-cyan-500/10 text-cyan-500 border-cyan-500/20",
  tentative: "bg-amber-500/10 text-amber-500 border-amber-500/20",
  confirmed: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  deprecated: "bg-red-500/10 text-red-500 border-red-500/20",
}

export function StatusBadge({ status }: { status: ChapterStatus | string }) {
  const config = statusConfig[status]
  const color = statusColors[status]
  return (
    <Badge variant={config?.variant ?? "outline"} className={color}>
      {config?.label ?? status}
    </Badge>
  )
}
