import { useState, useEffect } from "react"
import { Save, TestTube, CheckCircle2, XCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useAppStore } from "@/stores/app-store"
import { llm } from "@/services/api"
import { toast } from "sonner"

export default function Settings() {
  const { llmConfig, setLLMConfig, darkMode, toggleDarkMode } = useAppStore()
  const [form, setForm] = useState(llmConfig)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState<"success" | "error" | null>(null)

  useEffect(() => { setForm(llmConfig) }, [llmConfig])

  const handleSave = async () => {
    setLLMConfig(form)
    try {
      await llm.setConfig(form)
      toast.success("LLM 配置已保存")
    } catch {
      toast.success("本地配置已保存（后端未连接）")
    }
  }

  const handleTest = async () => {
    if (!form.api_url || !form.api_token) {
      toast.error("请先填写 API URL 和 Token")
      return
    }
    setLLMConfig(form)
    try { await llm.setConfig(form) } catch { /* backend might be offline */ }

    setTesting(true)
    setTestResult(null)
    try {
      const res = await llm.chat([{ role: "user", content: "Hi, respond with just 'ok'" }])
      if (res.ok) {
        setTestResult("success")
        toast.success("连接成功")
      } else {
        const body = await res.text().catch(() => res.statusText)
        setTestResult("error")
        toast.error("连接失败: " + body)
      }
    } catch (e: unknown) {
      setTestResult("error")
      toast.error("连接失败: " + (e as Error).message)
    } finally {
      setTesting(false)
    }
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">设置</h1>
        <p className="text-muted-foreground">配置 LLM 接入和应用偏好</p>
      </div>

      <Tabs defaultValue="llm">
        <TabsList>
          <TabsTrigger value="llm">LLM 配置</TabsTrigger>
          <TabsTrigger value="appearance">外观</TabsTrigger>
        </TabsList>

        <TabsContent value="llm" className="mt-4 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">大模型接入</CardTitle>
              <CardDescription>配置第三方大模型的 API 地址和密钥，兼容 OpenAI 格式</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="api-url">API URL</Label>
                <Input
                  id="api-url"
                  placeholder="https://api.openai.com/v1/chat/completions"
                  value={form.api_url}
                  onChange={(e) => setForm({ ...form, api_url: e.target.value })}
                />
                <p className="text-xs text-muted-foreground">
                  支持 OpenAI、Anthropic、DeepSeek 等兼容 API
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="api-token">API Token</Label>
                <Input
                  id="api-token"
                  type="password"
                  placeholder="sk-..."
                  value={form.api_token}
                  onChange={(e) => setForm({ ...form, api_token: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="model">模型名称</Label>
                <Input
                  id="model"
                  placeholder="gpt-4o"
                  value={form.model}
                  onChange={(e) => setForm({ ...form, model: e.target.value })}
                />
              </div>

              <Separator />

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="temperature">Temperature</Label>
                  <Input
                    id="temperature"
                    type="number"
                    min={0}
                    max={2}
                    step={0.1}
                    value={form.temperature}
                    onChange={(e) => setForm({ ...form, temperature: parseFloat(e.target.value) || 0 })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="max-tokens">Max Tokens</Label>
                  <Input
                    id="max-tokens"
                    type="number"
                    min={256}
                    max={128000}
                    step={256}
                    value={form.max_tokens}
                    onChange={(e) => setForm({ ...form, max_tokens: parseInt(e.target.value) || 4096 })}
                  />
                </div>
              </div>

              <div className="flex items-center gap-3 pt-2">
                <Button onClick={handleSave}>
                  <Save className="mr-2 h-4 w-4" />
                  保存配置
                </Button>
                <Button variant="outline" onClick={handleTest} disabled={testing}>
                  <TestTube className="mr-2 h-4 w-4" />
                  {testing ? "测试中..." : "测试连接"}
                </Button>
                {testResult === "success" && <CheckCircle2 className="h-5 w-5 text-emerald-500" />}
                {testResult === "error" && <XCircle className="h-5 w-5 text-red-500" />}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="appearance" className="mt-4 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">外观</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>深色模式</Label>
                  <p className="text-xs text-muted-foreground">切换深色/浅色主题</p>
                </div>
                <Switch checked={darkMode} onCheckedChange={toggleDarkMode} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
