import Image from "next/image";
import Link from "next/link";

const steps = [
  {
    number: "01",
    title: "Describe the outcome",
    text: "Start with the result you want, in your own words. Add useful actions, files, or a preferred specialist only when they help.",
  },
  {
    number: "02",
    title: "ForgeMaster prepares the flow",
    text: "ForgeMaster reviews the request, asks when something is unclear, and decides which specialist Agents should contribute and in what order.",
  },
  {
    number: "03",
    title: "Specialists do the focused work",
    text: "One Agent may be enough, or several can work in sequence or together. Each stays focused on its declared specialty.",
  },
  {
    number: "04",
    title: "Follow the work to a result",
    text: "See the plan, respond when input is needed, and keep the full objective and its progress together in one workspace.",
  },
];

const capabilities = [
  ["Start naturally", "You do not need to know the Agent catalogue. Explain what you want to achieve and FlowFoundry helps shape the path."],
  ["Bring your context", "Attach relevant source material so the work begins with the information that matters."],
  ["Use the right specialists", "Express a preference or let ForgeMaster identify the most suitable Agent combination for the outcome."],
  ["Stay oriented", "Keep the plan, participating Agents, progress, questions, and outputs connected to the same objective."],
  ["Pause before execution", "Use Wait for GO when you want to prepare the request now and release it only when you are ready."],
  ["Keep oversight", "ForgeMaster remains present throughout, receiving escalations and adjusting the flow when circumstances change."],
];

export default function AboutPage() {
  return (
    <>
      <header className="global-header">
        <Link className="brand-art" href="/" aria-label="About FlowFoundry">
          <Image className="brand-lockup" src="/flowfoundry-logo-modern-v1.png" alt="FlowFoundry" width={419} height={135} priority />
        </Link>
        <nav className="global-nav" aria-label="Global navigation">
          <Link href="/workspace">Workspace</Link><button>Activity</button><button>Agents</button><button>Governance</button><Link className="current" href="/" aria-current="page">About</Link>
        </nav>
        <div className="header-tools">
          <Link className="about-workspace-link" href="/workspace">Open workspace <span aria-hidden="true">→</span></Link>
        </div>
      </header>

      <main className="about-page">
        <section className="about-hero">
          <div className="about-hero-copy">
            <span className="about-kicker">About FlowFoundry</span>
            <h1>From an idea to coordinated action</h1>
            <p className="about-lead">Tell FlowFoundry what you want to achieve. It brings together the right specialist Agents, prepares a clear workflow, and helps you follow the work through to a useful result.</p>
            <p className="about-support">You focus on the outcome. FlowFoundry handles the coordination while keeping you informed and in control.</p>
            <div className="about-actions">
              <Link className="about-primary-action" href="/workspace">Start a new workflow <span aria-hidden="true">→</span></Link>
              <a className="about-text-action" href="#how-it-works">See how it works</a>
            </div>
          </div>
          <div className="about-hero-visual" aria-label="A request is coordinated by ForgeMaster and specialist Agents">
            <div className="about-user-request"><span>Your outcome</span><strong>Review my requirements and prepare a test-ready plan</strong></div>
            <div className="about-flow-line" aria-hidden="true" />
            <div className="about-forgemaster-card">
              <Image src="/forgemaster-happy.png" alt="ForgeMaster coordinating the workflow" width={220} height={280} priority />
              <div><span>Always supervising</span><strong>ForgeMaster</strong><p>Understands, coordinates, and adapts the flow.</p></div>
            </div>
            <div className="about-agent-row" aria-label="Specialist Agents working together">
              <div><Image src="/Athena.png" alt="Athena" width={80} height={80} /><span>Athena</span></div>
              <div><Image src="/Themis.png" alt="Themis" width={80} height={80} /><span>Themis</span></div>
              <div><Image src="/Hermes.png" alt="Hermes" width={80} height={80} /><span>Hermes</span></div>
            </div>
          </div>
        </section>

        <section className="about-section" id="how-it-works">
          <div className="about-section-heading"><span>How it works</span><h2>A clear path from request to result</h2><p>FlowFoundry makes sophisticated coordination feel straightforward. You can begin without learning the system behind it.</p></div>
          <div className="about-steps">
            {steps.map((step) => <article key={step.number}><span>{step.number}</span><h3>{step.title}</h3><p>{step.text}</p></article>)}
          </div>
        </section>

        <section className="about-control-section">
          <div className="about-control-visual">
            <div className="about-control-top"><span>Workflow overview</span><b>In progress</b></div>
            <div className="about-progress"><i /><i /><i /><i /></div>
            <div className="about-control-row complete"><span>✓</span><div><strong>Request understood</strong><small>ForgeMaster prepared the workflow</small></div><b>Complete</b></div>
            <div className="about-control-row active"><span>2</span><div><strong>Specialist work</strong><small>Focused Agents are contributing</small></div><b>Working</b></div>
            <div className="about-control-row"><span>3</span><div><strong>Review the result</strong><small>Outputs remain tied to your objective</small></div><b>Next</b></div>
          </div>
          <div className="about-control-copy"><span className="about-kicker">Built around your oversight</span><h2>You stay in control</h2><p>FlowFoundry is not a black box that simply disappears with your request. The workspace is designed to show who is involved, what is happening, and when your decision is needed.</p><ul><li>Use <strong>Wait for GO</strong> to hold execution until you release it.</li><li>See ForgeMaster&apos;s plan and the participating specialists.</li><li>Respond when an Agent needs clarification or a decision.</li><li>Keep progress and outputs connected to one objective.</li></ul></div>
        </section>

        <section className="about-section about-capability-section">
          <div className="about-section-heading"><span>What you can do</span><h2>One workspace for coordinated AI work</h2></div>
          <div className="about-capability-grid">
            {capabilities.map(([title, text], index) => <article key={title}><span aria-hidden="true">{["✦","▤","◈","◎","Ⅱ","↻"][index]}</span><div><h3>{title}</h3><p>{text}</p></div></article>)}
          </div>
        </section>

        <section className="about-cta"><div><span>Ready when you are</span><h2>Start with the outcome you have in mind.</h2><p>FlowFoundry will help turn it into a coordinated, visible workflow.</p></div><Link href="/workspace">Start a new workflow <span aria-hidden="true">→</span></Link></section>
      </main>
    </>
  );
}
