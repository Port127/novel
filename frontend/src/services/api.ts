const BASE = "/api"

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  })
  if (!res.ok) {
    const body = await res.text().catch(() => "")
    throw new Error(`${res.status}: ${body || res.statusText}`)
  }
  return res.json() as Promise<T>
}

function get<T>(path: string) {
  return request<T>(path)
}
function post<T>(path: string, body: unknown) {
  return request<T>(path, { method: "POST", body: JSON.stringify(body) })
}
function put<T>(path: string, body: unknown) {
  return request<T>(path, { method: "PUT", body: JSON.stringify(body) })
}
function del<T>(path: string) {
  return request<T>(path, { method: "DELETE" })
}

import type {
  ProjectListItem, ProjectMeta, ProjectState,
  CharacterEntry, Character,
  WorldbuildingIndex, Setting,
  ChapterMeta, ChapterContent,
  PlotOutline,
  TimelineEvent,
  Relationship, RelationEvent,
  InspirationEntry, RiskEntry,
  AITraceReport,
  LLMConfig, SkillInfo,
} from "@/types"

// ── Projects ─────────────────────────────────────────────

export const projects = {
  list: async (): Promise<ProjectListItem[]> => {
    const raw = await get<{ name: string; path: string; meta: Record<string, unknown>; state: Record<string, unknown> }[]>("/projects")
    const current = await get<{ current: { current_project: string } }>("/projects/current").catch(() => ({ current: { current_project: "" } }))
    return raw.map((p) => {
      const meta = p.meta || {}
      const writing = (meta.writing || {}) as Record<string, unknown>
      return {
        name: p.name,
        path: p.path,
        genre: (meta.genre as string) || "",
        status: (meta.status as string) || "drafting",
        chapter_count: (writing.chapter_count as number) || 0,
        word_count: (writing.current_word_count as number) || 0,
        updated: (meta.updated as string) || "",
        is_current: p.name === current.current.current_project,
      }
    })
  },

  current: async (): Promise<{ meta: ProjectMeta; state: ProjectState }> => {
    const raw = await get<{ meta: Record<string, unknown>; state: Record<string, unknown> }>("/projects/current")
    return { meta: raw.meta as unknown as ProjectMeta, state: raw.state as unknown as ProjectState }
  },

  switch: (name: string) =>
    post<{ ok: boolean }>("/projects/switch", { project_name: name, project_path: `projects/${name}` }),
}

// ── Characters ───────────────────────────────────────────

export const characters = {
  list: async (): Promise<CharacterEntry[]> => {
    const raw = await get<{ entries: CharacterEntry[] }>("/characters")
    return raw.entries || []
  },
  get: (name: string) => get<Character>(`/characters/${encodeURIComponent(name)}`),
  create: (data: Partial<Character>) =>
    post<{ ok: boolean }>("/characters", { name: data.name, role: data.role, data }),
  update: (name: string, data: Partial<Character>) =>
    put<{ ok: boolean }>(`/characters/${encodeURIComponent(name)}`, { data }),
  delete: (name: string) => del<void>(`/characters/${encodeURIComponent(name)}`),
}

// ── Worldbuilding ────────────────────────────────────────

export const worldbuilding = {
  index: () => get<WorldbuildingIndex>("/worldbuilding"),
  get: (id: string) => get<Setting>(`/worldbuilding/entries/${id}`),
  create: (data: Partial<Setting>) => post<Setting>("/worldbuilding/entries", data),
  update: (id: string, data: Partial<Setting>) =>
    put<Setting>(`/worldbuilding/entries/${id}`, data),
  delete: (id: string) => del<void>(`/worldbuilding/entries/${id}`),
}

// ── Chapters ─────────────────────────────────────────────

export const chapters = {
  list: async (): Promise<ChapterMeta[]> => {
    const raw = await get<{ chapters: ChapterMeta[] }>("/chapters")
    return raw.chapters || []
  },
  get: (id: string) => get<ChapterContent>(`/chapters/${id}`),
  create: (data: { id: string; title: string; goal: string }) =>
    post<{ ok: boolean }>("/chapters", data),
  updateContent: (id: string, content: string) =>
    put<void>(`/chapters/${id}`, { content }),
  updateMeta: (id: string, data: Partial<ChapterMeta>) =>
    put<{ ok: boolean }>(`/chapters/${id}/meta`, data),
  delete: (id: string) => del<void>(`/chapters/${id}`),
}

// ── Plot ─────────────────────────────────────────────────

export const plot = {
  outline: async (): Promise<PlotOutline> => {
    const raw = await get<{ markdown: string; structured: PlotOutline["structured"] }>("/plot/outline")
    return { markdown: raw.markdown || "", structured: raw.structured || null }
  },
  updateOutline: (markdown: string) => put<void>("/plot/outline", { markdown }),
}

// ── Timeline ─────────────────────────────────────────────

export const timeline = {
  list: async (): Promise<TimelineEvent[]> => {
    const raw = await get<{ events: TimelineEvent[] }>("/timeline")
    return raw.events || []
  },
  add: (event: Partial<TimelineEvent>) => post<TimelineEvent>("/timeline", event),
}

// ── Relationships ────────────────────────────────────────

export const relationships = {
  list: async (): Promise<Relationship[]> => {
    const raw = await get<{ relations: Relationship[] }>("/relationships")
    return raw.relations || []
  },
  events: async (): Promise<RelationEvent[]> => {
    const raw = await get<{ events: RelationEvent[] }>("/relationships/events")
    return raw.events || []
  },
}

// ── Compliance ───────────────────────────────────────────

export const compliance = {
  inspirations: async (): Promise<InspirationEntry[]> => {
    const raw = await get<{ entries: InspirationEntry[] }>("/compliance/inspirations")
    return raw.entries || []
  },
  risks: async (): Promise<RiskEntry[]> => {
    const raw = await get<{ entries: RiskEntry[] }>("/compliance/risks")
    return raw.entries || []
  },
}

// ── Quality ──────────────────────────────────────────────

export const quality = {
  aiTrace: async (): Promise<AITraceReport[]> => {
    const raw = await get<{ reports: AITraceReport[] }>("/quality/ai-trace")
    return raw.reports || []
  },
}

// ── LLM ──────────────────────────────────────────────────

export const llm = {
  getConfig: () => get<LLMConfig>("/llm/config"),
  setConfig: (config: LLMConfig) =>
    put<{ ok: boolean }>("/llm/config", {
      api_url: config.api_url,
      api_key: config.api_token,
      model: config.model,
      temperature: config.temperature,
      max_tokens: config.max_tokens,
    }),
  chat: (messages: { role: string; content: string }[]) => {
    return fetch(`${BASE}/llm/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
    })
  },
}

// ── Skills ───────────────────────────────────────────────

export const skills = {
  list: async (): Promise<SkillInfo[]> => {
    const raw = await get<{ skills: SkillInfo[] }>("/skills")
    return raw.skills || []
  },
  execute: (skill: string, params: Record<string, unknown>) => {
    return fetch(`${BASE}/skills/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skill_name: skill,
        arguments: typeof params.query === "string" ? params.query : JSON.stringify(params),
      }),
    })
  },
}
