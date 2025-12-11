"use client"

import * as React from "react"
import {
  BookOpen,
  Brain,
  LayoutDashboard,
  LifeBuoy,
  MessageSquare,
  Send,
  Settings2,
} from "lucide-react"
import type { User } from "@supabase/supabase-js"
import Link from "next/link"

import { NavMain } from "@/components/nav-main"
import { NavSecondary } from "@/components/nav-secondary"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const navDashboard = [
  {
    title: "Dashboard",
    url: "/",
    icon: LayoutDashboard,
  },
]

const navMain = [
  {
    title: "Chat",
    url: "/chat",
    icon: MessageSquare,
    isActive: true,
  },
  {
    title: "Knowledge",
    url: "/knowledge",
    icon: Brain,
    items: [
      {
        title: "Dashboard",
        url: "/knowledge",
      },
      {
        title: "Documents",
        url: "/knowledge/documents",
      },
      {
        title: "Graph",
        url: "/knowledge/graph",
      },
      {
        title: "Search",
        url: "/knowledge/search",
      },
    ],
  },
  {
    title: "Settings",
    url: "/knowledge/settings",
    icon: Settings2,
    items: [
      {
        title: "General",
        url: "/knowledge/settings",
      },
      {
        title: "Embeddings",
        url: "/knowledge/settings/embeddings",
      },
      {
        title: "Chunking",
        url: "/knowledge/settings/chunking",
      },
      {
        title: "Stores",
        url: "/knowledge/settings/stores",
      },
    ],
  },
]

const navSecondary = [
  {
    title: "Documentation",
    url: "/docs",
    icon: BookOpen,
  },
  {
    title: "Support",
    url: "#",
    icon: LifeBuoy,
  },
  {
    title: "Feedback",
    url: "#",
    icon: Send,
  },
]

interface AppSidebarProps extends React.ComponentProps<typeof Sidebar> {
  user: User
}

export function AppSidebar({ user, ...props }: AppSidebarProps) {
  const userData = {
    name: user.user_metadata?.full_name || user.email?.split("@")[0] || "User",
    email: user.email || "",
    avatar: user.user_metadata?.avatar_url || "",
  }

  return (
    <Sidebar variant="inset" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link href="/">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Brain className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Piragi</span>
                  <span className="truncate text-xs">RAG Platform</span>
                </div>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navDashboard} label="Home" />
        <NavMain items={navMain} />
        <NavSecondary items={navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={userData} />
      </SidebarFooter>
    </Sidebar>
  )
}
