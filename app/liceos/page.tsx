import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { LiceosExplorer } from '@/components/liceos/liceos-explorer'

export default function LiceosPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <LiceosExplorer />
      </main>
      <SiteFooter />
    </>
  )
}
