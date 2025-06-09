"use client"

import { useState, useEffect } from "react"
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

  const [allDiscountRevenue, setAllDiscountRevenue] = useState<{ [key: string]: number }>({})
  const [allDiscountOrders, setAllDiscountOrders] = useState<{ [key: string]: number }>({})
  const [allSkuRevenue, setAllSkuRevenue] = useState<{ [key: string]: number }>({})
  const [allSkuOrders, setAllSkuOrders] = useState<{ [key: string]: number }>({})

  useEffect(() => {
    fetchAllData()
  }, [])

  const fetchAllData = async () => {
    try {
      // Fetch all discount data
      const [discountRevenueRes, discountOrdersRes, skuRevenueRes, skuOrdersRes] = await Promise.all([
        fetch("http://localhost:5000/insights/shopify/discount-revenue"),
        fetch("http://localhost:5000/insights/shopify/discount-order-count"),
        fetch("http://localhost:5000/insights/shopify/sku-revenue"),
        fetch("http://localhost:5000/insights/shopify/sku-order-count"),
      ])

      const [discountRevenueData, discountOrdersData, skuRevenueData, skuOrdersData] = await Promise.all([
        discountRevenueRes.json(),
        discountOrdersRes.json(),
        skuRevenueRes.json(),
        skuOrdersRes.json(),
      ])

      setAllDiscountRevenue(discountRevenueData.data || {})
      setAllDiscountOrders(discountOrdersData.data || {})
      setAllSkuRevenue(skuRevenueData.data || {})
      setAllSkuOrders(skuOrdersData.data || {})
    } catch (error) {
      console.error("Error fetching all data:", error)
    }
  }

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

    // Use cached data instead of API call
    if (discountCode in allDiscountRevenue) {
      const revenue = allDiscountRevenue[discountCode]
      setDiscountRevenue(formatCurrency(revenue))
      setDiscountError("")
    } else {
      setDiscountRevenue("$0")
      setDiscountError("Discount code not found")
    }

    if (discountCode in allDiscountOrders) {
      const orderCount = allDiscountOrders[discountCode]
      setDiscountItems(orderCount.toString())
    } else {
      setDiscountItems("0")
    }

    setIsLoadingDiscount(false)
  }

  const searchSkuNumber = async () => {
    if (!skuNumber.trim()) return

    setIsLoadingSku(true)
    setSkuError("")

    // Use cached data instead of API call
    if (skuNumber in allSkuRevenue) {
      const revenue = allSkuRevenue[skuNumber]
      setSkuRevenue(formatCurrency(revenue))
      setSkuError("")
    } else {
      setSkuRevenue("$0")
      setSkuError("SKU not found")
    }

    if (skuNumber in allSkuOrders) {
      const orderCount = allSkuOrders[skuNumber]
      setSkuOrders(orderCount.toString())
    } else {
      setSkuOrders("0")
    }

    setIsLoadingSku(false)
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
