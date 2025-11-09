import { useEffect, useMemo, useState } from 'react'
import { api } from '../api/client'
import { DeptSplitter } from '../components/DeptSplitter'

interface Subscription {
  id: number
  vendor: string
  monthly_cost: number
  issues: string[]
  department?: string | null
}

const departments = ['Sales', 'Engineering', 'Marketing', 'HR', 'IT', 'Operations']

export const Departments = () => {
  const [selected, setSelected] = useState(departments[0])
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([])

  useEffect(() => {
    api.get<Subscription[]>('/subscriptions').then(({ data }) => setSubscriptions(data))
  }, [])

  const scopedSubscriptions = useMemo(
    () => subscriptions.filter((subscription) => (subscription.department || 'General') === selected),
    [subscriptions, selected]
  )

  const queueTermination = async (id: number, scope: string) => {
    await api.post('/actions/terminate', { subscription_id: id, scope, method: 'browser' })
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {departments.map((department) => (
          <button
            key={department}
            onClick={() => setSelected(department)}
            className={`rounded-full px-4 py-2 text-sm ${
              department === selected ? 'bg-accent text-slate-950' : 'bg-slate-800 text-slate-300'
            }`}
          >
            {department}
          </button>
        ))}
      </div>
      <DeptSplitter department={selected} subscriptions={scopedSubscriptions} onQueueTermination={queueTermination} />
    </div>
  )
}
