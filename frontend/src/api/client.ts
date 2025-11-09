import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

export const api = axios.create({
  baseURL,
})

export type MetricsResponse = {
  monthly_spend: number
  annual_savings: number
  zombies_found: number
}

export const fetchMetrics = async (): Promise<MetricsResponse> => {
  const { data } = await api.get<MetricsResponse>('/reports/metrics')
  return data
}
