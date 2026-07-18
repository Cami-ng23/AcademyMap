import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { Hero } from '@/components/landing/hero'
import { AreasSection } from '@/components/landing/areas-section'
import { HowItWorks } from '@/components/landing/how-it-works'
import { Features } from '@/components/landing/features'
import { CTA } from '@/components/landing/cta'
import { StatsBar } from '@/components/landing/stats-bar'

export default function Page() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <StatsBar />
        <AreasSection />
        <HowItWorks />
        <Features />
        <CTA />
      </main>
      <SiteFooter />
    </>
  )
}
