import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { VendorCard } from '../components/VendorCard'

interface Subscription {
  id: number
  vendor: string
  monthly_cost: number
  issues: string[]
}

export const Subscriptions = () => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([])

  const load = () => {
    api.get<Subscription[]>('/subscriptions').then(({ data }) => setSubscriptions(data))
  }

  useEffect(() => {
    load()
  }, [])

  const terminate = async (id: number) => {
    await api.post('/actions/terminate', { subscription_id: id, scope: 'org', method: 'email' })
    load()
  }

  const negotiate = async (id: number) => {
    await api.post('/actions/negotiate', { subscription_id: id })
  }

  return (
    <div className="space-y-4">
      {subscriptions.map((subscription) => (
        <VendorCard
          key={subscription.id}
          vendor={subscription.vendor}
          monthlyCost={subscription.monthly_cost}
          issues={subscription.issues}
          onTerminate={() => terminate(subscription.id)}
          onNegotiate={() => negotiate(subscription.id)}
        />
      ))}
    </div>
  )
}
