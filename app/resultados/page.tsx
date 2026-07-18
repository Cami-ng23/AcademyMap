import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { ResultsView } from '@/components/results/results-view'

export default function ResultadosPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <ResultsView />
      </main>
      <SiteFooter />
    </>
  )
}
