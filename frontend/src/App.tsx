import { useState } from 'react'
import { Dashboard } from './pages/Dashboard'
import { Subscriptions } from './pages/Subscriptions'
import { Departments } from './pages/Departments'
import { Actions } from './pages/Actions'

const tabs = [
  { id: 'dashboard', label: 'Dashboard', component: <Dashboard /> },
  { id: 'subscriptions', label: 'Subscriptions', component: <Subscriptions /> },
  { id: 'departments', label: 'Departments', component: <Departments /> },
  { id: 'actions', label: 'Actions', component: <Actions /> },
]

export default function App() {
  const [active, setActive] = useState(tabs[0].id)
  const [copilotResponse, setCopilotResponse] = useState('')

  const runCopilot = () => {
    setCopilotResponse(
      'Prioritize canceling Zoom for HR (unused 60+ days), renegotiate Slack Plus for 20% discount, and consolidate Asana + Monday to one tool.'
    )
  }

  return (
    <div className="mx-auto min-h-screen max-w-6xl space-y-6 px-4 py-8">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">ContractKill</h1>
          <p className="text-sm text-slate-400">AI assistant to hunt down zombie SaaS spend.</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <p className="text-xs uppercase text-slate-400">Tracks Alignment</p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {['Amazon Practical AI', 'Capital One Financial Hack', 'Knot TransactionLink', 'Photon HIL', 'Predictive Intelligence'].map((badge) => (
              <span key={badge} className="rounded-full bg-slate-800 px-3 py-1 text-slate-200">
                {badge}
              </span>
            ))}
          </div>
        </div>
      </header>

      <nav className="flex flex-wrap gap-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={`rounded-full px-4 py-2 text-sm font-medium ${
              tab.id === active ? 'bg-primary text-white' : 'bg-slate-800 text-slate-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <section className="space-y-6 bg-slate-950/40 p-2 lg:p-0">
          {tabs.find((tab) => tab.id === active)?.component}
        </section>
        <aside className="space-y-4">
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
            <h2 className="text-lg font-semibold text-white">CFO Copilot</h2>
            <p className="text-sm text-slate-300">Ask “Where can I save 30% fastest?”</p>
            <button onClick={runCopilot} className="mt-3 rounded bg-accent px-3 py-2 text-sm font-semibold text-slate-950">
              Ask Copilot
            </button>
            {copilotResponse && <p className="mt-3 text-sm text-slate-200">{copilotResponse}</p>}
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
            <h2 className="text-lg font-semibold text-white">Kill Queue Snapshot</h2>
            <p className="text-sm text-slate-400">Jump to the Actions tab for more detail.</p>
          </div>
        </aside>
      </main>
    </div>
  )
}
