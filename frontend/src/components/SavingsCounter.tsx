import { useEffect, useState } from 'react'

interface SavingsCounterProps {
  target: number
}

export const SavingsCounter = ({ target }: SavingsCounterProps) => {
  const [value, setValue] = useState(0)

  useEffect(() => {
    let frame: number
    let start: number | null = null
    const duration = 1500

    const step = (timestamp: number) => {
      if (!start) start = timestamp
      const progress = Math.min((timestamp - start) / duration, 1)
      setValue(Math.floor(progress * target))
      if (progress < 1) {
        frame = requestAnimationFrame(step)
      }
    }

    frame = requestAnimationFrame(step)
    return () => cancelAnimationFrame(frame)
  }, [target])

  return (
    <div className="rounded-lg bg-slate-900 p-4 shadow-lg">
      <p className="text-sm uppercase tracking-widest text-slate-400">Annual Savings</p>
      <p className="mt-2 text-3xl font-bold text-accent">${value.toLocaleString()}</p>
    </div>
  )
}
