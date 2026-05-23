import { AuthPlaceholder } from '../components/AuthPlaceholder'

const features = [
  {
    title: 'Vite + React + TypeScript',
    body: 'Compilación rápida, tipado estricto y plantilla alineada con el ecosistema actual de Vite 8.',
  },
  {
    title: 'Module Federation (remote)',
    body: (
      <>
        Nombre del remote: <span className="st-inline-code">boogiepopRemote</span>. Expone{' '}
        <span className="st-inline-code">./Shell</span> para que el host lo cargue con el runtime
        MF (manifest o <span className="st-inline-code">remoteEntry.js</span>
        ).
      </>
    ),
  },
  {
    title: 'Tailwind CSS',
    body: 'Estilos con tokens tipo Streamlit definidos en `src/index.css` (tema claro).',
  },
  {
    title: 'React Router',
    body: (
      <>
        Una sola vista en la raíz. Sin navbar propia: el chrome va en el host. Integrado en el hub,
        las rutas se resuelven como <span className="st-inline-code">Routes</span> descendiente bajo{' '}
        <span className="st-inline-code">/hub/react-remote/*</span> (sin segundo{' '}
        <span className="st-inline-code">Router</span> anidado, que RR v6 prohíbe).
      </>
    ),
  },
]

/** Intro + documentación del seed en una única página. */
export function SeedLandingPage() {
  return (
    <div className="space-y-12 text-left">
      <header className="space-y-4">
        <h1 className="text-[1.75rem] font-semibold text-st-body sm:text-[2rem]">
          Remote Vite + React
        </h1>
        <p className="max-w-2xl text-[1rem] leading-relaxed text-st-muted-text">
          Este repositorio es un <strong className="text-st-body">seed</strong> listo para
          publicar como <strong className="text-st-body">remote</strong> de Module Federation. En
          local corre como SPA en una sola vista; si lo montás como{' '}
          <span className="st-inline-code">boogiepopRemote/Shell</span>, todo lo que ves abajo forma
          parte de ese mismo módulo.
        </p>
        <div className="flex flex-wrap gap-3">
          <a href="#detalle-del-seed" className="st-btn-primary">
            Ver detalle del seed
          </a>
          <a
            href="https://github.com/module-federation/vite"
            target="_blank"
            rel="noreferrer"
            className="st-btn-secondary"
          >
            Documentación MF + Vite
          </a>
        </div>
      </header>

      <section
        id="detalle-del-seed"
        className="scroll-mt-10 space-y-6"
        aria-labelledby="detalle-titulo"
      >
        <div className="space-y-2">
          <h2 id="detalle-titulo" className="text-[1.375rem] font-semibold text-st-body">
            Contenido del seed
          </h2>
          <p className="max-w-2xl text-[1rem] leading-relaxed text-st-muted-text">
            Resumen para quien clone el repo o consuma el remote desde un host.
          </p>
        </div>

        <ul className="space-y-4">
          {features.map((item) => (
            <li
              key={item.title}
              className="rounded-[0.5rem] border border-st-border bg-st-muted-bg/80 p-5"
            >
              <h3 className="text-lg font-semibold text-st-body">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-st-muted-text">{item.body}</p>
            </li>
          ))}
        </ul>

        <AuthPlaceholder />

        <div className="rounded-[0.5rem] border border-st-border border-l-[6px] border-l-st-primary bg-st-muted-bg/50 p-5 text-sm text-st-muted-text">
          <p className="font-semibold text-st-body">Despliegue</p>
          <p className="mt-2 leading-relaxed">
            Imagen Docker (nginx + estáticos de <span className="st-inline-code">dist</span>
            ), push a ECR y servicio ECS. Ver{' '}
            <span className="st-inline-code">README.md</span> y{' '}
            <span className="st-inline-code">.github/workflows</span>.
          </p>
        </div>
      </section>
    </div>
  )
}
