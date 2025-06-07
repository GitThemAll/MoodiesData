"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Icons } from "@/components/icons"

export default function SettingsPage() {
  const [isLoading, setIsLoading] = useState(false)

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      setIsLoading(false)
      alert("Profile updated successfully!")
    }, 1000)
  }

  const handleSaveTokens = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      setIsLoading(false)
      alert("API tokens updated successfully!")
    }, 1000)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">Manage your account settings and API integrations.</p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile Information</CardTitle>
            <CardDescription>Update your personal information and account details.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSaveProfile} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input id="firstName" defaultValue="John" placeholder="Enter your first name" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input id="lastName" defaultValue="Doe" placeholder="Enter your last name" />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" defaultValue="john@example.com" placeholder="Enter your email" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Company</Label>
                <Input id="company" defaultValue="Acme Inc." placeholder="Enter your company name" />
              </div>
              <Button type="submit" disabled={isLoading}>
                {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
                Save Profile
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>API Integrations</CardTitle>
            <CardDescription>Configure your API tokens for Klaviyo and Shopify integrations.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSaveTokens} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="klaviyoToken" className="text-base font-medium">
                    Klaviyo API Token
                  </Label>
                  <p className="text-sm text-muted-foreground mb-2">
                    Enter your Klaviyo private API key to sync customer data.
                  </p>
                  <Input id="klaviyoToken" type="password" placeholder="pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" />
                </div>

                <Separator />

                <div>
                  <Label htmlFor="shopifyToken" className="text-base font-medium">
                    Shopify API Token
                  </Label>
                  <p className="text-sm text-muted-foreground mb-2">Enter your Shopify Admin API access token.</p>
                  <Input id="shopifyToken" type="password" placeholder="shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" />
                </div>

                <div>
                  <Label htmlFor="shopifyStore" className="text-base font-medium">
                    Shopify Store URL
                  </Label>
                  <p className="text-sm text-muted-foreground mb-2">
                    Enter your Shopify store URL (e.g., your-store.myshopify.com).
                  </p>
                  <Input id="shopifyStore" placeholder="your-store.myshopify.com" />
                </div>
              </div>

              <Button type="submit" disabled={isLoading}>
                {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
                Save API Tokens
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
