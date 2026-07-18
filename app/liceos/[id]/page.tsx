import { notFound } from 'next/navigation'
import { SiteHeader } from '@/components/site-header'
import { SiteFooter } from '@/components/site-footer'
import { SchoolProfile } from '@/components/school/school-profile'
import { getSchool, SCHOOLS } from '@/lib/data'

export function generateStaticParams() {
  return SCHOOLS.map((s) => ({ id: s.id }))
}

export default async function SchoolPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const school = getSchool(id)
  if (!school) notFound()

  return (
    <>
      <SiteHeader />
      <main>
        <SchoolProfile school={school} />
      </main>
      <SiteFooter />
    </>
  )
}
