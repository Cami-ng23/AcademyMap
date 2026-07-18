import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { ComparadorView } from '@/components/comparador/comparador-view'

export const metadata = {
  title: 'Comparador de liceos | AcademyMap',
  description: 'Compara hasta 3 liceos técnico-profesionales lado a lado.',
}

export default function ComparadorPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />
      <main className="flex-1">
        <ComparadorView />
      </main>
      <SiteFooter />
    </div>
  )
}
