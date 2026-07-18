'use client'

import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'
import type { Answers } from '@/lib/quiz'

type QuizContextValue = {
  answers: Answers
  setAnswer: (questionId: string, optionIndex: number) => void
  reset: () => void
  completed: boolean
  setCompleted: (v: boolean) => void
  compare: string[]
  toggleCompare: (id: string) => void
}

const QuizContext = createContext<QuizContextValue | null>(null)

export function QuizProvider({ children }: { children: ReactNode }) {
  const [answers, setAnswers] = useState<Answers>({})
  const [completed, setCompleted] = useState(false)
  const [compare, setCompare] = useState<string[]>([])

  const value = useMemo<QuizContextValue>(
    () => ({
      answers,
      setAnswer: (questionId, optionIndex) =>
        setAnswers((prev) => ({ ...prev, [questionId]: optionIndex })),
      reset: () => {
        setAnswers({})
        setCompleted(false)
      },
      completed,
      setCompleted,
      compare,
      toggleCompare: (id) =>
        setCompare((prev) =>
          prev.includes(id)
            ? prev.filter((x) => x !== id)
            : prev.length >= 3
              ? prev
              : [...prev, id]
        ),
    }),
    [answers, completed, compare]
  )

  return <QuizContext.Provider value={value}>{children}</QuizContext.Provider>
}

export function useQuiz() {
  const ctx = useContext(QuizContext)
  if (!ctx) throw new Error('useQuiz must be used within QuizProvider')
  return ctx
}
