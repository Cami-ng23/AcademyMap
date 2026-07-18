'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  ArrowLeft,
  Check,
  GraduationCap,
  MapPin,
  Plus,
  Scale,
  Star,
  TrendingUp,
  Users,
} from 'lucide-react'
import { AREAS, type School } from '@/lib/data'
import { AreaIcon } from '@/components/area-icon'
import { useQuiz } from '@/components/quiz-provider'
import { SchoolMap } from '@/components/map/school-map'
import { cn } from '@/lib/utils'

export function SchoolProfile({ school }: { school: School }) {
  const { compare, toggleCompare } = useQuiz()
  const inCompare = compare.includes(school.id)

  const stats = [
    { icon: Star, label: 'Valoración', value: `${school.rating} / 5` },
    { icon: Users, label: 'Estudiantes', value: school.students.toLocaleString('es-CL') },
    { icon: TrendingUp, label: 'Empleabilidad', value: `${school.employability}%` },
    { icon: GraduationCap, label: 'Admisión', value: `${school.admissionRate}%` },
  ]

  return (
    <div className="mx-auto max-w-6xl px-4 pb-8 pt-24">
      <Link
        href="/liceos"
        className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" />
        Volver a los liceos
      </Link>

      {/* hero */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative mt-4 overflow-hidden rounded-[2rem] shadow-float"
      >
        <div className="relative h-64 sm:h-80">
          <Image
            src={school.image || '/placeholder.svg'}
            alt={`Instalaciones del ${school.name}`}
            fill
            priority
            sizes="100vw"
            className="object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
        </div>
        <div className="absolute inset-x-0 bottom-0 p-6 text-white sm:p-8">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-sm font-medium backdrop-blur">
              <MapPin className="size-4" />
              {school.comuna}, {school.region}
            </span>
            <span
              className={cn(
                'rounded-full px-3 py-1 text-sm font-semibold',
                school.free ? 'bg-success text-success-foreground' : 'bg-white/15 backdrop-blur'
              )}
            >
              {school.free ? 'Gratuito' : 'Subvencionado'}
            </span>
          </div>
          <h1 className="mt-3 text-balance font-display text-3xl font-extrabold leading-tight sm:text-4xl">
            {school.name}
          </h1>
          <p className="mt-1 text-sm opacity-90">{school.dependency}</p>
        </div>
      </motion.div>

      {/* stats */}
      <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06 }}
            className="rounded-3xl border border-border/70 bg-card p-5 shadow-soft"
          >
            <s.icon className="size-5 text-primary" aria-hidden="true" />
            <p className="mt-3 font-display text-2xl font-extrabold">{s.value}</p>
            <p className="text-xs text-muted-foreground">{s.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <section className="rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
            <h2 className="font-display text-xl font-bold">Sobre el liceo</h2>
            <p className="mt-3 leading-relaxed text-muted-foreground">{school.description}</p>
          </section>

          <section className="rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
            <h2 className="font-display text-xl font-bold">Especialidades</h2>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              {school.specialties.map((sp) => (
                <div
                  key={sp}
                  className="flex items-center gap-3 rounded-2xl border border-border/60 bg-background p-3"
                >
                  <span className="flex size-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <GraduationCap className="size-4" />
                  </span>
                  <span className="text-sm font-medium">{sp}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
            <h2 className="font-display text-xl font-bold">Áreas de formación</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {school.areas.map((a) => (
                <span
                  key={a}
                  className="inline-flex items-center gap-1.5 rounded-full bg-secondary px-3 py-1.5 text-sm font-medium text-secondary-foreground"
                >
                  <AreaIcon icon={AREAS[a].icon} className="size-4" />
                  {AREAS[a].name}
                </span>
              ))}
            </div>
          </section>

          <section className="overflow-hidden rounded-3xl border border-border/70 bg-card shadow-soft">
            <div className="p-6 pb-3">
              <h2 className="font-display text-xl font-bold">Ubicación</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                {school.comuna}, Región de {school.region}
              </p>
            </div>
            <div className="h-72">
              <SchoolMap schools={[school]} activeId={school.id} zoom={13} />
            </div>
          </section>
        </div>

        {/* sidebar */}
        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          <div className="rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
            <h3 className="font-display text-lg font-bold">Características</h3>
            <ul className="mt-4 space-y-3">
              {school.features.map((f) => (
                <li key={f} className="flex items-start gap-3 text-sm">
                  <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full bg-success/15 text-success">
                    <Check className="size-3.5" />
                  </span>
                  {f}
                </li>
              ))}
            </ul>

            <button
              type="button"
              onClick={() => toggleCompare(school.id)}
              className={cn(
                'mt-6 inline-flex w-full items-center justify-center gap-2 rounded-2xl px-4 py-3 text-sm font-semibold transition-all',
                inCompare
                  ? 'bg-success text-success-foreground'
                  : 'bg-primary text-primary-foreground shadow-soft hover:shadow-glow hover:brightness-110'
              )}
            >
              {inCompare ? <Check className="size-4" /> : <Plus className="size-4" />}
              {inCompare ? 'En el comparador' : 'Agregar a comparar'}
            </button>
            <Link
              href="/comparar"
              className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-border px-4 py-3 text-sm font-semibold transition-colors hover:bg-secondary"
            >
              <Scale className="size-4" />
              Ir al comparador
            </Link>
          </div>
        </aside>
      </div>
    </div>
  )
}
