'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Check, MapPin, Plus, Star, Users } from 'lucide-react'
import type { School } from '@/lib/data'
import { AREAS } from '@/lib/data'
import { AreaIcon } from '@/components/area-icon'
import { useQuiz } from '@/components/quiz-provider'
import { cn } from '@/lib/utils'

export function SchoolCard({
  school,
  match,
  index = 0,
}: {
  school: School
  match?: number
  index?: number
}) {
  const { compare, toggleCompare } = useQuiz()
  const inCompare = compare.includes(school.id)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.4, delay: Math.min(index * 0.06, 0.4) }}
      className="group flex flex-col overflow-hidden rounded-3xl border border-border/70 bg-card shadow-soft transition-all hover:-translate-y-1 hover:shadow-float"
    >
      <div className="relative h-44 overflow-hidden">
        <Image
          src={school.image || '/placeholder.svg'}
          alt={`Instalaciones del ${school.name}`}
          fill
          sizes="(max-width: 768px) 100vw, 400px"
          className="object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/55 via-black/10 to-transparent" />
        {match !== undefined && (
          <div className="absolute left-3 top-3 rounded-full glass-strong px-3 py-1 text-xs font-bold text-foreground shadow-soft">
            {match}% match
          </div>
        )}
        <button
          type="button"
          onClick={() => toggleCompare(school.id)}
          aria-pressed={inCompare}
          aria-label={inCompare ? 'Quitar del comparador' : 'Agregar al comparador'}
          className={cn(
            'absolute right-3 top-3 inline-flex size-9 items-center justify-center rounded-xl shadow-soft transition-all',
            inCompare
              ? 'bg-success text-success-foreground'
              : 'glass-strong text-foreground hover:bg-primary hover:text-primary-foreground'
          )}
        >
          {inCompare ? <Check className="size-4" /> : <Plus className="size-4" />}
        </button>
        <div className="absolute bottom-3 left-3 flex items-center gap-1.5 text-white">
          <MapPin className="size-4" aria-hidden="true" />
          <span className="text-sm font-medium">
            {school.comuna}, {school.region}
          </span>
        </div>
      </div>

      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-display text-lg font-bold leading-tight">{school.shortName}</h3>
          <span className="flex shrink-0 items-center gap-1 rounded-lg bg-highlight/15 px-2 py-1 text-sm font-bold text-highlight-foreground">
            <Star className="size-3.5 fill-highlight text-highlight" />
            {school.rating}
          </span>
        </div>

        <div className="mt-3 flex flex-wrap gap-1.5">
          {school.areas.slice(0, 3).map((a) => (
            <span
              key={a}
              className="inline-flex items-center gap-1 rounded-full bg-secondary px-2.5 py-1 text-xs font-medium text-secondary-foreground"
            >
              <AreaIcon icon={AREAS[a].icon} className="size-3" />
              {AREAS[a].name.split(' ')[0]}
            </span>
          ))}
        </div>

        <p className="mt-3 line-clamp-2 text-sm leading-relaxed text-muted-foreground">
          {school.description}
        </p>

        <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1">
            <Users className="size-3.5" />
            {school.students.toLocaleString('es-CL')} estudiantes
          </span>
          <span
            className={cn(
              'inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-semibold',
              school.free ? 'bg-success/15 text-success' : 'bg-secondary text-secondary-foreground'
            )}
          >
            {school.free ? 'Gratuito' : 'Subvencionado'}
          </span>
        </div>

        <Link
          href={`/liceos/${school.id}`}
          className="mt-5 inline-flex items-center justify-center rounded-2xl bg-secondary px-4 py-2.5 text-sm font-semibold text-secondary-foreground transition-colors hover:bg-primary hover:text-primary-foreground"
        >
          Ver perfil del liceo
        </Link>
      </div>
    </motion.div>
  )
}
