'use client'

import { motion } from 'framer-motion'
import { AREAS } from '@/lib/data'
import { AreaIcon } from '@/components/area-icon'

export function AreasSection() {
  const areas = Object.values(AREAS)
  return (
    <section className="px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-primary">
            Áreas técnico-profesionales
          </p>
          <h2 className="mt-3 text-balance font-display text-3xl font-extrabold tracking-tight sm:text-4xl">
            Explora todos los caminos posibles
          </h2>
          <p className="mt-4 text-pretty text-muted-foreground">
            El sistema técnico-profesional ofrece decenas de especialidades. Estas son las
            grandes áreas que evaluamos en tu test.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {areas.map((area, i) => (
            <motion.div
              key={area.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.4, delay: i * 0.05 }}
              className="group relative overflow-hidden rounded-3xl border border-border/70 bg-card p-5 shadow-soft transition-all hover:-translate-y-1 hover:shadow-float"
            >
              <div
                className="flex size-12 items-center justify-center rounded-2xl transition-transform group-hover:scale-110"
                style={{ backgroundColor: `color-mix(in oklch, ${area.color} 16%, transparent)` }}
              >
                <AreaIcon icon={area.icon} className="size-6" />
              </div>
              <h3 className="mt-4 font-display text-base font-bold leading-tight">
                {area.name}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {area.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
