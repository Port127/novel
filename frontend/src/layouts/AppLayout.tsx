import type { ReactNode } from "react"
import { useEffect } from "react"
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { useLocation } from "react-router-dom"
import { AppSidebar } from "@/components/app-sidebar"
import { useAppStore } from "@/stores/app-store"
import { projects as projectApi } from "@/services/api"

const titleMap: Record<string, string> = {
  dashboard: "仪表板",
  characters: "角色",
  worldbuilding: "世界观",
  plot: "大纲",
  chapters: "章节",
  timeline: "时间线",
  relationships: "关系",
  quality: "写作质量",
  compliance: "合规检查",
  pipelines: "流水线",
  skills: "AI 助手",
  settings: "设置",
}

export default function AppLayout({ children }: { children: ReactNode }) {
  const location = useLocation()
  const segments = location.pathname.split("/").filter(Boolean)
  const { setProjects, setCurrentProject, currentProject } = useAppStore()

  useEffect(() => {
    projectApi.list().then((list) => {
      setProjects(list)
      const cur = list.find((p) => p.is_current)
      if (cur && !currentProject) setCurrentProject(cur)
    }).catch(() => {})
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 !h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              {segments.map((seg, i) => {
                const label = titleMap[seg] ?? decodeURIComponent(seg)
                const isLast = i === segments.length - 1
                const href = "/" + segments.slice(0, i + 1).join("/")
                return isLast ? (
                  <BreadcrumbItem key={href}>
                    <BreadcrumbPage>{label}</BreadcrumbPage>
                  </BreadcrumbItem>
                ) : (
                  <BreadcrumbItem key={href}>
                    <BreadcrumbLink href={href}>{label}</BreadcrumbLink>
                    <BreadcrumbSeparator />
                  </BreadcrumbItem>
                )
              })}
            </BreadcrumbList>
          </Breadcrumb>
        </header>

        <main className="flex-1 overflow-auto p-6">{children}</main>
      </SidebarInset>
    </>
  )
}
