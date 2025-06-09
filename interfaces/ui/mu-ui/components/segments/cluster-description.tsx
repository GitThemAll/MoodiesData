"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"

interface ClusterInfo {
  label: string
  emoji: string
  description: string
  indicators: string[]
  insight: string
}

interface ClusterDescriptionProps {
  onClusterChange?: (clusterId: string) => void
}

const clusterData: { [key: string]: ClusterInfo } = {
  "0": {
    label: "NL Dormant Value Buyers",
    emoji: "🟠",
    description:
      "These are Dutch customers who used to be engaged, with relatively high item counts and purchases, but have been inactive for a long time.",
    indicators: ["Country: Netherlands 🇳🇱", "Payment: iDEAL dominance", "Recent Order: Very stale (~474 days)"],
    insight: "Target with reactivation campaigns and loyalty perks.",
  },
  "1": {
    label: "Low-Intent Pay-Later Shoppers",
    emoji: "🟡",
    description:
      "These customers are price-sensitive and less engaged, likely testing the waters. Many opted for Pay Later and show low purchase volume.",
    indicators: ["Payment: Klarna / Pay Later usage", "Country: Mostly unknown", "Activity: Very low"],
    insight: "Test incentives or educational funnels about product value.",
  },
  "2": {
    label: "Highly Engaged Dutch Customers",
    emoji: "🟣",
    description: "Your strongest audience. They're recent, active, repeat buyers and represent your core market.",
    indicators: ["Country: Netherlands 🇳🇱", "Payment: Shopify Pay and iDEAL", "Recency: Recent activity (~283 days)"],
    insight: "Nurture and reward these loyalists—upsell, subscribe, and retain.",
  },
  "3": {
    label: "Inactive Belgian Shoppers",
    emoji: "🟢",
    description:
      "Low-frequency Belgian customers who haven't purchased recently. Mostly passive and aging in engagement.",
    indicators: ["Country: Belgium 🇧🇪", "Payment: Bancontact", "Recency: Stale"],
    insight: "Try seasonal or culturally tailored campaigns to reengage.",
  },
}

export function ClusterDescription({ onClusterChange }: ClusterDescriptionProps) {
  const [selectedCluster, setSelectedCluster] = useState<string>("2") // Default to Highly Engaged
  const [showDropdown, setShowDropdown] = useState(false)

  const currentCluster = clusterData[selectedCluster]

  const handleClusterChange = (clusterId: string) => {
    setSelectedCluster(clusterId)
    setShowDropdown(false)
    if (onClusterChange) {
      onClusterChange(clusterId)
    }
  }

  const CustomDropdown = () => (
    <div className="relative mb-6">
      <button
        type="button"
        onClick={() => setShowDropdown(!showDropdown)}
        className="w-full flex items-center justify-between px-4 py-3 text-sm border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <span className="flex items-center gap-2">
          <span className="text-lg">{currentCluster.emoji}</span>
          <span className="font-medium">{currentCluster.label}</span>
        </span>
        <ChevronDown className="h-4 w-4 text-gray-400" />
      </button>
      {showDropdown && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {Object.entries(clusterData).map(([key, cluster]) => (
            <button
              key={key}
              type="button"
              onClick={() => handleClusterChange(key)}
              className="w-full px-4 py-3 text-sm text-left hover:bg-gray-100 focus:outline-none focus:bg-gray-100 flex items-center gap-2"
            >
              <span className="text-lg">{cluster.emoji}</span>
              <span className="font-medium">{cluster.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )

  return (
    <div className="space-y-4">
      <CustomDropdown />

      {currentCluster && (
        <div className="space-y-4">
          {/* Description */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
            <p className="text-gray-700 text-sm leading-relaxed">{currentCluster.description}</p>
          </div>

          {/* Key Indicators */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-3">Key Indicators</h4>
            <ul className="space-y-2">
              {currentCluster.indicators.map((indicator, index) => (
                <li key={index} className="flex items-center text-sm text-gray-700">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3 flex-shrink-0"></span>
                  {indicator}
                </li>
              ))}
            </ul>
          </div>

          {/* Strategic Insight */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-2">Strategic Insight</h4>
            <p className="text-green-800 text-sm font-medium">{currentCluster.insight}</p>
          </div>
        </div>
      )}
    </div>
  )
}
