'use client'

import dynamic from 'next/dynamic'
import { Loader2 } from 'lucide-react'
import type { School } from '@/lib/data'

const LeafletMap = dynamic(() => import('./leaflet-map'), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center bg-secondary/50">
      <Loader2 className="size-6 animate-spin text-primary" />
    </div>
  ),
})

export function SchoolMap({
  schools,
  activeId,
  zoom,
}: {
  schools: School[]
  activeId?: string
  zoom?: number
}) {
  return <LeafletMap schools={schools} activeId={activeId} zoom={zoom} />
}
