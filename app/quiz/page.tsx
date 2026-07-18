import { QuizFlow } from '@/components/quiz/quiz-flow'

export default function QuizPage() {
  return (
    <main className="relative">
      <div className="pointer-events-none fixed inset-0 -z-10 bg-grid [mask-image:radial-gradient(ellipse_50%_50%_at_50%_0%,#000_50%,transparent_100%)]" />
      <div className="pointer-events-none fixed -top-24 left-1/2 -z-10 h-96 w-[700px] -translate-x-1/2 rounded-full bg-primary/15 blur-[120px]" />
      <QuizFlow />
    </main>
  )
}
