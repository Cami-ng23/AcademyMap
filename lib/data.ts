export type AreaId =
  | 'tecnologia'
  | 'industrial'
  | 'salud'
  | 'gastronomia'
  | 'agro'
  | 'administracion'
  | 'construccion'
  | 'electricidad'

export type Area = {
  id: AreaId
  name: string
  icon: string
  color: string
  description: string
}

export const AREAS: Record<AreaId, Area> = {
  tecnologia: {
    id: 'tecnologia',
    name: 'Tecnología e Informática',
    icon: 'Cpu',
    color: 'oklch(0.54 0.21 264)',
    description: 'Programación, redes, soporte y desarrollo de software.',
  },
  industrial: {
    id: 'industrial',
    name: 'Industrial y Mecánica',
    icon: 'Wrench',
    color: 'oklch(0.62 0.14 200)',
    description: 'Mecánica, mecatrónica y mantenimiento industrial.',
  },
  salud: {
    id: 'salud',
    name: 'Salud y Bienestar',
    icon: 'HeartPulse',
    color: 'oklch(0.65 0.19 25)',
    description: 'Atención de enfermería, laboratorio y cuidado de personas.',
  },
  gastronomia: {
    id: 'gastronomia',
    name: 'Gastronomía y Turismo',
    icon: 'Utensils',
    color: 'oklch(0.83 0.16 85)',
    description: 'Cocina, servicios de turismo y hotelería.',
  },
  agro: {
    id: 'agro',
    name: 'Agropecuario',
    icon: 'Leaf',
    color: 'oklch(0.72 0.17 158)',
    description: 'Agricultura, ganadería y recursos naturales.',
  },
  administracion: {
    id: 'administracion',
    name: 'Administración y Comercio',
    icon: 'Briefcase',
    color: 'oklch(0.58 0.12 300)',
    description: 'Contabilidad, administración y logística.',
  },
  construccion: {
    id: 'construccion',
    name: 'Construcción',
    icon: 'HardHat',
    color: 'oklch(0.6 0.13 55)',
    description: 'Edificación, obras civiles y dibujo técnico.',
  },
  electricidad: {
    id: 'electricidad',
    name: 'Electricidad y Electrónica',
    icon: 'Zap',
    color: 'oklch(0.7 0.16 95)',
    description: 'Instalaciones eléctricas, electrónica y telecomunicaciones.',
  },
}

export type QuizOption = {
  label: string
  emoji?: string
  weights: Partial<Record<AreaId, number>>
}

export type QuizQuestion = {
  id: string
  question: string
  helper: string
  options: QuizOption[]
}

export const QUESTIONS: QuizQuestion[] = [
  {
    id: 'q1',
    question: '¿Qué actividad disfrutas más en tu tiempo libre?',
    helper: 'Elige la que más se acerca a ti.',
    options: [
      { label: 'Armar o reparar cosas', weights: { industrial: 3, construccion: 2, electricidad: 1 } },
      { label: 'Usar el computador y crear', weights: { tecnologia: 3, administracion: 1 } },
      { label: 'Cocinar o compartir con gente', weights: { gastronomia: 3, salud: 1 } },
      { label: 'Estar al aire libre y con la naturaleza', weights: { agro: 3, construccion: 1 } },
    ],
  },
  {
    id: 'q2',
    question: '¿Cuál de estas materias se te da mejor?',
    helper: 'Piensa en dónde te sientes con más confianza.',
    options: [
      { label: 'Matemáticas y lógica', weights: { tecnologia: 2, electricidad: 2, administracion: 1 } },
      { label: 'Ciencias naturales y biología', weights: { salud: 3, agro: 1 } },
      { label: 'Tecnología y talleres', weights: { industrial: 2, electricidad: 2 } },
      { label: 'Lenguaje y trabajo en equipo', weights: { administracion: 2, gastronomia: 1, salud: 1 } },
    ],
  },
  {
    id: 'q3',
    question: '¿Cómo te gustaría que fuera tu trabajo ideal?',
    helper: 'Imagina cómo sería tu día a día.',
    options: [
      { label: 'Frente a una pantalla resolviendo problemas', weights: { tecnologia: 3, administracion: 1 } },
      { label: 'En terreno, usando herramientas', weights: { industrial: 2, construccion: 2, electricidad: 1 } },
      { label: 'Ayudando y cuidando a otras personas', weights: { salud: 3, gastronomia: 1 } },
      { label: 'Al aire libre o con animales y plantas', weights: { agro: 3 } },
    ],
  },
  {
    id: 'q4',
    question: '¿Qué habilidad crees que es tu superpoder?',
    helper: 'No hay respuestas incorrectas.',
    options: [
      { label: 'Ser ordenado y planificar', weights: { administracion: 3, construccion: 1 } },
      { label: 'Ser creativo con las manos', weights: { gastronomia: 2, industrial: 1, construccion: 1 } },
      { label: 'Entender cómo funcionan las máquinas', weights: { electricidad: 2, industrial: 2 } },
      { label: 'Aprender tecnología rápidamente', weights: { tecnologia: 3 } },
    ],
  },
  {
    id: 'q5',
    question: '¿Qué proyecto te emocionaría más realizar?',
    helper: 'Elige el que te haría decir "¡quiero hacer eso!".',
    options: [
      { label: 'Crear una app o página web', weights: { tecnologia: 3 } },
      { label: 'Diseñar el plano de una casa', weights: { construccion: 3, administracion: 1 } },
      { label: 'Preparar un banquete para un evento', weights: { gastronomia: 3 } },
      { label: 'Cultivar un huerto sustentable', weights: { agro: 3 } },
    ],
  },
  {
    id: 'q6',
    question: '¿En qué tipo de ambiente rindes mejor?',
    helper: 'Piensa en dónde te concentras y disfrutas.',
    options: [
      { label: 'Un laboratorio o clínica', weights: { salud: 3 } },
      { label: 'Un taller con máquinas', weights: { industrial: 2, electricidad: 2 } },
      { label: 'Una oficina organizada', weights: { administracion: 3 } },
      { label: 'Una cocina o restaurante', weights: { gastronomia: 3 } },
    ],
  },
]

export type Specialty = { area: AreaId; name: string }

export type School = {
  id: string
  name: string
  shortName: string
  comuna: string
  region: string
  lat: number
  lng: number
  rating: number
  students: number
  free: boolean
  dependency: 'Municipal' | 'Particular Subvencionado' | 'Servicio Local'
  image: string
  description: string
  areas: AreaId[]
  specialties: string[]
  features: string[]
  admissionRate: number
  employability: number
}

export const SCHOOLS: School[] = [
  {
    id: 'insel',
    name: 'Liceo Industrial Superior de Electrotecnia',
    shortName: 'Liceo Industrial de Electrotecnia',
    comuna: 'Santiago',
    region: 'Metropolitana',
    lat: -33.4489,
    lng: -70.6693,
    rating: 4.7,
    students: 1240,
    free: true,
    dependency: 'Municipal',
    image: '/schools/school-tech.png',
    description:
      'Referente nacional en formación técnica industrial con laboratorios de última generación y fuertes convenios con la industria eléctrica.',
    areas: ['electricidad', 'industrial', 'tecnologia'],
    specialties: ['Electricidad', 'Electrónica', 'Telecomunicaciones', 'Mecatrónica'],
    features: ['Laboratorios equipados', 'Práctica profesional garantizada', 'Certificación técnica', 'Talleres extendidos'],
    admissionRate: 62,
    employability: 88,
  },
  {
    id: 'ltp-valpo',
    name: 'Liceo Técnico Profesional Valparaíso',
    shortName: 'LTP Valparaíso',
    comuna: 'Valparaíso',
    region: 'Valparaíso',
    lat: -33.0472,
    lng: -71.6127,
    rating: 4.4,
    students: 980,
    free: true,
    dependency: 'Servicio Local',
    image: '/schools/school-gastro.png',
    description:
      'Especializado en gastronomía y turismo, aprovecha la identidad porteña para formar profesionales de la hotelería y los servicios.',
    areas: ['gastronomia', 'administracion'],
    specialties: ['Gastronomía', 'Servicios de Turismo', 'Administración', 'Atención de Párvulos'],
    features: ['Cocina profesional', 'Convenios hoteleros', 'Inglés técnico', 'Emprendimiento'],
    admissionRate: 74,
    employability: 79,
  },
  {
    id: 'lca-sur',
    name: 'Liceo Agrícola del Valle Central',
    shortName: 'Liceo Agrícola Valle Central',
    comuna: 'Rancagua',
    region: "O'Higgins",
    lat: -34.1708,
    lng: -70.7444,
    rating: 4.5,
    students: 640,
    free: true,
    dependency: 'Municipal',
    image: '/schools/school-agro.png',
    description:
      'Campus rural con predio productivo propio. Forma técnicos agropecuarios con enfoque en sustentabilidad e innovación agrícola.',
    areas: ['agro'],
    specialties: ['Agropecuaria', 'Vitivinicultura', 'Recursos Naturales'],
    features: ['Predio productivo', 'Internado disponible', 'Proyectos sustentables', 'Maquinaria agrícola'],
    admissionRate: 81,
    employability: 76,
  },
  {
    id: 'lts-concepcion',
    name: 'Liceo Técnico de Salud Concepción',
    shortName: 'Liceo de Salud Concepción',
    comuna: 'Concepción',
    region: 'Biobío',
    lat: -36.8201,
    lng: -73.0444,
    rating: 4.6,
    students: 1120,
    free: false,
    dependency: 'Particular Subvencionado',
    image: '/schools/school-health.png',
    description:
      'Formación en el área de la salud con simulación clínica y convenios con hospitales de la región del Biobío.',
    areas: ['salud'],
    specialties: ['Atención de Enfermería', 'Laboratorio Clínico', 'Atención de Párvulos'],
    features: ['Simulación clínica', 'Convenios hospitalarios', 'Uniforme incluido', 'Beca de excelencia'],
    admissionRate: 58,
    employability: 84,
  },
  {
    id: 'lpt-antofagasta',
    name: 'Liceo Politécnico de Antofagasta',
    shortName: 'Politécnico Antofagasta',
    comuna: 'Antofagasta',
    region: 'Antofagasta',
    lat: -23.6509,
    lng: -70.3975,
    rating: 4.3,
    students: 1580,
    free: true,
    dependency: 'Servicio Local',
    image: '/schools/school-industrial.png',
    description:
      'Vinculado a la industria minera del norte, ofrece especialidades industriales con alta empleabilidad y prácticas remuneradas.',
    areas: ['industrial', 'electricidad', 'construccion'],
    specialties: ['Mecánica Industrial', 'Construcciones Metálicas', 'Electricidad', 'Explotación Minera'],
    features: ['Convenios mineros', 'Prácticas remuneradas', 'Equipamiento pesado', 'Alta empleabilidad'],
    admissionRate: 69,
    employability: 91,
  },
  {
    id: 'lti-temuco',
    name: 'Liceo de Tecnología e Innovación Temuco',
    shortName: 'Liceo Tecnológico Temuco',
    comuna: 'Temuco',
    region: 'La Araucanía',
    lat: -38.7359,
    lng: -72.5904,
    rating: 4.8,
    students: 860,
    free: true,
    dependency: 'Municipal',
    image: '/schools/school-tech2.png',
    description:
      'Enfocado en programación y desarrollo digital, con un ecosistema maker y participación destacada en ferias tecnológicas.',
    areas: ['tecnologia', 'administracion'],
    specialties: ['Programación', 'Conectividad y Redes', 'Administración', 'Diseño Digital'],
    features: ['Laboratorio maker', 'Impresoras 3D', 'Club de robótica', 'Certificación internacional'],
    admissionRate: 55,
    employability: 86,
  },
]

export function getSchool(id: string) {
  return SCHOOLS.find((s) => s.id === id)
}
