const STATS = [
  { value: '+250', label: 'Liceos técnicos en Chile' },
  { value: '35', label: 'Especialidades disponibles' },
  { value: '6', label: 'Preguntas en el test' },
  { value: '100%', label: 'Gratis para estudiantes' },
]

export function StatsBar() {
  return (
    <section className="px-4">
      <div className="mx-auto grid max-w-5xl grid-cols-2 gap-4 rounded-3xl border border-border/70 bg-card px-6 py-8 shadow-soft sm:grid-cols-4">
        {STATS.map((s) => (
          <div key={s.label} className="text-center">
            <p className="font-display text-3xl font-extrabold text-primary sm:text-4xl">
              {s.value}
            </p>
            <p className="mt-1 text-xs leading-snug text-muted-foreground sm:text-sm">
              {s.label}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}
