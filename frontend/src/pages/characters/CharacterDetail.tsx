import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { ArrowLeft, Edit, Save, X, Sparkles } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useFetch } from "@/hooks/use-fetch"
import { characters } from "@/services/api"
import { toast } from "sonner"
import type { Character } from "@/types"

function EditField({ label, value, onChange, multiline }: {
  label: string; value: string; onChange: (v: string) => void; multiline?: boolean
}) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs">{label}</Label>
      {multiline ? (
        <Textarea value={value} onChange={(e) => onChange(e.target.value)} className="text-sm min-h-[80px]" />
      ) : (
        <Input value={value} onChange={(e) => onChange(e.target.value)} className="text-sm h-8" />
      )}
    </div>
  )
}

export default function CharacterDetail() {
  const { name } = useParams<{ name: string }>()
  const navigate = useNavigate()
  const { data: char, loading, refetch } = useFetch(
    () => characters.get(decodeURIComponent(name!)),
    [name],
  )
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState<Partial<Character>>({})
  const [saving, setSaving] = useState(false)

  const startEdit = () => {
    if (!char) return
    setForm({
      ...char,
      profile: { ...char.profile },
      traits: [...(char.traits || [])],
    })
    setEditing(true)
  }

  const cancelEdit = () => {
    setEditing(false)
    setForm({})
  }

  const handleSave = async () => {
    if (!name || !form.name) return
    setSaving(true)
    try {
      await characters.update(decodeURIComponent(name), form)
      toast.success("角色已更新")
      setEditing(false)
      refetch()
    } catch (e: unknown) {
      toast.error("保存失败: " + (e as Error).message)
    } finally {
      setSaving(false)
    }
  }

  const updateProfile = (key: string, value: string) => {
    setForm((prev) => ({
      ...prev,
      profile: { ...(prev.profile || {} as Character["profile"]), [key]: value },
    }))
  }

  if (loading) {
    return <div className="space-y-4">{[1, 2, 3].map((i) => <Card key={i} className="h-40 animate-pulse bg-muted" />)}</div>
  }

  if (!char) {
    return <div className="text-center py-12 text-muted-foreground">角色未找到</div>
  }

  const display = editing ? form as Character : char

  const fivePieces = [
    { label: "致命缺陷", key: "fatal_flaw" as const, color: "text-red-500" },
    { label: "执念", key: "obsession" as const, color: "text-amber-500" },
    { label: "软肋", key: "soft_spot" as const, color: "text-pink-500" },
    { label: "误判", key: "misbelief" as const, color: "text-purple-500" },
    { label: "反差习惯", key: "contrast_habit" as const, color: "text-blue-500" },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/characters")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{display.name}</h1>
            <Badge variant="outline">{display.role}</Badge>
            {display.archetype && <Badge variant="secondary">{display.archetype}</Badge>}
          </div>
          <p className="text-muted-foreground">{display.narrative_function}</p>
        </div>
        <div className="flex gap-2">
          {editing ? (
            <>
              <Button variant="ghost" size="sm" onClick={cancelEdit}>
                <X className="mr-2 h-4 w-4" />取消
              </Button>
              <Button size="sm" onClick={handleSave} disabled={saving}>
                <Save className="mr-2 h-4 w-4" />{saving ? "保存中..." : "保存"}
              </Button>
            </>
          ) : (
            <>
              <Button variant="outline" size="sm" onClick={startEdit}>
                <Edit className="mr-2 h-4 w-4" />编辑
              </Button>
              <Button variant="outline" size="sm" onClick={() => navigate("/skills")}>
                <Sparkles className="mr-2 h-4 w-4" />AI 分析
              </Button>
            </>
          )}
        </div>
      </div>

      <Tabs defaultValue="profile">
        <TabsList>
          <TabsTrigger value="profile">基本信息</TabsTrigger>
          <TabsTrigger value="psychology">心理画像</TabsTrigger>
          <TabsTrigger value="arc">角色弧光</TabsTrigger>
          <TabsTrigger value="relations">关系</TabsTrigger>
        </TabsList>

        {/* ── 基本信息 ── */}
        <TabsContent value="profile" className="space-y-4 mt-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader><CardTitle className="text-base">档案</CardTitle></CardHeader>
              <CardContent className="space-y-2 text-sm">
                {editing ? (
                  <div className="space-y-3">
                    <EditField label="年龄" value={form.profile?.age ?? ""} onChange={(v) => updateProfile("age", v)} />
                    <EditField label="性别" value={form.profile?.gender ?? ""} onChange={(v) => updateProfile("gender", v)} />
                    <EditField label="职业" value={form.profile?.occupation ?? ""} onChange={(v) => updateProfile("occupation", v)} />
                    <EditField label="所在地" value={form.profile?.location ?? ""} onChange={(v) => updateProfile("location", v)} />
                    <EditField label="初登场" value={form.first_appearance ?? ""} onChange={(v) => setForm({ ...form, first_appearance: v })} />
                    <EditField label="原型" value={form.archetype ?? ""} onChange={(v) => setForm({ ...form, archetype: v })} />
                  </div>
                ) : (
                  <>
                    {[
                      ["年龄", display.profile?.age],
                      ["性别", display.profile?.gender],
                      ["职业", display.profile?.occupation],
                      ["所在地", display.profile?.location],
                      ["初登场", display.first_appearance],
                    ].map(([k, v]) => v ? (
                      <div key={k as string} className="flex justify-between">
                        <span className="text-muted-foreground">{k}</span>
                        <span>{v as string}</span>
                      </div>
                    ) : null)}
                    {display.profile?.affiliation?.length > 0 && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">阵营</span>
                        <div className="flex gap-1">{display.profile.affiliation.map((a) => <Badge key={a} variant="outline" className="text-xs">{a}</Badge>)}</div>
                      </div>
                    )}
                  </>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader><CardTitle className="text-base">外貌</CardTitle></CardHeader>
              <CardContent>
                {editing ? (
                  <EditField label="" value={form.appearance ?? ""} onChange={(v) => setForm({ ...form, appearance: v })} multiline />
                ) : (
                  <p className="text-sm">{display.appearance || "暂无描述"}</p>
                )}
              </CardContent>
            </Card>

            <Card className="md:col-span-2">
              <CardHeader><CardTitle className="text-base">背景故事</CardTitle></CardHeader>
              <CardContent>
                {editing ? (
                  <EditField label="" value={form.backstory ?? ""} onChange={(v) => setForm({ ...form, backstory: v })} multiline />
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{display.backstory || "暂无"}</p>
                )}
              </CardContent>
            </Card>

            {(display.abilities?.length > 0 || editing) && (
              <Card className="md:col-span-2">
                <CardHeader><CardTitle className="text-base">能力</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                  {display.abilities?.map((a, i) => (
                    <div key={i}>
                      <div className="font-medium text-sm">{a.name}</div>
                      <div className="text-sm text-muted-foreground">{a.description}</div>
                    </div>
                  ))}
                  {!display.abilities?.length && <p className="text-sm text-muted-foreground">暂无</p>}
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>

        {/* ── 心理画像 ── */}
        <TabsContent value="psychology" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">五件套</CardTitle></CardHeader>
            <CardContent className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {fivePieces.map((p) => (
                <div key={p.label} className="rounded-lg border p-4">
                  <div className={`text-xs font-semibold uppercase ${p.color}`}>{p.label}</div>
                  {editing ? (
                    <Textarea
                      value={(form as Record<string, unknown>)[p.key] as string ?? ""}
                      onChange={(e) => setForm({ ...form, [p.key]: e.target.value })}
                      className="mt-1 text-sm min-h-[60px]"
                    />
                  ) : (
                    <div className="mt-1 text-sm">{(display as Record<string, unknown>)[p.key] as string || "—"}</div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader><CardTitle className="text-base">性格特征</CardTitle></CardHeader>
              <CardContent>
                {editing ? (
                  <EditField label="逗号分隔" value={(form.traits || []).join(", ")} onChange={(v) => setForm({ ...form, traits: v.split(/[,，]/).map((s) => s.trim()).filter(Boolean) })} />
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {display.traits?.map((t) => <Badge key={t} variant="secondary">{t}</Badge>)}
                    {!display.traits?.length && <span className="text-sm text-muted-foreground">暂无</span>}
                  </div>
                )}
                {editing ? (
                  <div className="mt-3">
                    <EditField label="道德光谱" value={form.moral_spectrum ?? ""} onChange={(v) => setForm({ ...form, moral_spectrum: v })} />
                  </div>
                ) : display.moral_spectrum ? (
                  <div className="mt-3 text-sm"><span className="text-muted-foreground">道德光谱: </span>{display.moral_spectrum}</div>
                ) : null}
              </CardContent>
            </Card>

            <Card>
              <CardHeader><CardTitle className="text-base">语言模式</CardTitle></CardHeader>
              <CardContent>
                {editing ? (
                  <EditField label="" value={form.speech_pattern ?? ""} onChange={(v) => setForm({ ...form, speech_pattern: v })} multiline />
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{display.speech_pattern || "暂无"}</p>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* ── 角色弧光 ── */}
        <TabsContent value="arc" className="mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">角色弧光</CardTitle></CardHeader>
            <CardContent>
              {display.arc?.length > 0 ? (
                <div className="relative">
                  <div className="absolute left-4 top-0 bottom-0 w-px bg-border" />
                  <div className="space-y-6">
                    {display.arc.map((a, i) => (
                      <div key={i} className="relative pl-10">
                        <div className="absolute left-2.5 top-1 h-3 w-3 rounded-full border-2 border-primary bg-background" />
                        <div className="font-medium text-sm">{a.stage}</div>
                        <div className="text-sm text-muted-foreground">{a.state}</div>
                        <div className="text-xs text-muted-foreground mt-1">
                          第 {a.chapter} 章 · {a.moment_type}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">暂无弧光数据</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* ── 关系 ── */}
        <TabsContent value="relations" className="mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">人物关系</CardTitle></CardHeader>
            <CardContent>
              {display.relations?.length > 0 ? (
                <div className="space-y-4">
                  {display.relations.map((r, i) => (
                    <div key={i} className="flex items-start gap-4 p-3 rounded-lg border">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 font-bold text-sm">
                        {r.character[0]}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-medium cursor-pointer hover:text-primary" onClick={() => navigate(`/characters/${encodeURIComponent(r.character)}`)}>
                            {r.character}
                          </span>
                          <Badge variant="outline">{r.type}</Badge>
                        </div>
                        <p className="text-sm text-muted-foreground mt-1">{r.description}</p>
                        {r.dynamic && <p className="text-xs text-muted-foreground mt-0.5">动态: {r.dynamic}</p>}
                        {r.tension_source && <p className="text-xs text-amber-500 mt-0.5">张力: {r.tension_source}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">暂无关系数据</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
