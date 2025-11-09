interface DeptSplitterProps {
  department: string
  subscriptions: Array<{
    id: number
    vendor: string
    monthly_cost: number
    issues: string[]
  }>
  onQueueTermination: (id: number, scope: string) => Promise<void>
}

export const DeptSplitter = ({ department, subscriptions, onQueueTermination }: DeptSplitterProps) => {
  return (
    <div className="space-y-3">
      {subscriptions.map((subscription) => (
        <div key={subscription.id} className="rounded border border-slate-800 p-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-lg font-semibold">{subscription.vendor}</h4>
              <p className="text-sm text-slate-400">${subscription.monthly_cost.toFixed(2)} / month</p>
            </div>
            <button
              onClick={() => onQueueTermination(subscription.id, department)}
              className="rounded bg-red-500 px-3 py-1 text-sm font-medium text-white"
            >
              Terminate for {department}
            </button>
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {subscription.issues.map((issue) => (
              <span key={issue} className="rounded-full bg-slate-800 px-2 py-1 text-xs uppercase text-slate-300">
                {issue}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
