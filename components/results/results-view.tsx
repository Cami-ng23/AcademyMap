'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, RefreshCw, Sparkles } from 'lucide-react'
import { AREAS } from '@/lib/data'
import { matchSchools, scoreAreas } from '@/lib/quiz'
import { useQuiz } from '@/components/quiz-provider'
import { AreaIcon } from '@/components/area-icon'
import { SchoolCard } from '@/components/school-card'

export function ResultsView() {
  const { answers, completed, reset } = useQuiz()

  if (!completed || Object.keys(answers).length === 0) {
    return (
      <div className="mx-auto flex min-h-[70svh] max-w-md flex-col items-center justify-center px-4 text-center">
        <div className="flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary">
          <Sparkles className="size-7" />
        </div>
        <h1 className="mt-5 font-display text-2xl font-extrabold">Aún no tienes resultados</h1>
        <p className="mt-2 text-muted-foreground">
          Responde el test vocacional para descubrir qué liceos técnicos encajan contigo.
        </p>
        <Link
          href="/quiz"
          className="mt-6 inline-flex items-center gap-2 rounded-2xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-glow transition-all hover:brightness-110"
        >
          Comenzar el test
          <ArrowRight className="size-4" />
        </Link>
      </div>
    )
  }

  const ranked = scoreAreas(answers).slice(0, 4)
  const matches = matchSchools(answers)
  const top = ranked[0]

  return (
    <div className="mx-auto max-w-6xl px-4 pb-8 pt-28">
      {/* header */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-[2rem] bg-primary p-8 text-primary-foreground shadow-glow sm:p-10"
      >
        <div className="pointer-events-none absolute -right-16 -top-16 size-64 rounded-full bg-primary-foreground/10 blur-3xl" />
        <div className="relative flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-primary-foreground/15 px-3 py-1 text-sm font-medium">
              <Sparkles className="size-4" />
              Tu resultado
            </span>
            <h1 className="mt-4 text-balance font-display text-3xl font-extrabold leading-tight sm:text-4xl">
              Tu área destacada es {AREAS[top.area].name}
            </h1>
            <p className="mt-2 max-w-lg text-pretty opacity-90">
              {AREAS[top.area].description} Estos son los liceos que mejor se ajustan a tu perfil.
            </p>
          </div>
          <div className="flex size-28 shrink-0 items-center justify-center rounded-3xl bg-primary-foreground/15">
            <AreaIcon icon={AREAS[top.area].icon} className="size-14" />
          </div>
        </div>
      </motion.div>

      {/* area breakdown */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {ranked.map((r, i) => (
          <motion.div
            key={r.area}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="rounded-3xl border border-border/70 bg-card p-5 shadow-soft"
          >
            <div className="flex items-center justify-between">
              <div
                className="flex size-10 items-center justify-center rounded-xl"
                style={{
                  backgroundColor: `color-mix(in oklch, ${AREAS[r.area].color} 16%, transparent)`,
                }}
              >
                <AreaIcon icon={AREAS[r.area].icon} className="size-5" />
              </div>
              <span className="font-display text-2xl font-extrabold text-primary">
                {r.score}%
              </span>
            </div>
            <h3 className="mt-3 text-sm font-bold leading-tight">{AREAS[r.area].name}</h3>
            <div className="mt-2 h-2 rounded-full bg-secondary">
              <motion.div
                className="h-2 rounded-full"
                style={{ backgroundColor: AREAS[r.area].color }}
                initial={{ width: 0 }}
                animate={{ width: `${r.score}%` }}
                transition={{ duration: 0.8, delay: 0.2 + i * 0.08 }}
              />
            </div>
          </motion.div>
        ))}
      </div>

      {/* schools */}
      <div className="mt-12 flex items-center justify-between">
        <div>
          <h2 className="font-display text-2xl font-extrabold tracking-tight">
            Liceos recomendados para ti
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Ordenados por porcentaje de coincidencia con tu perfil.
          </p>
        </div>
        <button
          type="button"
          onClick={reset}
          className="hidden items-center gap-2 rounded-2xl border border-border px-4 py-2.5 text-sm font-semibold transition-colors hover:bg-secondary sm:inline-flex"
        >
          <RefreshCw className="size-4" />
          Repetir test
        </button>
      </div>

      <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {matches.map((m, i) => (
          <SchoolCard key={m.school.id} school={m.school} match={m.match} index={i} />
        ))}
      </div>

      <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
        <Link
          href="/comparar"
          className="inline-flex items-center gap-2 rounded-2xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-soft transition-all hover:shadow-glow hover:brightness-110"
        >
          Comparar mis favoritos
          <ArrowRight className="size-4" />
        </Link>
        <Link
          href="/liceos"
          className="inline-flex items-center gap-2 rounded-2xl border border-border px-6 py-3 text-sm font-semibold transition-colors hover:bg-secondary"
        >
          Ver todos en el mapa
        </Link>
      </div>
    </div>
  )
}
