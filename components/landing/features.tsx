'use client'

import { motion } from 'framer-motion'
import { Map, Scale, ShieldCheck, Sparkles, TrendingUp } from 'lucide-react'

export function Features() {
  return (
    <section className="px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-primary">
            Por qué AcademyMap
          </p>
          <h2 className="mt-3 text-balance font-display text-3xl font-extrabold tracking-tight sm:text-4xl">
            Todo lo que necesitas para decidir con confianza
          </h2>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          <Card
            className="md:col-span-2"
            icon={Sparkles}
            title="Test inteligente y cercano"
            desc="Un cuestionario diseñado con psicólogos para adolescentes: motivador, claro y sin presión. Cada respuesta ajusta tu perfil vocacional en tiempo real."
            delay={0}
          >
            <div className="mt-5 grid grid-cols-3 gap-2">
              {[92, 68, 54].map((v, i) => (
                <div key={i} className="rounded-2xl bg-secondary p-3">
                  <div className="flex h-20 items-end">
                    <div
                      className="w-full rounded-lg bg-primary"
                      style={{ height: `${v}%` }}
                    />
                  </div>
                  <p className="mt-2 text-center text-xs font-semibold text-muted-foreground">
                    {v}%
                  </p>
                </div>
              ))}
            </div>
          </Card>

          <Card
            icon={Map}
            title="Mapa interactivo"
            desc="Ubica cada liceo en el mapa y descubre cuáles están cerca de ti."
            delay={0.1}
          />
          <Card
            icon={Scale}
            title="Comparador lado a lado"
            desc="Compara especialidades, empleabilidad y características de hasta tres liceos."
            delay={0.15}
          />
          <Card
            icon={TrendingUp}
            title="Datos de empleabilidad"
            desc="Información real de titulación y continuidad de estudios por especialidad."
            delay={0.2}
          />
          <Card
            icon={ShieldCheck}
            title="Gratis y confiable"
            desc="Sin costo para estudiantes y familias, con datos verificados de cada establecimiento."
            delay={0.25}
          />
        </div>
      </div>
    </section>
  )
}

function Card({
  icon: Icon,
  title,
  desc,
  children,
  className = '',
  delay = 0,
}: {
  icon: React.ElementType
  title: string
  desc: string
  children?: React.ReactNode
  className?: string
  delay?: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.45, delay }}
      className={`group rounded-3xl border border-border/70 bg-card p-6 shadow-soft transition-all hover:-translate-y-1 hover:shadow-float ${className}`}
    >
      <div className="flex size-11 items-center justify-center rounded-2xl bg-primary/10 text-primary transition-transform group-hover:scale-110">
        <Icon className="size-5" aria-hidden="true" />
      </div>
      <h3 className="mt-4 font-display text-lg font-bold">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{desc}</p>
      {children}
    </motion.div>
  )
}
