import { useEffect, useState } from 'react'
import { api } from '../api/client'

interface ActionItem {
  id: number
  type: string
  method: string
  scope: string
  status: string
  expected_annual_savings: number
  payload: Record<string, any>
}

export const Actions = () => {
  const [actions, setActions] = useState<ActionItem[]>([])

  useEffect(() => {
    api.get<ActionItem[]>('/actions').then(({ data }) => setActions(data))
  }, [])

  return (
    <div className="space-y-3">
      {actions.map((action) => (
        <div key={action.id} className="rounded border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-accent">{action.type.toUpperCase()}</h3>
            <span className="text-xs uppercase text-slate-400">{action.status}</span>
          </div>
          <p className="mt-1 text-sm text-slate-300">Scope: {action.scope}</p>
          <p className="text-sm text-slate-300">Method: {action.method}</p>
          <p className="text-sm text-slate-300">
            Expected Savings: ${action.expected_annual_savings.toFixed(2)}
          </p>
          {action.payload?.body && (
            <pre className="mt-2 whitespace-pre-wrap rounded bg-slate-950 p-2 text-xs text-slate-300">
              {action.payload.body}
            </pre>
          )}
        </div>
      ))}
    </div>
  )
}
