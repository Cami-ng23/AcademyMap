'use client'

import { motion } from 'framer-motion'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  GraduationCap,
  MapPin,
  TrendingUp,
  Users,
} from 'lucide-react'
import { AREAS, SCHOOLS, type AreaId } from '@/lib/data'

const testTrend = [
  { month: 'Mar', tests: 320 },
  { month: 'Abr', tests: 480 },
  { month: 'May', tests: 610 },
  { month: 'Jun', tests: 890 },
  { month: 'Jul', tests: 1240 },
  { month: 'Ago', tests: 1580 },
  { month: 'Sep', tests: 2010 },
]

const areaCounts = (Object.keys(AREAS) as AreaId[]).map((id) => ({
  name: AREAS[id].name.split(' ')[0],
  value: SCHOOLS.filter((s) => s.areas.includes(id)).length * 40 + (id.charCodeAt(0) % 7) * 15,
  color: AREAS[id].color,
}))

const regionData = Array.from(
  SCHOOLS.reduce((acc, s) => {
    acc.set(s.region, (acc.get(s.region) ?? 0) + s.students)
    return acc
  }, new Map<string, number>()),
).map(([region, students]) => ({ region, students }))

const KPIS = [
  { label: 'Tests completados', value: '7.130', delta: '+18%', icon: GraduationCap },
  { label: 'Liceos registrados', value: SCHOOLS.length.toString(), delta: '+2', icon: MapPin },
  {
    label: 'Estudiantes activos',
    value: SCHOOLS.reduce((a, s) => a + s.students, 0).toLocaleString('es-CL'),
    delta: '+9%',
    icon: Users,
  },
  { label: 'Match promedio', value: '82%', delta: '+3%', icon: TrendingUp },
]

function ChartCard({
  title,
  subtitle,
  children,
  delay = 0,
}: {
  title: string
  subtitle: string
  children: React.ReactNode
  delay?: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="rounded-3xl border border-border/70 bg-card p-5 shadow-soft"
    >
      <div className="mb-4">
        <h3 className="font-display text-lg font-bold">{title}</h3>
        <p className="text-sm text-muted-foreground">{subtitle}</p>
      </div>
      {children}
    </motion.div>
  )
}

export function AdminDashboard() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10 md:py-14">
      <div className="flex flex-col gap-2">
        <span className="inline-flex w-fit items-center gap-2 rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
          Panel administrativo
        </span>
        <h1 className="text-balance font-display text-3xl font-bold md:text-4xl">
          Resumen de la plataforma
        </h1>
        <p className="text-muted-foreground">
          Métricas de uso, tendencias del test vocacional y distribución de liceos.
        </p>
      </div>

      <div className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {KPIS.map((kpi, i) => (
          <motion.div
            key={kpi.label}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: i * 0.06 }}
            className="rounded-3xl border border-border/70 bg-card p-5 shadow-soft"
          >
            <div className="flex items-center justify-between">
              <div className="grid size-10 place-items-center rounded-xl bg-primary/10 text-primary">
                <kpi.icon className="size-5" />
              </div>
              <span className="rounded-full bg-success/15 px-2 py-0.5 text-xs font-semibold text-success">
                {kpi.delta}
              </span>
            </div>
            <p className="mt-4 font-display text-2xl font-bold">{kpi.value}</p>
            <p className="text-sm text-muted-foreground">{kpi.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ChartCard
            title="Tests completados por mes"
            subtitle="Crecimiento del uso del test vocacional"
            delay={0.1}
          >
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={testTrend} margin={{ left: -20, right: 8, top: 8 }}>
                <defs>
                  <linearGradient id="fillTests" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-primary)" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="var(--color-primary)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                <XAxis dataKey="month" stroke="var(--color-muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--color-muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    borderRadius: 14,
                    border: '1px solid var(--color-border)',
                    background: 'var(--color-popover)',
                    color: 'var(--color-popover-foreground)',
                    fontSize: 13,
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="tests"
                  stroke="var(--color-primary)"
                  strokeWidth={2.5}
                  fill="url(#fillTests)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        <ChartCard
          title="Áreas de interés"
          subtitle="Distribución de resultados del test"
          delay={0.15}
        >
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={areaCounts}
                dataKey="value"
                nameKey="name"
                innerRadius={55}
                outerRadius={90}
                paddingAngle={3}
                stroke="none"
              >
                {areaCounts.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  borderRadius: 14,
                  border: '1px solid var(--color-border)',
                  background: 'var(--color-popover)',
                  color: 'var(--color-popover-foreground)',
                  fontSize: 13,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-x-4 gap-y-1.5">
            {areaCounts.slice(0, 6).map((a) => (
              <span key={a.name} className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="size-2.5 rounded-full" style={{ backgroundColor: a.color }} />
                {a.name}
              </span>
            ))}
          </div>
        </ChartCard>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ChartCard
            title="Estudiantes por región"
            subtitle="Cobertura de liceos registrados"
            delay={0.2}
          >
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={regionData} margin={{ left: -20, right: 8, top: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
                <XAxis dataKey="region" stroke="var(--color-muted-foreground)" fontSize={11} tickLine={false} axisLine={false} interval={0} angle={-12} textAnchor="end" height={50} />
                <YAxis stroke="var(--color-muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip
                  cursor={{ fill: 'var(--color-secondary)' }}
                  contentStyle={{
                    borderRadius: 14,
                    border: '1px solid var(--color-border)',
                    background: 'var(--color-popover)',
                    color: 'var(--color-popover-foreground)',
                    fontSize: 13,
                  }}
                />
                <Bar dataKey="students" fill="var(--color-primary)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        <ChartCard title="Liceos destacados" subtitle="Mejor empleabilidad" delay={0.25}>
          <ul className="flex flex-col gap-3">
            {[...SCHOOLS]
              .sort((a, b) => b.employability - a.employability)
              .slice(0, 5)
              .map((s, i) => (
                <li key={s.id} className="flex items-center gap-3">
                  <span className="grid size-7 shrink-0 place-items-center rounded-lg bg-secondary text-xs font-bold text-secondary-foreground">
                    {i + 1}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold">{s.shortName}</p>
                    <p className="text-xs text-muted-foreground">{s.comuna}</p>
                  </div>
                  <span className="rounded-full bg-success/15 px-2 py-0.5 text-xs font-bold text-success">
                    {s.employability}%
                  </span>
                </li>
              ))}
          </ul>
        </ChartCard>
      </div>
    </div>
  )
}
