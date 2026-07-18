'use client'

import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowLeft, ArrowRight, Check, Compass, Loader2 } from 'lucide-react'
import { QUESTIONS } from '@/lib/data'
import { useQuiz } from '@/components/quiz-provider'
import { cn } from '@/lib/utils'

export function QuizFlow() {
  const router = useRouter()
  const { answers, setAnswer, setCompleted } = useQuiz()
  const [step, setStep] = useState(0)
  const [dir, setDir] = useState(1)
  const [submitting, setSubmitting] = useState(false)

  const question = QUESTIONS[step]
  const total = QUESTIONS.length
  const selected = answers[question.id]
  const progress = useMemo(
    () => Math.round(((step + (selected !== undefined ? 1 : 0)) / total) * 100),
    [step, selected, total]
  )
  const isLast = step === total - 1

  const goNext = () => {
    if (selected === undefined) return
    if (isLast) {
      setSubmitting(true)
      setCompleted(true)
      setTimeout(() => router.push('/resultados'), 900)
      return
    }
    setDir(1)
    setStep((s) => s + 1)
  }

  const goPrev = () => {
    if (step === 0) return
    setDir(-1)
    setStep((s) => s - 1)
  }

  return (
    <div className="mx-auto flex min-h-[100svh] max-w-2xl flex-col px-4 pb-10 pt-24">
      {/* top bar */}
      <div className="flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          <Compass className="size-4 text-primary" />
          AcademyMap
        </Link>
        <span className="rounded-full bg-secondary px-3 py-1 text-xs font-semibold text-secondary-foreground">
          Pregunta {step + 1} de {total}
        </span>
      </div>

      {/* progress */}
      <div className="mt-4">
        <div className="h-2.5 w-full overflow-hidden rounded-full bg-secondary">
          <motion.div
            className="h-full rounded-full bg-primary"
            initial={false}
            animate={{ width: `${progress}%` }}
            transition={{ type: 'spring', stiffness: 120, damping: 20 }}
          />
        </div>
        <div className="mt-2 flex justify-between text-xs text-muted-foreground">
          <span>Progreso</span>
          <span className="font-semibold text-primary">{progress}%</span>
        </div>
      </div>

      {/* card */}
      <div className="relative mt-8 flex-1">
        <AnimatePresence mode="wait" custom={dir}>
          {!submitting ? (
            <motion.div
              key={question.id}
              custom={dir}
              initial={{ opacity: 0, x: dir * 60 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: dir * -60 }}
              transition={{ duration: 0.3 }}
            >
              <div className="rounded-3xl border border-border/70 bg-card p-6 shadow-float sm:p-8">
                <p className="text-sm font-semibold uppercase tracking-wider text-primary">
                  Test vocacional
                </p>
                <h1 className="mt-2 text-balance font-display text-2xl font-extrabold leading-tight tracking-tight sm:text-3xl">
                  {question.question}
                </h1>
                <p className="mt-2 text-sm text-muted-foreground">{question.helper}</p>

                <div className="mt-6 grid gap-3">
                  {question.options.map((opt, i) => {
                    const active = selected === i
                    return (
                      <motion.button
                        key={i}
                        type="button"
                        whileTap={{ scale: 0.985 }}
                        onClick={() => setAnswer(question.id, i)}
                        className={cn(
                          'group flex items-center gap-4 rounded-2xl border p-4 text-left transition-all',
                          active
                            ? 'border-primary bg-primary/8 shadow-glow'
                            : 'border-border bg-background hover:border-primary/40 hover:bg-secondary/50'
                        )}
                        aria-pressed={active}
                      >
                        <span
                          className={cn(
                            'flex size-8 shrink-0 items-center justify-center rounded-xl text-sm font-bold transition-colors',
                            active
                              ? 'bg-primary text-primary-foreground'
                              : 'bg-secondary text-secondary-foreground group-hover:bg-primary/15'
                          )}
                        >
                          {active ? <Check className="size-4" /> : String.fromCharCode(65 + i)}
                        </span>
                        <span className="text-sm font-medium sm:text-base">{opt.label}</span>
                      </motion.button>
                    )
                  })}
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center justify-center rounded-3xl border border-border/70 bg-card p-12 text-center shadow-float"
            >
              <Loader2 className="size-10 animate-spin text-primary" />
              <h2 className="mt-5 font-display text-xl font-bold">Analizando tu perfil…</h2>
              <p className="mt-2 max-w-xs text-sm text-muted-foreground">
                Estamos calculando qué liceos técnicos encajan mejor contigo.
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* nav */}
      {!submitting && (
        <div className="mt-6 flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={goPrev}
            disabled={step === 0}
            className="inline-flex items-center gap-2 rounded-2xl border border-border px-5 py-3 text-sm font-semibold transition-colors hover:bg-secondary disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ArrowLeft className="size-4" />
            Atrás
          </button>
          <button
            type="button"
            onClick={goNext}
            disabled={selected === undefined}
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-2xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-soft transition-all hover:shadow-glow hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-40 sm:flex-none"
          >
            {isLast ? 'Ver mis resultados' : 'Siguiente'}
            <ArrowRight className="size-4" />
          </button>
        </div>
      )}
    </div>
  )
}
