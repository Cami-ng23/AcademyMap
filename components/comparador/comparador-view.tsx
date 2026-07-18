'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowLeft, GitCompare, Star, X } from 'lucide-react'
import { AREAS, SCHOOLS } from '@/lib/data'
import { AreaIcon } from '@/components/area-icon'
import { useQuiz } from '@/components/quiz-provider'
import { cn } from '@/lib/utils'

type MetricRow = {
  label: string
  render: (schoolId: string) => React.ReactNode
  best?: (ids: string[]) => string | null
}

export function ComparadorView() {
  const { compare, toggleCompare } = useQuiz()
  const schools = SCHOOLS.filter((s) => compare.includes(s.id))

  const rows: MetricRow[] = [
    {
      label: 'Comuna',
      render: (id) => SCHOOLS.find((s) => s.id === id)!.comuna,
    },
    {
      label: 'Dependencia',
      render: (id) => SCHOOLS.find((s) => s.id === id)!.dependency,
    },
    {
      label: 'Gratuidad',
      render: (id) => {
        const s = SCHOOLS.find((x) => x.id === id)!
        return (
          <span
            className={cn(
              'inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold',
              s.free ? 'bg-success/15 text-success' : 'bg-secondary text-secondary-foreground'
            )}
          >
            {s.free ? 'Gratuito' : 'Subvencionado'}
          </span>
        )
      },
    },
    {
      label: 'Valoración',
      render: (id) => {
        const s = SCHOOLS.find((x) => x.id === id)!
        return (
          <span className="inline-flex items-center gap-1 font-semibold">
            <Star className="size-3.5 fill-highlight text-highlight" />
            {s.rating}
          </span>
        )
      },
      best: (ids) =>
        ids.reduce((best, id) => {
          const s = SCHOOLS.find((x) => x.id === id)!
          const b = SCHOOLS.find((x) => x.id === best)!
          return s.rating > b.rating ? id : best
        }, ids[0]),
    },
    {
      label: 'Estudiantes',
      render: (id) => SCHOOLS.find((s) => s.id === id)!.students.toLocaleString('es-CL'),
    },
    {
      label: 'Empleabilidad',
      render: (id) => `${SCHOOLS.find((s) => s.id === id)!.employability}%`,
      best: (ids) =>
        ids.reduce((best, id) => {
          const s = SCHOOLS.find((x) => x.id === id)!
          const b = SCHOOLS.find((x) => x.id === best)!
          return s.employability > b.employability ? id : best
        }, ids[0]),
    },
    {
      label: 'Cupos (tasa admisión)',
      render: (id) => `${SCHOOLS.find((s) => s.id === id)!.admissionRate}%`,
    },
    {
      label: 'Especialidades',
      render: (id) => (
        <div className="flex flex-wrap gap-1">
          {SCHOOLS.find((s) => s.id === id)!.specialties.map((sp) => (
            <span key={sp} className="rounded-md bg-secondary px-1.5 py-0.5 text-xs">
              {sp}
            </span>
          ))}
        </div>
      ),
    },
  ]

  if (schools.length === 0) {
    return (
      <div className="mx-auto flex max-w-2xl flex-col items-center px-4 py-24 text-center">
        <div className="grid size-16 place-items-center rounded-2xl bg-primary/10 text-primary">
          <GitCompare className="size-8" />
        </div>
        <h1 className="mt-6 font-display text-3xl font-bold">Aún no comparas liceos</h1>
        <p className="mt-3 text-pretty text-muted-foreground">
          Agrega hasta 3 liceos con el botón{' '}
          <span className="font-semibold text-foreground">+</span> desde las tarjetas o los
          resultados del test para verlos lado a lado.
        </p>
        <Link
          href="/liceos"
          className="mt-8 inline-flex items-center gap-2 rounded-2xl bg-primary px-6 py-3 font-semibold text-primary-foreground shadow-soft transition-transform hover:-translate-y-0.5"
        >
          Explorar liceos
        </Link>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 md:py-14">
      <Link
        href="/liceos"
        className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" />
        Volver a explorar
      </Link>

      <div className="mt-4 flex flex-col gap-2">
        <h1 className="text-balance font-display text-3xl font-bold md:text-4xl">
          Comparador de liceos
        </h1>
        <p className="text-muted-foreground">
          Estás comparando {schools.length} de 3 liceos. Lo mejor de cada fila se destaca en verde.
        </p>
      </div>

      <div className="mt-8 overflow-x-auto rounded-3xl border border-border/70 bg-card shadow-soft">
        <table className="w-full min-w-[640px] border-collapse">
          <thead>
            <tr>
              <th className="sticky left-0 z-10 w-40 bg-card p-4 text-left align-bottom">
                <span className="text-sm font-medium text-muted-foreground">Criterio</span>
              </th>
              {schools.map((s) => (
                <th key={s.id} className="min-w-[220px] p-4 text-left align-top">
                  <div className="relative overflow-hidden rounded-2xl border border-border/60">
                    <button
                      type="button"
                      onClick={() => toggleCompare(s.id)}
                      aria-label={`Quitar ${s.shortName} del comparador`}
                      className="absolute right-2 top-2 z-10 inline-flex size-7 items-center justify-center rounded-lg glass-strong text-foreground transition-colors hover:bg-destructive hover:text-destructive-foreground"
                    >
                      <X className="size-4" />
                    </button>
                    <div className="relative h-24">
                      <Image
                        src={s.image || '/placeholder.svg'}
                        alt=""
                        fill
                        sizes="220px"
                        className="object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    </div>
                    <div className="flex items-center gap-1.5 p-3">
                      {s.areas.slice(0, 3).map((a) => (
                        <span
                          key={a}
                          className="grid size-6 place-items-center rounded-md"
                          style={{ backgroundColor: `${AREAS[a].color}22`, color: AREAS[a].color }}
                        >
                          <AreaIcon icon={AREAS[a].icon} className="size-3.5" />
                        </span>
                      ))}
                    </div>
                    <Link
                      href={`/liceos/${s.id}`}
                      className="block px-3 pb-3 font-display text-sm font-bold leading-tight hover:text-primary"
                    >
                      {s.shortName}
                    </Link>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => {
              const bestId = row.best ? row.best(schools.map((s) => s.id)) : null
              return (
                <motion.tr
                  key={row.label}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.04 }}
                  className="border-t border-border/60"
                >
                  <td className="sticky left-0 z-10 bg-card p-4 text-sm font-medium text-muted-foreground">
                    {row.label}
                  </td>
                  {schools.map((s) => (
                    <td
                      key={s.id}
                      className={cn(
                        'p-4 text-sm',
                        bestId === s.id && 'bg-success/10 font-semibold text-foreground'
                      )}
                    >
                      {row.render(s.id)}
                    </td>
                  ))}
                </motion.tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
