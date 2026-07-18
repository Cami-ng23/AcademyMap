import { AREAS, type AreaId, QUESTIONS, SCHOOLS, type School } from './data'

export type Answers = Record<string, number> // questionId -> option index

export function scoreAreas(answers: Answers): { area: AreaId; score: number }[] {
  const totals = {} as Record<AreaId, number>
  ;(Object.keys(AREAS) as AreaId[]).forEach((a) => (totals[a] = 0))

  for (const q of QUESTIONS) {
    const idx = answers[q.id]
    if (idx === undefined) continue
    const opt = q.options[idx]
    if (!opt) continue
    for (const [area, w] of Object.entries(opt.weights)) {
      totals[area as AreaId] += w ?? 0
    }
  }

  const max = Math.max(1, ...Object.values(totals))
  return (Object.keys(totals) as AreaId[])
    .map((area) => ({ area, score: Math.round((totals[area] / max) * 100) }))
    .sort((a, b) => b.score - a.score)
}

export function matchSchools(
  answers: Answers
): { school: School; match: number; topAreas: AreaId[] }[] {
  const ranked = scoreAreas(answers)
  const topAreas = ranked.slice(0, 3).map((r) => r.area)
  const areaScore = Object.fromEntries(ranked.map((r) => [r.area, r.score])) as Record<
    AreaId,
    number
  >

  return SCHOOLS.map((school) => {
    const relevant = school.areas.map((a) => areaScore[a] ?? 0)
    const base = relevant.length ? Math.max(...relevant) : 0
    const bonus = school.areas.filter((a) => topAreas.includes(a)).length * 6
    const rep = (school.rating - 4) * 8
    const match = Math.min(99, Math.round(base + bonus + rep))
    return { school, match, topAreas }
  }).sort((a, b) => b.match - a.match)
}

export const TOTAL_QUESTIONS = QUESTIONS.length
