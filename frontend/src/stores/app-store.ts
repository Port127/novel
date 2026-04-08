import { create } from "zustand"
import { persist } from "zustand/middleware"
import type { ProjectListItem, LLMConfig } from "@/types"

interface AppState {
  currentProject: ProjectListItem | null
  projects: ProjectListItem[]
  sidebarOpen: boolean
  darkMode: boolean
  llmConfig: LLMConfig

  setCurrentProject: (p: ProjectListItem | null) => void
  setProjects: (p: ProjectListItem[]) => void
  toggleSidebar: () => void
  toggleDarkMode: () => void
  setLLMConfig: (c: Partial<LLMConfig>) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      currentProject: null,
      projects: [],
      sidebarOpen: true,
      darkMode: true,
      llmConfig: {
        api_url: "https://api.openai.com/v1/chat/completions",
        api_token: "",
        model: "gpt-4o",
        temperature: 0.7,
        max_tokens: 4096,
      },

      setCurrentProject: (p) => set({ currentProject: p }),
      setProjects: (p) => set({ projects: p }),
      toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      toggleDarkMode: () => set((s) => ({ darkMode: !s.darkMode })),
      setLLMConfig: (c) =>
        set((s) => ({ llmConfig: { ...s.llmConfig, ...c } })),
    }),
    { name: "novel-app-store" },
  ),
)
