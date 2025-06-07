import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const activities = [
  {
    user: "John Smith",
    action: "CLV prediction updated",
    time: "2 minutes ago",
    avatar: "JS",
  },
  {
    user: "Sarah Johnson",
    action: "New customer segment created",
    time: "1 hour ago",
    avatar: "SJ",
  },
  {
    user: "Mike Wilson",
    action: "Purchase prediction completed",
    time: "3 hours ago",
    avatar: "MW",
  },
  {
    user: "Emma Davis",
    action: "Model accuracy improved",
    time: "1 day ago",
    avatar: "ED",
  },
]

export function RecentActivities() {
  return (
    <div className="space-y-4">
      {activities.map((activity, index) => (
        <div key={index} className="flex items-center space-x-4">
          <Avatar className="h-8 w-8">
            <AvatarImage src={`/placeholder.svg?height=32&width=32`} />
            <AvatarFallback>{activity.avatar}</AvatarFallback>
          </Avatar>
          <div className="flex-1 space-y-1">
            <p className="text-sm font-medium leading-none">{activity.user}</p>
            <p className="text-sm text-muted-foreground">{activity.action}</p>
          </div>
          <div className="text-xs text-muted-foreground">{activity.time}</div>
        </div>
      ))}
    </div>
  )
}
