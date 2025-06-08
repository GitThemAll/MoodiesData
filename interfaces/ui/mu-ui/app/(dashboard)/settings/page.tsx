"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Icons } from "@/components/icons"

export default function SettingsPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [userData, setUserData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    company: "",
  })

  useEffect(() => {
    // Get user data from localStorage
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser)
        console.log("Stored user data:", parsedUser) // Debug log

        // Check if the data is nested under 'user' key or direct
        const userObj = parsedUser.user || parsedUser

        // Extract first and last name from username if available
        let firstName = ""
        let lastName = ""

        if (userObj.username) {
          const nameParts = userObj.username.split(" ")
          firstName = nameParts[0] || ""
          lastName = nameParts.length > 1 ? nameParts.slice(1).join(" ") : ""
        }

        // Correctly extract email from the user object
        const email = userObj.email || ""

        console.log("Extracted email:", email) // Debug log

        setUserData({
          firstName,
          lastName,
          email,
          company: userObj.company || "",
        })
      } catch (error) {
        console.error("Failed to parse user data:", error)
      }
    }
  }, [])

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      // Update localStorage with new values
      try {
        const storedUser = localStorage.getItem("user")
        if (storedUser) {
          const parsedUser = JSON.parse(storedUser)
          const userObj = parsedUser.user || parsedUser

          const updatedUser = {
            ...userObj,
            username: `${userData.firstName} ${userData.lastName}`.trim(),
            email: userData.email,
            company: userData.company,
          }

          // Store back in the same structure
          if (parsedUser.user) {
            localStorage.setItem("user", JSON.stringify({ ...parsedUser, user: updatedUser }))
          } else {
            localStorage.setItem("user", JSON.stringify(updatedUser))
          }
        }
      } catch (error) {
        console.error("Failed to update user data:", error)
      }

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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target
    setUserData((prev) => ({
      ...prev,
      [id]: value,
    }))
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
                  <Input
                    id="firstName"
                    value={userData.firstName}
                    onChange={handleInputChange}
                    placeholder="Enter your first name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    value={userData.lastName}
                    onChange={handleInputChange}
                    placeholder="Enter your last name"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={userData.email}
                  onChange={handleInputChange}
                  placeholder="Enter your email"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Company</Label>
                <Input
                  id="company"
                  value={userData.company}
                  onChange={handleInputChange}
                  placeholder="Enter your company name"
                />
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
