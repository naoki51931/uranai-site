import type { Locale } from "@/lib/i18n-core";
import { localizedUrl } from "@/lib/site";

type SeoContent = {
  title: string;
  description: string;
  keywords: string[];
  heading: string;
  intro: string;
  bulletPoints: string[];
  faq: Array<{ question: string; answer: string }>;
};

const SEO_CONTENT: Record<Locale, SeoContent> = {
  ja: {
    title: "無料タロット占い | 3枚引きオンラインリーディング",
    description:
      "日本語で使えるオンラインの無料タロット占い。3枚引きで恋愛、仕事、人間関係の悩みに対する解釈をすぐに確認できます。",
    keywords: ["タロット占い", "無料タロット", "オンライン占い", "3枚引き", "恋愛占い", "仕事占い"],
    heading: "オンラインで使える無料タロット占い",
    intro:
      "Moon Arcana は、日本語で使える3枚引きのオンラインタロット占いです。恋愛、仕事、転職、人間関係などの悩みに対して、カード画像付きで解釈を返します。",
    bulletPoints: [
      "無料で始められる3枚引きタロット占い",
      "恋愛や仕事の悩みに使いやすい質問入力",
      "過去・現在・未来の流れをカード画像付きで表示",
    ],
    faq: [
      {
        question: "このタロット占いは無料ですか？",
        answer: "はい。初回利用では無料枠でオンラインのタロット占いを試せます。",
      },
      {
        question: "どんな相談に向いていますか？",
        answer: "恋愛、仕事、転職、人間関係など、方向性を整理したい相談に向いています。",
      },
    ],
  },
  en: {
    title: "Free Tarot Reading Online | 3 Card Tarot Spread",
    description:
      "Get a free tarot reading online in English. Use a 3 card tarot spread for love, career, and relationship questions with clear interpretations.",
    keywords: ["free tarot reading", "online tarot reading", "3 card tarot spread", "love tarot", "career tarot", "tarot reading online"],
    heading: "Free Online Tarot Reading in English",
    intro:
      "Moon Arcana offers a free online tarot reading experience in English. Ask about love, career, relationships, or life direction and receive a 3 card tarot spread with interpretation and card images.",
    bulletPoints: [
      "Free online tarot reading with a 3 card spread",
      "Useful for love, career, and relationship questions",
      "Card images and interpretation for past, present, and future",
    ],
    faq: [
      {
        question: "Is this tarot reading free?",
        answer: "Yes. You can start with the free online tarot reading flow and receive a three card spread.",
      },
      {
        question: "What questions work well for tarot?",
        answer: "Questions about love, career, decisions, and relationship direction work especially well.",
      },
    ],
  },
  ru: {
    title: "Бесплатное онлайн таро | Расклад на 3 карты",
    description:
      "Получите бесплатный онлайн расклад таро на русском языке. Таро на 3 карты подходит для вопросов о любви, работе и отношениях.",
    keywords: ["таро онлайн", "бесплатное таро", "расклад таро", "таро 3 карты", "таро любовь", "таро работа"],
    heading: "Бесплатное онлайн таро на русском языке",
    intro:
      "Moon Arcana позволяет сделать бесплатный онлайн расклад таро на русском языке. Вы можете задать вопрос о любви, работе, отношениях или выборе пути и получить расклад на 3 карты с толкованием.",
    bulletPoints: [
      "Бесплатный онлайн расклад таро на 3 карты",
      "Подходит для вопросов о любви, работе и отношениях",
      "Показывает прошлое, настоящее и будущее с изображениями карт",
    ],
    faq: [
      {
        question: "Это бесплатное таро?",
        answer: "Да. Сервис позволяет начать с бесплатного онлайн расклада таро.",
      },
      {
        question: "Для каких вопросов подходит расклад?",
        answer: "Лучше всего подходят вопросы о любви, карьере, отношениях и принятии решений.",
      },
    ],
  },
  de: {
    title: "Kostenloses Tarot Online | 3 Karten Tarot",
    description:
      "Nutze ein kostenloses Online-Tarot auf Deutsch. Das 3-Karten-Tarot hilft bei Fragen zu Liebe, Beruf und Beziehungen.",
    keywords: ["Tarot online", "kostenloses Tarot", "3 Karten Tarot", "Tarot Liebe", "Tarot Beruf", "Online Tarot"],
    heading: "Kostenloses Online-Tarot auf Deutsch",
    intro:
      "Moon Arcana bietet ein kostenloses Online-Tarot auf Deutsch. Stelle Fragen zu Liebe, Beruf, Beziehungen oder Entscheidungen und erhalte ein 3-Karten-Tarot mit Deutung und Kartenbildern.",
    bulletPoints: [
      "Kostenloses 3-Karten-Tarot online",
      "Geeignet für Liebe, Beruf und Beziehungen",
      "Zeigt Vergangenheit, Gegenwart und Zukunft mit Kartenbildern",
    ],
    faq: [
      {
        question: "Ist das Tarot kostenlos?",
        answer: "Ja. Du kannst das Online-Tarot zunächst kostenlos nutzen.",
      },
      {
        question: "Welche Fragen passen gut?",
        answer: "Gut geeignet sind Fragen zu Liebe, Karriere, Beziehungen und Entscheidungen.",
      },
    ],
  },
  fr: {
    title: "Tarot Gratuit en Ligne | Tirage de 3 Cartes",
    description:
      "Faites un tarot gratuit en ligne en français. Le tirage de 3 cartes convient aux questions d'amour, de travail et de relations.",
    keywords: ["tarot gratuit", "tarot en ligne", "tirage tarot 3 cartes", "tarot amour", "tarot travail", "voyance tarot"],
    heading: "Tarot gratuit en ligne en français",
    intro:
      "Moon Arcana propose un tarot gratuit en ligne en français. Posez une question sur l'amour, le travail, les relations ou une décision importante et obtenez un tirage de 3 cartes avec interpretation et images.",
    bulletPoints: [
      "Tarot gratuit en ligne avec tirage de 3 cartes",
      "Adapté aux questions d'amour, de travail et de relations",
      "Affiche passé, présent et avenir avec images de cartes",
    ],
    faq: [
      {
        question: "Ce tarot est-il gratuit ?",
        answer: "Oui. Vous pouvez commencer par un tirage de tarot gratuit en ligne.",
      },
      {
        question: "Quels types de questions conviennent ?",
        answer: "Les questions sur l'amour, le travail, les relations et les choix de vie conviennent bien.",
      },
    ],
  },
  it: {
    title: "Tarocchi Gratis Online | Lettura dei Tarocchi a 3 Carte",
    description:
      "Prova i tarocchi gratis online in italiano. La lettura a 3 carte aiuta con domande su amore, lavoro e relazioni.",
    keywords: ["tarocchi gratis", "tarocchi online", "lettura tarocchi 3 carte", "tarocchi amore", "tarocchi lavoro", "consulto tarocchi"],
    heading: "Tarocchi gratis online in italiano",
    intro:
      "Moon Arcana offre tarocchi gratis online in italiano. Fai una domanda su amore, lavoro, relazioni o decisioni personali e ricevi una lettura dei tarocchi a 3 carte con interpretazione e immagini.",
    bulletPoints: [
      "Tarocchi online gratis con lettura a 3 carte",
      "Utile per domande su amore, lavoro e relazioni",
      "Mostra passato, presente e futuro con immagini delle carte",
    ],
    faq: [
      {
        question: "I tarocchi sono gratis?",
        answer: "Si. Puoi iniziare con una lettura dei tarocchi gratis online.",
      },
      {
        question: "Quali domande funzionano meglio?",
        answer: "Funzionano bene domande su amore, carriera, relazioni e scelte importanti.",
      },
    ],
  },
};

export function getSeoContent(locale: Locale): SeoContent {
  return SEO_CONTENT[locale];
}

export function buildLocaleJsonLd(locale: Locale) {
  const seo = getSeoContent(locale);
  const pageUrl = localizedUrl(locale);
  return [
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      name: "Moon Arcana",
      description: seo.description,
      inLanguage: locale,
      url: pageUrl,
    },
    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      name: seo.title,
      description: seo.description,
      inLanguage: locale,
      url: pageUrl,
      about: seo.keywords,
    },
    {
      "@context": "https://schema.org",
      "@type": "Service",
      serviceType: "Online tarot reading",
      name: seo.title,
      description: seo.description,
      areaServed: "Worldwide",
      availableLanguage: locale,
      url: pageUrl,
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      inLanguage: locale,
      mainEntity: seo.faq.map((item) => ({
        "@type": "Question",
        name: item.question,
        acceptedAnswer: {
          "@type": "Answer",
          text: item.answer,
        },
      })),
    },
  ];
}
