'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, Compass, MapPin, Sparkles, Star } from 'lucide-react'

export function Hero() {
  return (
    <section className="relative overflow-hidden px-4 pt-32 pb-16 sm:pt-40">
      {/* ambient background */}
      <div className="pointer-events-none absolute inset-0 -z-10 bg-grid [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_60%,transparent_100%)]" />
      <div className="pointer-events-none absolute -top-24 left-1/2 -z-10 h-[420px] w-[820px] -translate-x-1/2 rounded-full bg-primary/20 blur-[120px]" />
      <div className="pointer-events-none absolute top-40 right-0 -z-10 h-72 w-72 rounded-full bg-success/20 blur-[110px]" />

      <div className="mx-auto max-w-3xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mx-auto inline-flex items-center gap-2 rounded-full glass px-4 py-1.5 text-sm font-medium shadow-soft"
        >
          <Sparkles className="size-4 text-primary" aria-hidden="true" />
          Orientación vocacional para 8° básico
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.05 }}
          className="mt-6 text-balance font-display text-4xl font-extrabold leading-[1.05] tracking-tight sm:text-6xl"
        >
          Descubre el <span className="text-gradient">liceo técnico</span> hecho para ti
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.12 }}
          className="mx-auto mt-5 max-w-xl text-pretty text-lg leading-relaxed text-muted-foreground"
        >
          Responde un test breve y divertido, y AcademyMap te mostrará los liceos
          técnico-profesionales que mejor se adaptan a tus intereses y talentos.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.18 }}
          className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row"
        >
          <Link
            href="/quiz"
            className="group inline-flex items-center gap-2 rounded-2xl bg-primary px-6 py-3.5 text-base font-semibold text-primary-foreground shadow-glow transition-all hover:brightness-110"
          >
            Comenzar mi test
            <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <Link
            href="/liceos"
            className="inline-flex items-center gap-2 rounded-2xl glass px-6 py-3.5 text-base font-semibold shadow-soft transition-all hover:shadow-float"
          >
            <MapPin className="size-4 text-primary" />
            Explorar liceos
          </Link>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-6 flex items-center justify-center gap-2 text-sm text-muted-foreground"
        >
          <div className="flex">
            {[0, 1, 2, 3, 4].map((i) => (
              <Star key={i} className="size-4 fill-highlight text-highlight" aria-hidden="true" />
            ))}
          </div>
          Recomendado por orientadores de más de 40 establecimientos
        </motion.div>
      </div>

      <HeroPreview />
    </section>
  )
}

function HeroPreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.7, delay: 0.25 }}
      className="relative mx-auto mt-16 max-w-4xl"
    >
      <div className="glass-strong rounded-[2rem] p-3 shadow-float sm:p-4">
        <div className="rounded-3xl border border-border/60 bg-card/80 p-5 sm:p-8">
          <div className="flex items-center gap-2">
            <span className="size-3 rounded-full bg-destructive/70" />
            <span className="size-3 rounded-full bg-highlight" />
            <span className="size-3 rounded-full bg-success" />
            <span className="ml-3 text-xs font-medium text-muted-foreground">
              academymap.cl / resultado
            </span>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl bg-primary p-5 text-primary-foreground shadow-glow sm:col-span-1">
              <Compass className="size-6" aria-hidden="true" />
              <p className="mt-3 text-sm/relaxed opacity-90">Tu área destacada</p>
              <p className="font-display text-xl font-bold">Tecnología</p>
              <div className="mt-3 h-2 rounded-full bg-primary-foreground/25">
                <div className="h-2 w-[92%] rounded-full bg-primary-foreground" />
              </div>
              <p className="mt-2 text-xs opacity-90">92% de coincidencia</p>
            </div>

            <div className="space-y-3 sm:col-span-2">
              {[
                { name: 'Liceo Tecnológico Temuco', match: 92 },
                { name: 'Liceo Industrial de Electrotecnia', match: 84 },
                { name: 'Politécnico Antofagasta', match: 71 },
              ].map((s, i) => (
                <motion.div
                  key={s.name}
                  initial={{ opacity: 0, x: 12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + i * 0.12 }}
                  className="flex items-center gap-3 rounded-2xl border border-border/60 bg-background/60 p-3"
                >
                  <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-secondary text-sm font-bold">
                    {i + 1}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold">{s.name}</p>
                    <div className="mt-1.5 h-1.5 rounded-full bg-secondary">
                      <div
                        className="h-1.5 rounded-full bg-success"
                        style={{ width: `${s.match}%` }}
                      />
                    </div>
                  </div>
                  <span className="text-sm font-bold text-success">{s.match}%</span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <motion.div
        animate={{ y: [0, -12, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute -right-4 -top-6 hidden rounded-2xl glass-strong px-4 py-3 shadow-float sm:block"
      >
        <p className="text-xs text-muted-foreground">Coincidencia</p>
        <p className="font-display text-2xl font-bold text-success">92%</p>
      </motion.div>
    </motion.div>
  )
}
