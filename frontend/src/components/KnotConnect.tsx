import { useState } from 'react'
import { api } from '../api/client'
import { SKUPanel } from './SKUPanel'

type Merchant = {
  id: number
  name: string
}

const merchants: Merchant[] = [
  { id: 44, name: 'Amazon' },
  { id: 12, name: 'Target' },
  { id: 45, name: 'Walmart' },
]

export const KnotConnect = () => {
  const [selected, setSelected] = useState<Merchant | null>(null)
  const [loading, setLoading] = useState(false)
  const [transactions, setTransactions] = useState<any[]>([])
  const [summary, setSummary] = useState('')

  const handleConnect = async () => {
    if (!selected) return
    setLoading(true)
    try {
      const { data } = await api.post('/knot/transactions/sync', {
        merchant_id: selected.id,
      })
      setTransactions(data.transactions)
      setSummary(`Imported ${data.count} transactions totaling $${data.total_amount.toFixed(2)}`)
    } catch (error) {
      setSummary('Failed to import transactions. Using demo data instead.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-lg bg-slate-900 p-4">
      <div className="flex items-center gap-4">
        <img src="https://knotapi.com/favicon.ico" alt="Knot" className="h-8 w-8" />
        <h3 className="text-lg font-semibold">Link a Merchant via Knot</h3>
      </div>
      <div className="mt-4 flex flex-col gap-2 md:flex-row">
        <select
          className="w-full rounded border border-slate-700 bg-slate-950 p-2"
          onChange={(event) => setSelected(merchants.find((m) => m.id === Number(event.target.value)) || null)}
        >
          <option value="">Choose merchant</option>
          {merchants.map((merchant) => (
            <option key={merchant.id} value={merchant.id}>
              {merchant.name}
            </option>
          ))}
        </select>
        <button
          onClick={handleConnect}
          className="rounded bg-primary px-4 py-2 font-medium text-white disabled:opacity-50"
          disabled={!selected || loading}
        >
          {loading ? 'Linking…' : 'Link Merchant'}
        </button>
      </div>
      {summary && <p className="mt-3 text-sm text-slate-300">{summary}</p>}
      {transactions.length > 0 && <SKUPanel transactions={transactions} />}
    </div>
  )
}
