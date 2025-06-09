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
  const [discountError, setDiscountError] = useState("")
  const [skuError, setSkuError] = useState("")

  // Format number as currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
    }).format(value)
  }

  const searchDiscountCode = async () => {
    if (!discountCode.trim()) return

    setIsLoadingDiscount(true)
    setDiscountError("")

    try {
      console.log("Searching for discount code:", discountCode)

      // Fetch discount revenue
      const revenueResponse = await fetch(`http://localhost:5000/insights/shopify/discount-revenue`)
      const revenueData = await revenueResponse.json()
      console.log("Revenue response:", revenueData)

      // Fetch discount order count
      const orderCountResponse = await fetch(`http://localhost:5000/insights/shopify/discount-order-count`)
      const orderCountData = await orderCountResponse.json()
      console.log("Order count response:", orderCountData)

      if (revenueResponse.ok && orderCountResponse.ok) {
        // Check if the discount code exists in the response
        if (revenueData.data && discountCode in revenueData.data) {
          const revenue = revenueData.data[discountCode]
          setDiscountRevenue(formatCurrency(revenue))
          setDiscountError("")
        } else {
          setDiscountRevenue("$0")
          setDiscountError("Discount code not found")
        }

        // Check if the discount code exists in the order count response
        if (orderCountData.data && discountCode in orderCountData.data) {
          const orderCount = orderCountData.data[discountCode]
          setDiscountItems(orderCount.toString())
        } else {
          setDiscountItems("0")
        }
      } else {
        console.error(
          "API error - Revenue status:",
          revenueResponse.status,
          "Order count status:",
          orderCountResponse.status,
        )
        setDiscountRevenue("$0")
        setDiscountItems("0")
        setDiscountError("Failed to fetch discount data")
      }
    } catch (error) {
      console.error("Error fetching discount data:", error)
      setDiscountRevenue("$0")
      setDiscountItems("0")
      setDiscountError("Network error")
    } finally {
      setIsLoadingDiscount(false)
    }
  }

  const searchSkuNumber = async () => {
    if (!skuNumber.trim()) return

    setIsLoadingSku(true)
    setSkuError("")

    try {
      console.log("Searching for SKU:", skuNumber)

      // Fetch SKU revenue data
      const revenueResponse = await fetch(`http://localhost:5000/insights/shopify/sku-revenue`)

      // Fetch SKU order count data
      const orderCountResponse = await fetch(`http://localhost:5000/insights/shopify/sku-order-count`)

      if (!revenueResponse.ok || !orderCountResponse.ok) {
        throw new Error(
          `HTTP error! Revenue status: ${revenueResponse.status}, Order count status: ${orderCountResponse.status}`,
        )
      }

      const revenueData = await revenueResponse.json()
      const orderCountData = await orderCountResponse.json()

      console.log("SKU Revenue data:", revenueData)
      console.log("SKU Order count data:", orderCountData)

      // Check if the SKU exists in the revenue data
      if (revenueData.data && skuNumber in revenueData.data) {
        const revenue = revenueData.data[skuNumber]
        console.log("Found revenue for SKU:", revenue)
        setSkuRevenue(formatCurrency(revenue))
        setSkuError("")
      } else {
        console.log("SKU not found in revenue data")
        setSkuRevenue("$0")
        setSkuError("SKU not found")
      }

      // Check if the SKU exists in the order count data
      if (orderCountData.data && skuNumber in orderCountData.data) {
        const orderCount = orderCountData.data[skuNumber]
        console.log("Found order count for SKU:", orderCount)
        setSkuOrders(orderCount.toString())
      } else {
        console.log("SKU not found in order count data")
        setSkuOrders("0")
      }
    } catch (error) {
      console.error("Error fetching SKU data:", error)
      setSkuRevenue("$0")
      setSkuOrders("0")
      setSkuError("Network error")
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
          {discountError ? (
            <p className="text-xs text-red-500">{discountError}</p>
          ) : (
            <p className="text-xs text-muted-foreground">
              {discountCode ? `Code: ${discountCode}` : "Enter code to search"}
            </p>
          )}
        </CardContent>
      </Card>

      {/* Discount Code Items Ordered */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Discount Code Orders</CardTitle>
          <Tag className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-center text-sm text-muted-foreground mb-2">Search using the Revenue card</div>
          <div className="text-2xl font-bold">{isLoadingDiscount ? "Loading..." : discountItems}</div>
          <p className="text-xs text-muted-foreground">
            {discountCode ? `Code: ${discountCode}` : "Enter code in Revenue card"}
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
          {skuError ? (
            <p className="text-xs text-red-500">{skuError}</p>
          ) : (
            <p className="text-xs text-muted-foreground">{skuNumber ? `SKU: ${skuNumber}` : "Enter SKU to search"}</p>
          )}
        </CardContent>
      </Card>

      {/* SKU Orders */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">SKU Orders</CardTitle>
          <ShoppingCart className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-center text-sm text-muted-foreground mb-2">Search using the Revenue card</div>
          <div className="text-2xl font-bold">{isLoadingSku ? "Loading..." : skuOrders}</div>
          <p className="text-xs text-muted-foreground">
            {skuNumber ? `SKU: ${skuNumber}` : "Enter SKU in Revenue card"}
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
