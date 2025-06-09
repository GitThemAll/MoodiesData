"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, DollarSign, ShoppingCart, Tag } from "lucide-react"

export function MetricCards() {
  const [discountCode, setDiscountCode] = useState("")
  const [skuNumber, setSkuNumber] = useState("")
  const [discountRevenue, setDiscountRevenue] = useState("$0")
  const [discountItems, setDiscountItems] = useState("0")
  const [skuRevenue, setSkuRevenue] = useState("$0")
  const [skuOrders, setSkuOrders] = useState("0")
  const [isLoadingDiscount, setIsLoadingDiscount] = useState(false)
  const [isLoadingSku, setIsLoadingSku] = useState(false)

  const searchDiscountCode = async () => {
    if (!discountCode.trim()) return

    setIsLoadingDiscount(true)
    try {
      // Simulate API call - replace with your actual API endpoint
      const response = await fetch(`http://localhost:5000/insights/discount/${discountCode}`)
      const data = await response.json()

      if (response.ok) {
        setDiscountRevenue(data.revenue || "$0")
        setDiscountItems(data.items || "0")
      } else {
        setDiscountRevenue("$0")
        setDiscountItems("0")
      }
    } catch (error) {
      console.error("Error fetching discount data:", error)
      setDiscountRevenue("$0")
      setDiscountItems("0")
    } finally {
      setIsLoadingDiscount(false)
    }
  }

  const searchSkuNumber = async () => {
    if (!skuNumber.trim()) return

    setIsLoadingSku(true)
    try {
      // Simulate API call - replace with your actual API endpoint
      const response = await fetch(`http://localhost:5000/insights/sku/${skuNumber}`)
      const data = await response.json()

      if (response.ok) {
        setSkuRevenue(data.revenue || "$0")
        setSkuOrders(data.orders || "0")
      } else {
        setSkuRevenue("$0")
        setSkuOrders("0")
      }
    } catch (error) {
      console.error("Error fetching SKU data:", error)
      setSkuRevenue("$0")
      setSkuOrders("0")
    } finally {
      setIsLoadingSku(false)
    }
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {/* Discount Code Revenue */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Discount Code Revenue</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Input
              placeholder="Enter discount code"
              value={discountCode}
              onChange={(e) => setDiscountCode(e.target.value)}
              className="text-xs"
              onKeyPress={(e) => e.key === "Enter" && searchDiscountCode()}
            />
            <Button size="sm" onClick={searchDiscountCode} disabled={isLoadingDiscount}>
              <Search className="h-3 w-3" />
            </Button>
          </div>
          <div className="text-2xl font-bold">{isLoadingDiscount ? "Loading..." : discountRevenue}</div>
          <p className="text-xs text-muted-foreground">
            {discountCode ? `Code: ${discountCode}` : "Enter code to search"}
          </p>
        </CardContent>
      </Card>

      {/* Discount Code Items Ordered */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Discount Code Items</CardTitle>
          <Tag className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Input
              placeholder="Enter discount code"
              value={discountCode}
              onChange={(e) => setDiscountCode(e.target.value)}
              className="text-xs"
              onKeyPress={(e) => e.key === "Enter" && searchDiscountCode()}
            />
            <Button size="sm" onClick={searchDiscountCode} disabled={isLoadingDiscount}>
              <Search className="h-3 w-3" />
            </Button>
          </div>
          <div className="text-2xl font-bold">{isLoadingDiscount ? "Loading..." : discountItems}</div>
          <p className="text-xs text-muted-foreground">
            {discountCode ? `Code: ${discountCode}` : "Enter code to search"}
          </p>
        </CardContent>
      </Card>

      {/* SKU Revenue */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">SKU Revenue</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Input
              placeholder="Enter SKU number"
              value={skuNumber}
              onChange={(e) => setSkuNumber(e.target.value)}
              className="text-xs"
              onKeyPress={(e) => e.key === "Enter" && searchSkuNumber()}
            />
            <Button size="sm" onClick={searchSkuNumber} disabled={isLoadingSku}>
              <Search className="h-3 w-3" />
            </Button>
          </div>
          <div className="text-2xl font-bold">{isLoadingSku ? "Loading..." : skuRevenue}</div>
          <p className="text-xs text-muted-foreground">{skuNumber ? `SKU: ${skuNumber}` : "Enter SKU to search"}</p>
        </CardContent>
      </Card>

      {/* SKU Orders */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">SKU Orders</CardTitle>
          <ShoppingCart className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Input
              placeholder="Enter SKU number"
              value={skuNumber}
              onChange={(e) => setSkuNumber(e.target.value)}
              className="text-xs"
              onKeyPress={(e) => e.key === "Enter" && searchSkuNumber()}
            />
            <Button size="sm" onClick={searchSkuNumber} disabled={isLoadingSku}>
              <Search className="h-3 w-3" />
            </Button>
          </div>
          <div className="text-2xl font-bold">{isLoadingSku ? "Loading..." : skuOrders}</div>
          <p className="text-xs text-muted-foreground">{skuNumber ? `SKU: ${skuNumber}` : "Enter SKU to search"}</p>
        </CardContent>
      </Card>
    </div>
  )
}
