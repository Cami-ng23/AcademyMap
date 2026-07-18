import {
  Briefcase,
  Cpu,
  HardHat,
  HeartPulse,
  Leaf,
  Utensils,
  Wrench,
  Zap,
  type LucideIcon,
} from 'lucide-react'
import type { AreaId } from '@/lib/data'

const MAP: Record<string, LucideIcon> = {
  Cpu,
  Wrench,
  HeartPulse,
  Utensils,
  Leaf,
  Briefcase,
  HardHat,
  Zap,
}

export function AreaIcon({
  icon,
  className,
}: {
  icon: string
  className?: string
}) {
  const Icon = MAP[icon] ?? Cpu
  return <Icon className={className} aria-hidden="true" />
}

export const AREA_ICON: Record<AreaId, string> = {
  tecnologia: 'Cpu',
  industrial: 'Wrench',
  salud: 'HeartPulse',
  gastronomia: 'Utensils',
  agro: 'Leaf',
  administracion: 'Briefcase',
  construccion: 'HardHat',
  electricidad: 'Zap',
}
