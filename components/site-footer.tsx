import Link from 'next/link'
import { Compass } from 'lucide-react'

export function SiteFooter() {
  return (
    <footer className="mt-24 border-t border-border/70">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:grid-cols-2 lg:grid-cols-4">
        <div className="space-y-3">
          <Link href="/" className="flex items-center gap-2.5">
            <span className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Compass className="size-4" aria-hidden="true" />
            </span>
            <span className="font-display text-base font-extrabold tracking-tight">
              Academy<span className="text-primary">Map</span>
            </span>
          </Link>
          <p className="max-w-xs text-sm leading-relaxed text-muted-foreground">
            Orientación vocacional para estudiantes de 8° básico que buscan su liceo
            técnico-profesional ideal en Chile.
          </p>
        </div>

        <FooterCol
          title="Plataforma"
          links={[
            { href: '/quiz', label: 'Test vocacional' },
            { href: '/liceos', label: 'Explorar liceos' },
            { href: '/comparar', label: 'Comparador' },
          ]}
        />
        <FooterCol
          title="Recursos"
          links={[
            { href: '/liceos', label: 'Mapa interactivo' },
            { href: '/admin', label: 'Panel de datos' },
            { href: '/', label: 'Preguntas frecuentes' },
          ]}
        />
        <FooterCol
          title="Proyecto"
          links={[
            { href: '/', label: 'Sobre AcademyMap' },
            { href: '/', label: 'Feria Técnico Profesional' },
            { href: '/', label: 'Contacto' },
          ]}
        />
      </div>
      <div className="border-t border-border/70">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-2 px-4 py-5 text-xs text-muted-foreground sm:flex-row">
          <p>© {new Date().getFullYear()} AcademyMap. Proyecto educativo.</p>
          <p>Hecho con dedicación para la orientación vocacional en Chile.</p>
        </div>
      </div>
    </footer>
  )
}

function FooterCol({
  title,
  links,
}: {
  title: string
  links: { href: string; label: string }[]
}) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold">{title}</h3>
      <ul className="space-y-2">
        {links.map((l) => (
          <li key={l.label}>
            <Link
              href={l.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
