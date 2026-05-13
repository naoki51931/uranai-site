import type { LegalPageContent } from "@/lib/compliance";

type Props = {
  content: LegalPageContent;
};

export function LegalPage({ content }: Props) {
  return (
    <main className="shell legalShell">
      <article className="panel legalPage">
        <header className="legalHeader">
          <h1>{content.title}</h1>
        </header>
        <div className="legalSections">
          {content.sections.map((section, index) => (
            <section className="legalSection" key={`${content.title}-${index}`}>
              {section.heading ? <h2>{section.heading}</h2> : null}
              {section.paragraphs?.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
              {section.bullets ? (
                <ul>
                  {section.bullets.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              ) : null}
            </section>
          ))}
        </div>
      </article>
    </main>
  );
}
