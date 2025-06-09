"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Search, ChevronDown } from "lucide-react"

export function CLVMetrics() {
  const [highestPeriod, setHighestPeriod] = useState("next_month")
  const [avgPeriod, setAvgPeriod] = useState("lifetime")
  const [searchEmail, setSearchEmail] = useState("john@moodies.com")
  const [searchPeriod, setSearchPeriod] = useState("next_3_month")
  const [searchResult, setSearchResult] = useState("€500")
  const [showHighestDropdown, setShowHighestDropdown] = useState(false)
  const [showAvgDropdown, setShowAvgDropdown] = useState(false)
  const [showSearchDropdown, setShowSearchDropdown] = useState(false)

  const periods = [
    { value: "next_month", label: "Next month" },
    { value: "next_3_month", label: "Next 3 month" },
    { value: "lifetime", label: "Lifetime" },
  ]

  const getHighestCLV = () => {
    const values = {
      next_month: "€39",
      next_3_month: "€200",
      lifetime: "€423",
    }
    return values[highestPeriod as keyof typeof values] || "€253"
  }

  const getAvgCLV = () => {
    const values = {
      next_month: "€24",
      next_3_month: "€78",
      lifetime: "€265",
    }
    return values[avgPeriod as keyof typeof values] || "€120"
  }

  const handleSearch = () => {
    // Mock search functionality
    const mockResults: { [key: string]: { [key: string]: string } } = {
      "john@moodies.com": {
        next_month: "€15",
        next_3_month: "€45",
        lifetime: "€423",
      },
      "silvia@moodies.com": {
        next_month: "€39",
        next_3_month: "€200",
        lifetime: "€350",
      },
    }

    const email = searchEmail.toLowerCase()
    if (mockResults[email] && mockResults[email][searchPeriod]) {
      setSearchResult(mockResults[email][searchPeriod])
    } else {
      setSearchResult("€0")
    }
  }

  const CustomDropdown = ({
    value,
    onChange,
    options,
    isOpen,
    setIsOpen,
  }: {
    value: string
    onChange: (value: string) => void
    options: { value: string; label: string }[]
    isOpen: boolean
    setIsOpen: (open: boolean) => void
  }) => (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <span>{options.find((opt) => opt.value === value)?.label}</span>
        <ChevronDown className="h-4 w-4 text-gray-400" />
      </button>
      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {options.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => {
                onChange(option.value)
                setIsOpen(false)
              }}
              className="w-full px-3 py-2 text-sm text-left hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
            >
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )

  return (
    <div className="grid gap-6 md:grid-cols-3">
      {/* Highest CLV */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Highest CLV</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="highest-period" className="text-sm font-medium">
              Period
            </Label>
            <CustomDropdown
              value={highestPeriod}
              onChange={setHighestPeriod}
              options={periods}
              isOpen={showHighestDropdown}
              setIsOpen={setShowHighestDropdown}
            />
          </div>

          <div className="text-center space-y-3">
            <div className="text-4xl font-bold">{getHighestCLV()}</div>
            <Button className="bg-green-600 hover:bg-green-700 text-white px-6">Segment</Button>
          </div>
        </CardContent>
      </Card>

      {/* Average CLV */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Avg CLV</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="avg-period" className="text-sm font-medium">
              Period
            </Label>
            <CustomDropdown
              value={avgPeriod}
              onChange={setAvgPeriod}
              options={periods}
              isOpen={showAvgDropdown}
              setIsOpen={setShowAvgDropdown}
            />
          </div>

          <div className="text-center space-y-3">
            <div className="text-4xl font-bold">{getAvgCLV()}</div>
            <Button className="bg-green-600 hover:bg-green-700 text-white px-6">Segment</Button>
          </div>
        </CardContent>
      </Card>

      {/* Search by Email */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Search by email</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="search-email" className="text-sm font-medium">
              Email
            </Label>
            <div className="flex gap-2">
              <Input
                id="search-email"
                value={searchEmail}
                onChange={(e) => setSearchEmail(e.target.value)}
                placeholder="Enter email address"
                className="flex-1"
              />
              <Button size="sm" onClick={handleSearch} variant="outline">
                <Search className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="search-period" className="text-sm font-medium">
              Period
            </Label>
            <CustomDropdown
              value={searchPeriod}
              onChange={setSearchPeriod}
              options={periods}
              isOpen={showSearchDropdown}
              setIsOpen={setShowSearchDropdown}
            />
          </div>

          <div className="text-center space-y-3">
            <div className="text-4xl font-bold">{searchResult}</div>
            <Button className="bg-green-600 hover:bg-green-700 text-white px-6">Segment</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
