'use client'

import { motion } from 'framer-motion'
import { ClipboardList, Compass, GraduationCap } from 'lucide-react'

const STEPS = [
  {
    icon: ClipboardList,
    title: 'Responde el test',
    desc: 'Seis preguntas simples sobre tus gustos, habilidades y sueños. Sin respuestas correctas ni incorrectas.',
  },
  {
    icon: Compass,
    title: 'Recibe tu perfil',
    desc: 'Calculamos tus áreas afines y te mostramos qué especialidades encajan mejor contigo.',
  },
  {
    icon: GraduationCap,
    title: 'Encuentra tu liceo',
    desc: 'Explora, compara y ubica en el mapa los liceos técnicos que se ajustan a tu perfil.',
  },
]

export function HowItWorks() {
  return (
    <section className="px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-primary">
            Cómo funciona
          </p>
          <h2 className="mt-3 text-balance font-display text-3xl font-extrabold tracking-tight sm:text-4xl">
            Tu orientación en tres pasos
          </h2>
        </div>

        <div className="relative mt-14 grid gap-6 md:grid-cols-3">
          <div className="pointer-events-none absolute inset-x-[16%] top-9 hidden h-px bg-gradient-to-r from-transparent via-border to-transparent md:block" />
          {STEPS.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.12 }}
              className="relative rounded-3xl border border-border/70 bg-card p-6 text-center shadow-soft"
            >
              <div className="mx-auto flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                <step.icon className="size-7" aria-hidden="true" />
              </div>
              <span className="mt-4 inline-block rounded-full bg-secondary px-3 py-1 text-xs font-bold text-secondary-foreground">
                Paso {i + 1}
              </span>
              <h3 className="mt-3 font-display text-xl font-bold">{step.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
