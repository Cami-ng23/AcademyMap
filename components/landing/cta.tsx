'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'

export function CTA() {
  return (
    <section className="px-4 py-20">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
        className="relative mx-auto max-w-5xl overflow-hidden rounded-[2.5rem] bg-primary px-6 py-14 text-center text-primary-foreground shadow-glow sm:px-12 sm:py-20"
      >
        <div className="pointer-events-none absolute -left-20 -top-20 size-64 rounded-full bg-primary-foreground/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 -right-16 size-72 rounded-full bg-primary-foreground/10 blur-3xl" />
        <h2 className="relative mx-auto max-w-2xl text-balance font-display text-3xl font-extrabold tracking-tight sm:text-4xl">
          Tu futuro empieza con una buena decisión
        </h2>
        <p className="relative mx-auto mt-4 max-w-xl text-pretty text-base/relaxed opacity-90">
          Descubre en minutos qué liceo técnico-profesional se ajusta mejor a la persona que
          quieres llegar a ser.
        </p>
        <Link
          href="/quiz"
          className="relative mt-8 inline-flex items-center gap-2 rounded-2xl bg-background px-7 py-3.5 text-base font-semibold text-foreground shadow-float transition-transform hover:scale-[1.03]"
        >
          Hacer el test gratis
          <ArrowRight className="size-4" />
        </Link>
      </motion.div>
    </section>
  )
}
