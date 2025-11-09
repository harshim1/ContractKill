interface SKUPanelProps {
  transactions: Array<{
    id: number
    merchant_name: string
    amount: number
    currency: string
    sku?: string | null
    description?: string | null
  }>
}

export const SKUPanel = ({ transactions }: SKUPanelProps) => {
  const grouped = transactions.reduce<Record<string, typeof transactions>>((acc, tx) => {
    const key = tx.merchant_name
    acc[key] = acc[key] || []
    acc[key].push(tx)
    return acc
  }, {})

  return (
    <div className="mt-4 rounded-lg border border-slate-800 p-4">
      <h4 className="text-base font-semibold text-slate-200">SKU Breakdown</h4>
      <div className="mt-2 space-y-4">
        {Object.entries(grouped).map(([merchant, items]) => (
          <div key={merchant} className="rounded border border-slate-800 p-3">
            <h5 className="font-medium text-accent">{merchant}</h5>
            <ul className="mt-2 space-y-1 text-sm text-slate-300">
              {items.map((item) => (
                <li key={item.id} className="flex justify-between">
                  <span>{item.sku || 'SKU-FAKE'}</span>
                  <span>
                    {item.currency} {item.amount.toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}
