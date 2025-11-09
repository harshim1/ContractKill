interface VendorCardProps {
  vendor: string
  monthlyCost: number
  issues: string[]
  onTerminate: () => void
  onNegotiate: () => void
}

export const VendorCard = ({ vendor, monthlyCost, issues, onTerminate, onNegotiate }: VendorCardProps) => (
  <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
    <div className="flex items-center justify-between">
      <div>
        <h3 className="text-xl font-semibold">{vendor}</h3>
        <p className="text-sm text-slate-400">${monthlyCost.toFixed(2)} / month</p>
      </div>
      <div className="space-x-2">
        <button onClick={onNegotiate} className="rounded bg-primary px-3 py-1 text-sm font-medium text-white">
          Negotiate
        </button>
        <button onClick={onTerminate} className="rounded bg-red-500 px-3 py-1 text-sm font-medium text-white">
          Terminate
        </button>
      </div>
    </div>
    <div className="mt-3 flex flex-wrap gap-2">
      {issues.map((issue) => (
        <span key={issue} className="rounded-full bg-slate-800 px-2 py-1 text-xs uppercase text-slate-300">
          {issue}
        </span>
      ))}
    </div>
  </div>
)
