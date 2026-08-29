const portfolio = [
  { no:"01", type:"Grand toilette · 1890", title:"The Pearl Parlour Gown", details:"Ivory silk · hand-set pearls · gathered tulle", image:"/atelier-hero.jpg", cls:"portrait hero-crop" },
  { no:"02", type:"Promenade · 1904", title:"The Blue Hour", details:"Silk faille · pintucked lawn · covered buttons", image:"/portfolio-blue.jpg", cls:"portrait" },
  { no:"03", type:"Evening · 1888", title:"A Study in Oxblood", details:"Velvet · soutache braid · jet beadwork", image:"/portfolio-oxblood.jpg", cls:"landscape" },
  { no:"04", type:"Garden dress · 1902", title:"Rose at Morning", details:"Cotton lawn · antique lace · silk ribbon", image:"/atelier-hero.jpg", cls:"portrait rose-crop" },
  { no:"05", type:"Trousseau · 1876", title:"The Quiet Underlayers", details:"Batiste · hand-worked buttonholes · insertion lace", image:"/process-table.jpg", cls:"portrait table-crop" },
];

const steps = [
  { no:"I", title:"The conversation", note:"Photographs · measurements · provenance", text:"We begin with the doll herself: her scale, age, condition, character, and the history you wish to honor." },
  { no:"II", title:"The silhouette", note:"Research · sketch · proportion", text:"Period references become an original hand-drawn study, refined until the silhouette belongs naturally to her." },
  { no:"III", title:"The paper pattern", note:"Draft · toile · fitting", text:"Every pattern is drafted from her exact measurements. A cotton toile tests balance and ease before precious cloth is cut." },
  { no:"IV", title:"The handwork", note:"Cut · stitch · embellish", text:"Silks, lawns, laces, and trims are shaped at miniature scale. Seams, buttonholes, and details are patiently finished by hand." },
  { no:"V", title:"The atelier record", note:"Final fitting · archive · presentation", text:"The completed garment is photographed, documented, and wrapped for safekeeping with its material and design record." },
];

const Arrow = () => <span aria-hidden="true">↗</span>;

export default function Home() {
  return <main>
    <header className="site-header">
      <a className="wordmark" href="#top" aria-label="The Doll Atelier home"><span>The Doll</span><strong>Atelier</strong></a>
      <nav aria-label="Primary navigation"><a href="#portfolio">Portfolio</a><a href="#process">The making</a><a href="#about">The maker</a></nav>
      <a className="header-cta" href="mailto:hello@thedollatelier.com?subject=Private commission enquiry">Private commissions</a>
    </header>

    <section className="hero" id="top">
      <div className="hero-image" role="img" aria-label="Antique bisque doll in an ivory hand-sewn couture gown"/><div className="hero-shade"/>
      <div className="hero-copy"><p className="eyebrow">Bespoke dressmaking · Commissions worldwide</p><h1>Small dresses.<br/><em>Enduring stories.</em></h1><p className="hero-deck">One-of-one garments for antique dolls, researched, drafted, and sewn entirely by hand.</p><a className="text-link" href="#portfolio">View selected works <Arrow/></a></div>
      <div className="hero-note"><span>No. 001</span><p>A lifetime of dressmaking,<br/>now worked in miniature.</p></div>
    </section>

    <section className="intro"><p className="section-label">The Maison</p><div><h2>Couture knowledge,<br/><em>translated in miniature.</em></h2><p className="lead">For collectors who see an antique doll not simply as an object, but as a keeper of memory.</p></div></section>

    <section className="portfolio" id="portfolio">
      <div className="section-heading"><p className="section-label">Portfolio · Selected works</p><div><h2>The private<br/><em>wardrobe.</em></h2><p>Each garment is a singular commission. These studies show the range of eras, materials, and hand techniques available to collectors.</p></div></div>
      <div className="portfolio-grid">{portfolio.map((item)=><article className={`look ${item.cls}`} key={item.no}><div className="look-image" style={{backgroundImage:`url('${item.image}')`}} role="img" aria-label={item.title}/><div className="look-meta"><span>{item.no} / {item.type}</span><h3>{item.title}</h3><p>{item.details}</p></div></article>)}</div>
      <div className="portfolio-tail"><p>Not a catalogue. A record of singular pieces.</p><a href="mailto:hello@thedollatelier.com?subject=Portfolio and commission enquiry">Discuss a garment <Arrow/></a></div>
    </section>

    <section className="process" id="process">
      <div className="process-intro"><div><p className="section-label">Inside the atelier</p><h2>From line<br/><em>to heirloom.</em></h2></div><p>Luxury at this scale is invisible until you look closely: the grain of silk, a hand-worked buttonhole, a seam pressed no wider than a breath.</p></div>
      <figure className="worktable"><div className="process-image" role="img" aria-label="Atelier worktable with miniature dressmaking tools, sketches, fabric swatches, and paper patterns"/><figcaption><span>Plate I</span><p>The working table · brass shears, silk thread, scale patterns, toile, and design study</p></figcaption></figure>
      <ol className="process-list">{steps.map((step)=><li key={step.no}><span className="step-no">{step.no}</span><div><p className="step-note">{step.note}</p><h3>{step.title}</h3><p className="step-text">{step.text}</p></div></li>)}</ol>
      <div className="materials"><p className="section-label">Atelier vocabulary</p><div><span>Silk faille</span><span>Cotton lawn</span><span>Antique lace</span><span>Soutache</span><span>Jet beadwork</span><span>Hand-dyed ribbon</span></div></div>
    </section>

    <section className="about" id="about"><div className="about-number">40<sup>+</sup><span>years<br/>at the needle</span></div><div className="about-copy"><p className="section-label">The master seamstress</p><h2>A lifetime<br/><em>in cloth.</em></h2><p>Her roots are in women’s dressmaking: decades spent understanding how cloth falls, how a sleeve turns, and how a pattern becomes personal. Later, that knowledge found a more intimate canvas in antique dolls.</p><p>Today, collectors across the world entrust her with garments that restore character without pretending to be original. Every piece is researched, drafted, and finished one at a time by the same pair of hands.</p><blockquote>“The scale becomes smaller. The standard of the work does not.”</blockquote></div></section>

    <section className="commission"><div><p className="section-label">A private service</p><h2>Begin with<br/><em>her photograph.</em></h2></div><div className="commission-copy"><p>Tell us about your doll, her measurements, and the garment you imagine. A limited number of commissions are accepted each season.</p><a className="primary-button" href="mailto:hello@thedollatelier.com?subject=Bespoke doll dress consultation">Request a consultation <Arrow/></a><small>Worldwide enquiries · Replies within 2–3 studio days</small></div></section>

    <footer><a className="wordmark" href="#top"><span>The Doll</span><strong>Atelier</strong></a><p>Bespoke garments for antique dolls.<br/>Made slowly. Kept forever.</p><div><a href="mailto:hello@thedollatelier.com">Email the atelier</a><a href="#top">Back to top ↑</a></div><small>© 2026 The Doll Atelier</small></footer>
  </main>;
}
