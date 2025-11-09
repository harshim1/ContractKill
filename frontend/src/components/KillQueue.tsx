import { useEffect, useState } from 'react'
import { api } from '../api/client'

interface ActionItem {
  id: number
  subscription_id: number
  type: string
  scope: string
  method: string
  status: string
  expected_annual_savings: number
  payload: Record<string, any>
}

export const KillQueue = () => {
  const [actions, setActions] = useState<ActionItem[]>([])

  useEffect(() => {
    api.get<ActionItem[]>('/actions').then(({ data }) => setActions(data))
  }, [])

  if (actions.length === 0) {
    return <p className="text-sm text-slate-400">No queued actions yet.</p>
  }

  return (
    <div className="space-y-3">
      {actions.map((action) => (
        <div key={action.id} className="rounded border border-red-500/30 bg-red-500/10 p-3">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-red-300">{action.type.toUpperCase()}</span>
            <span className="text-xs text-slate-400">Scope: {action.scope}</span>
          </div>
          <p className="mt-1 text-sm text-slate-200">Method: {action.method}</p>
          <p className="mt-1 text-sm text-slate-300">
            Expected Annual Savings: ${action.expected_annual_savings.toFixed(2)}
          </p>
          {action.payload?.body && (
            <pre className="mt-2 max-h-48 overflow-auto whitespace-pre-wrap rounded bg-slate-950 p-2 text-xs text-slate-300">
              {action.payload.body}
            </pre>
          )}
        </div>
      ))}
    </div>
  )
}
