import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { AdminDashboard } from '@/components/admin/admin-dashboard'

export const metadata = {
  title: 'Panel administrativo | AcademyMap',
  description: 'Métricas de uso y estadísticas de la plataforma AcademyMap.',
}

export default function AdminPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />
      <main className="flex-1">
        <AdminDashboard />
      </main>
      <SiteFooter />
    </div>
  )
}
