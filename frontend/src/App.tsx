import { Routes, Route, Navigate } from "react-router-dom"
import { useEffect } from "react"
import { useAppStore } from "@/stores/app-store"
import { SidebarProvider } from "@/components/ui/sidebar"
import AppLayout from "@/layouts/AppLayout"
import Dashboard from "@/pages/Dashboard"
import CharacterList from "@/pages/characters/CharacterList"
import CharacterDetail from "@/pages/characters/CharacterDetail"
import WorldbuildingList from "@/pages/worldbuilding/WorldbuildingList"
import SettingDetail from "@/pages/worldbuilding/SettingDetail"
import PlotOutline from "@/pages/plot/PlotOutline"
import ChapterBoard from "@/pages/chapters/ChapterBoard"
import ChapterEditor from "@/pages/chapters/ChapterEditor"
import TimelineView from "@/pages/timeline/TimelineView"
import RelationshipGraph from "@/pages/relationships/RelationshipGraph"
import QualityDashboard from "@/pages/quality/QualityDashboard"
import ComplianceReport from "@/pages/compliance/ComplianceReport"
import PipelineList from "@/pages/pipelines/PipelineList"
import Settings from "@/pages/settings/Settings"
import SkillRunner from "@/pages/skills/SkillRunner"

export default function App() {
  const darkMode = useAppStore((s) => s.darkMode)

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode)
  }, [darkMode])

  return (
    <SidebarProvider>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/characters" element={<CharacterList />} />
          <Route path="/characters/:name" element={<CharacterDetail />} />
          <Route path="/worldbuilding" element={<WorldbuildingList />} />
          <Route path="/worldbuilding/:id" element={<SettingDetail />} />
          <Route path="/plot" element={<PlotOutline />} />
          <Route path="/chapters" element={<ChapterBoard />} />
          <Route path="/chapters/:id" element={<ChapterEditor />} />
          <Route path="/timeline" element={<TimelineView />} />
          <Route path="/relationships" element={<RelationshipGraph />} />
          <Route path="/quality" element={<QualityDashboard />} />
          <Route path="/compliance" element={<ComplianceReport />} />
          <Route path="/pipelines" element={<PipelineList />} />
          <Route path="/skills" element={<SkillRunner />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </AppLayout>
    </SidebarProvider>
  )
}
