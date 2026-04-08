// ── Project ──────────────────────────────────────────────
export interface ProjectMeta {
  project_id: string
  name: string
  genre: string
  sub_genre: string[]
  status: "drafting" | "revising" | "completed" | "suspended"
  writing: {
    pov: string
    target_word_count: number
    current_word_count: number
    chapter_count: number
    update_frequency: string
  }
  style: { template: string; prose: string[]; strength: string[]; notes: string }
  created: string
  updated: string
}

export interface ProjectState {
  project: { name: string; genre: string; created: string; updated: string }
  protagonist: string
  ingestion: { status: string; brief_file: string; source_draft: string }
  plot: { structure: string }
  current_focus: string
}

export interface ProjectListItem {
  name: string
  path: string
  genre: string
  status: string
  chapter_count: number
  word_count: number
  updated: string
  is_current: boolean
}

// ── Character ────────────────────────────────────────────
export interface CharacterEntry {
  name: string
  role: "protagonist" | "supporting" | "minor" | "antagonist"
  archetype: string
  file: string
  first_appearance: string
  affiliation: string[]
  scene_count: number
}

export interface Character {
  name: string
  aliases: string[]
  role: string
  archetype: string
  narrative_function: string
  first_appearance: string
  profile: {
    age: string
    gender: string
    occupation: string
    affiliation: string[]
    location: string
  }
  traits: string[]
  moral_spectrum: string
  fatal_flaw: string
  obsession: string
  soft_spot: string
  misbelief: string
  contrast_habit: string
  tragedy_trigger: string
  appearance: string
  backstory: string
  speech_pattern: string
  abilities: { name: string; description: string }[]
  arc: { stage: string; state: string; chapter: number; moment_type: string }[]
  relations: {
    character: string
    type: string
    description: string
    dynamic: string
    tension_source: string
  }[]
  cross_references: {
    related_settings: { id: string; name: string; relevance: string }[]
    related_factions: { id: string; name: string; stance: string }[]
    key_chapters: number[]
  }
  notes: string
  created: string
  updated: string
}

// ── Worldbuilding ────────────────────────────────────────
export interface WorldbuildingIndex {
  core_concepts: { name: string; one_liner: string; entry_id: string }[]
  power_system: { name: string; type: string; entry_ids: string[]; summary: string }
  factions_summary: { name: string; stance: string; entry_id: string }[]
  entries: { id: string; name: string; category: string; status: string; file: string }[]
}

export interface Setting {
  id: string
  name: string
  category: string
  status: "tentative" | "confirmed" | "deprecated"
  summary: string
  description: string
  rules: string[]
  constraints: string[]
  plot_links: { node: string; role: string }[]
  character_links: { character: string; relation: string }[]
  setting_links: { target_id: string; relation: string; note: string }[]
  open_questions: string[]
  source: string
  created: string
  updated: string
}

// ── Chapter ──────────────────────────────────────────────
export type ChapterStatus = "idea" | "outline" | "draft" | "revise" | "final" | "published"

export interface ChapterMeta {
  id: string
  title: string
  status: ChapterStatus
  pov: string
  goal: string
  word_target: number
  word_actual: number
  hooks_planted: string[]
  hooks_revealed: string[]
  updated: string
  summary: string
  characters_involved: string[]
}

export interface ChapterContent {
  meta: ChapterMeta
  content: string
}

// ── Plot ─────────────────────────────────────────────────
export interface PlotOutline {
  markdown: string
  structured: {
    premise: string
    theme: string[]
    tone: string[]
    structure: { act: string; chapters: string; arc: string; pacing: string }[]
    foreshadowing: {
      id: string
      description: string
      plant_chapter: string
      payoff_chapter: string
      confidence: string
    }[]
    pacing_curve: { chapter: string; tension: number; note: string }[]
  } | null
}

// ── Timeline ─────────────────────────────────────────────
export interface TimelineEvent {
  time: string
  event: string
  chapter?: string
  location?: string
  characters?: string[]
  type?: string
}

// ── Relationships ────────────────────────────────────────
export interface Relationship {
  pair: [string, string]
  type: string
  dynamic: string
  tension_source: string
  strength: number
  last_updated: string
}

export interface RelationEvent {
  characters: [string, string]
  chapter: string
  change: string
  type: string
  cause: string
  cost: string
  reversible: boolean
  date: string
}

// ── Compliance ───────────────────────────────────────────
export interface InspirationEntry {
  chapter_id: string
  material_id: string
  dimensions: string[]
  note: string
  date: string
}

export interface RiskEntry {
  chapter_id: string
  level: "low" | "medium" | "high"
  issues: string[]
  suggestions: string[]
  checked_at: string
}

// ── Quality ──────────────────────────────────────────────
export interface AITraceReport {
  chapter_id: string
  score: number
  grade: string
  dimensions: Record<string, number>
  top_issues: string[]
  checked_at: string
}

// ── LLM ──────────────────────────────────────────────────
export interface LLMConfig {
  api_url: string
  api_token: string
  model: string
  temperature: number
  max_tokens: number
}

// ── Skills ───────────────────────────────────────────────
export interface SkillInfo {
  name: string
  description: string
  category: string
}

export interface SkillMessage {
  role: "user" | "assistant" | "system"
  content: string
}
