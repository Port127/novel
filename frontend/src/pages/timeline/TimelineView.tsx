import { useNavigate } from "react-router-dom"
import { Plus, Clock, MapPin, Users } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { useFetch } from "@/hooks/use-fetch"
import { timeline } from "@/services/api"

export default function TimelineView() {
  const navigate = useNavigate()
  const { data: events, loading } = useFetch(() => timeline.list())

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">时间线</h1>
          <p className="text-muted-foreground">{events?.length ?? 0} 个事件</p>
        </div>
        <Button onClick={() => navigate("/skills")}>
          <Plus className="mr-2 h-4 w-4" />
          添加事件
        </Button>
      </div>

      {loading ? (
        <div className="space-y-4">{[1, 2, 3].map((i) => <Card key={i} className="h-20 animate-pulse bg-muted" />)}</div>
      ) : events && events.length > 0 ? (
        <ScrollArea className="h-[calc(100vh-14rem)]">
          <div className="relative pl-8">
            <div className="absolute left-3 top-0 bottom-0 w-px bg-border" />
            <div className="space-y-6">
              {events.map((evt, i) => (
                <div key={i} className="relative">
                  <div className="absolute -left-5 top-2 h-3 w-3 rounded-full border-2 border-primary bg-background" />
                  <Card>
                    <CardContent className="pt-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <Clock className="h-3.5 w-3.5 text-muted-foreground" />
                            <span className="text-sm font-medium">{evt.time}</span>
                            {evt.chapter && <Badge variant="outline" className="text-xs">{evt.chapter}</Badge>}
                          </div>
                          <p className="text-sm">{evt.event}</p>
                          <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                            {evt.location && (
                              <span className="flex items-center gap-1">
                                <MapPin className="h-3 w-3" />{evt.location}
                              </span>
                            )}
                            {evt.characters && evt.characters.length > 0 && (
                              <span className="flex items-center gap-1">
                                <Users className="h-3 w-3" />{evt.characters.join(", ")}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ))}
            </div>
          </div>
        </ScrollArea>
      ) : (
        <div className="text-center py-16 text-muted-foreground">
          暂无时间线事件，使用 AI 助手添加
        </div>
      )}
    </div>
  )
}
