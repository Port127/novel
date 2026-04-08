import { useLocation, useNavigate } from "react-router-dom"
import {
  LayoutDashboard,
  Users,
  Globe,
  BookOpen,
  FileText,
  Clock,
  GitBranch,
  ShieldCheck,
  AlertTriangle,
  Workflow,
  Settings,
  Sparkles,
  Moon,
  Sun,
  ChevronDown,
} from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { useAppStore } from "@/stores/app-store"

const navGroups = [
  {
    label: "总览",
    items: [
      { title: "仪表板", icon: LayoutDashboard, path: "/dashboard" },
    ],
  },
  {
    label: "创作",
    items: [
      { title: "角色", icon: Users, path: "/characters" },
      { title: "世界观", icon: Globe, path: "/worldbuilding" },
      { title: "大纲", icon: BookOpen, path: "/plot" },
      { title: "章节", icon: FileText, path: "/chapters" },
      { title: "时间线", icon: Clock, path: "/timeline" },
      { title: "关系", icon: GitBranch, path: "/relationships" },
    ],
  },
  {
    label: "质量",
    items: [
      { title: "写作质量", icon: ShieldCheck, path: "/quality" },
      { title: "合规检查", icon: AlertTriangle, path: "/compliance" },
    ],
  },
  {
    label: "工具",
    items: [
      { title: "流水线", icon: Workflow, path: "/pipelines" },
      { title: "AI 助手", icon: Sparkles, path: "/skills" },
      { title: "设置", icon: Settings, path: "/settings" },
    ],
  },
]

export function AppSidebar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { currentProject, projects, darkMode, toggleDarkMode, setCurrentProject } =
    useAppStore()

  const projectName = currentProject?.name ?? "未选择项目"

  return (
    <Sidebar>
      <SidebarHeader className="border-b border-sidebar-border px-4 py-3">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-sm hover:bg-sidebar-accent transition-colors">
              <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground text-xs font-bold">
                {projectName[0]}
              </div>
              <div className="flex-1 truncate">
                <div className="font-semibold truncate">{projectName}</div>
                <div className="text-xs text-muted-foreground">
                  {currentProject?.genre ?? ""}
                </div>
              </div>
              <ChevronDown className="h-4 w-4 text-muted-foreground" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-64" align="start">
            {projects.map((p) => (
              <DropdownMenuItem
                key={p.name}
                onClick={() => setCurrentProject(p)}
                className={p.is_current ? "bg-accent" : ""}
              >
                <div className="truncate">
                  <div className="font-medium">{p.name}</div>
                  <div className="text-xs text-muted-foreground">
                    {p.genre} · {p.word_count.toLocaleString()} 字
                  </div>
                </div>
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarHeader>

      <SidebarContent>
        {navGroups.map((group) => (
          <SidebarGroup key={group.label}>
            <SidebarGroupLabel>{group.label}</SidebarGroupLabel>
            <SidebarMenu>
              {group.items.map((item) => {
                const active = location.pathname.startsWith(item.path)
                return (
                  <SidebarMenuItem key={item.path}>
                    <SidebarMenuButton
                      isActive={active}
                      onClick={() => navigate(item.path)}
                      tooltip={item.title}
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </SidebarGroup>
        ))}
      </SidebarContent>

      <SidebarFooter className="border-t border-sidebar-border p-2">
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start gap-2"
          onClick={toggleDarkMode}
        >
          {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          {darkMode ? "浅色模式" : "深色模式"}
        </Button>
      </SidebarFooter>
    </Sidebar>
  )
}
