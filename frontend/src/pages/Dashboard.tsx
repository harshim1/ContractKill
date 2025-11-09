import { useEffect, useState } from 'react'
import { api, fetchMetrics, MetricsResponse } from '../api/client'
import { SavingsCounter } from '../components/SavingsCounter'
import { KnotConnect } from '../components/KnotConnect'
import { KillQueue } from '../components/KillQueue'

interface SubscriptionSummary {
  id: number
  vendor: string
  monthly_cost: number
  issues: string[]
}

export const Dashboard = () => {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)
  const [topVendors, setTopVendors] = useState<SubscriptionSummary[]>([])

  useEffect(() => {
    fetchMetrics().then(setMetrics)
    api.get<SubscriptionSummary[]>('/subscriptions').then(({ data }) => {
      const sorted = [...data].sort((a, b) => b.monthly_cost - a.monthly_cost)
      setTopVendors(sorted.slice(0, 4))
    })
  }, [])

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg bg-slate-900 p-4">
          <p className="text-sm uppercase text-slate-400">Monthly Spend</p>
          <p className="mt-2 text-3xl font-semibold text-white">
            ${metrics ? metrics.monthly_spend.toFixed(2) : '—'}
          </p>
        </div>
        <SavingsCounter target={metrics ? Math.round(metrics.annual_savings) : 0} />
        <div className="rounded-lg bg-slate-900 p-4">
          <p className="text-sm uppercase text-slate-400">Zombies Found</p>
          <p className="mt-2 text-3xl font-semibold text-white">{metrics ? metrics.zombies_found : 0}</p>
        </div>
      </div>

      <section>
        <h2 className="text-xl font-semibold">Top Vendors</h2>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {topVendors.map((vendor) => (
            <div key={vendor.id} className="rounded border border-slate-800 bg-slate-900 p-4">
              <div className="flex items-center justify-between">
                <span className="text-lg font-semibold">{vendor.vendor}</span>
                <span className="text-sm text-slate-400">${vendor.monthly_cost.toFixed(2)}</span>
              </div>
              <div className="mt-2 flex flex-wrap gap-2">
                {vendor.issues.map((issue) => (
                  <span key={issue} className="rounded-full bg-slate-800 px-2 py-1 text-xs uppercase text-slate-300">
                    {issue}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Knot TransactionLink</h2>
        <KnotConnect />
      </section>

      <section>
        <h2 className="text-xl font-semibold">Kill Queue</h2>
        <KillQueue />
      </section>
    </div>
  )
}
