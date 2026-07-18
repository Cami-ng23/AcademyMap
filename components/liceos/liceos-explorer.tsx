'use client'

import { useMemo, useState } from 'react'
import { LayoutGrid, Map as MapIcon, Search, SlidersHorizontal } from 'lucide-react'
import { AREAS, type AreaId, SCHOOLS } from '@/lib/data'
import { AreaIcon } from '@/components/area-icon'
import { SchoolCard } from '@/components/school-card'
import { SchoolMap } from '@/components/map/school-map'
import { cn } from '@/lib/utils'

export function LiceosExplorer() {
  const [query, setQuery] = useState('')
  const [area, setArea] = useState<AreaId | 'all'>('all')
  const [view, setView] = useState<'grid' | 'map'>('grid')

  const filtered = useMemo(() => {
    return SCHOOLS.filter((s) => {
      const matchesArea = area === 'all' || s.areas.includes(area)
      const q = query.trim().toLowerCase()
      const matchesQuery =
        !q ||
        s.name.toLowerCase().includes(q) ||
        s.comuna.toLowerCase().includes(q) ||
        s.region.toLowerCase().includes(q) ||
        s.specialties.some((sp) => sp.toLowerCase().includes(q))
      return matchesArea && matchesQuery
    })
  }, [query, area])

  return (
    <div className="mx-auto max-w-6xl px-4 pb-8 pt-28">
      <div className="max-w-2xl">
        <h1 className="text-balance font-display text-3xl font-extrabold tracking-tight sm:text-4xl">
          Explora los liceos técnico-profesionales
        </h1>
        <p className="mt-3 text-pretty text-muted-foreground">
          Filtra por área, busca por comuna o especialidad, y ubica cada liceo en el mapa
          interactivo.
        </p>
      </div>

      {/* controls */}
      <div className="mt-8 flex flex-col gap-4 rounded-3xl border border-border/70 bg-card p-4 shadow-soft sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar por nombre, comuna o especialidad…"
            className="w-full rounded-2xl border border-border bg-background py-3 pl-10 pr-4 text-sm outline-none transition-shadow focus:ring-2 focus:ring-primary/40"
            aria-label="Buscar liceos"
          />
        </div>
        <div className="flex items-center gap-1 rounded-2xl bg-secondary p-1">
          <ViewBtn active={view === 'grid'} onClick={() => setView('grid')} icon={LayoutGrid}>
            Tarjetas
          </ViewBtn>
          <ViewBtn active={view === 'map'} onClick={() => setView('map')} icon={MapIcon}>
            Mapa
          </ViewBtn>
        </div>
      </div>

      {/* area filters */}
      <div className="mt-4 flex items-center gap-2 overflow-x-auto pb-2">
        <span className="inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-muted-foreground">
          <SlidersHorizontal className="size-4" />
        </span>
        <FilterChip active={area === 'all'} onClick={() => setArea('all')}>
          Todas
        </FilterChip>
        {(Object.keys(AREAS) as AreaId[]).map((id) => (
          <FilterChip key={id} active={area === id} onClick={() => setArea(id)}>
            <AreaIcon icon={AREAS[id].icon} className="size-3.5" />
            {AREAS[id].name.split(' ')[0]}
          </FilterChip>
        ))}
      </div>

      <p className="mt-4 text-sm text-muted-foreground">
        {filtered.length} {filtered.length === 1 ? 'liceo encontrado' : 'liceos encontrados'}
      </p>

      {/* content */}
      {view === 'grid' ? (
        filtered.length ? (
          <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((s, i) => (
              <SchoolCard key={s.id} school={s} index={i} />
            ))}
          </div>
        ) : (
          <div className="mt-8 rounded-3xl border border-dashed border-border p-12 text-center text-muted-foreground">
            No encontramos liceos con esos filtros. Prueba con otra búsqueda.
          </div>
        )
      ) : (
        <div className="mt-4 h-[560px] overflow-hidden rounded-3xl border border-border/70 shadow-soft">
          <SchoolMap schools={filtered.length ? filtered : SCHOOLS} />
        </div>
      )}
    </div>
  )
}

function ViewBtn({
  active,
  onClick,
  icon: Icon,
  children,
}: {
  active: boolean
  onClick: () => void
  icon: React.ElementType
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-2 rounded-xl px-3.5 py-2 text-sm font-semibold transition-colors',
        active ? 'bg-card text-foreground shadow-soft' : 'text-muted-foreground hover:text-foreground'
      )}
      aria-pressed={active}
    >
      <Icon className="size-4" />
      {children}
    </button>
  )
}

function FilterChip({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-sm font-medium transition-all',
        active
          ? 'border-primary bg-primary text-primary-foreground shadow-soft'
          : 'border-border bg-card text-foreground hover:border-primary/40 hover:bg-secondary'
      )}
      aria-pressed={active}
    >
      {children}
    </button>
  )
}
