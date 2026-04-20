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
  "zh-cn": {
    title: "免费在线塔罗占卜 | 三张牌塔罗牌阵",
    description: "使用简体中文进行免费在线塔罗占卜。三张牌牌阵适合爱情、工作、人际关系和人生选择。",
    keywords: ["免费塔罗占卜", "在线塔罗", "三张牌塔罗", "爱情塔罗", "事业塔罗", "塔罗占卜"],
    heading: "简体中文免费在线塔罗占卜",
    intro: "Moon Arcana 提供简体中文的免费在线塔罗占卜。你可以询问爱情、工作、人际关系或重要选择，并获得三张牌解读与牌面图片。",
    bulletPoints: ["免费三张牌在线塔罗", "适合爱情、工作和关系问题", "用牌面图片显示过去、现在和未来"],
    faq: [
      { question: "这个塔罗占卜免费吗？", answer: "是的。你可以先使用免费的在线三张牌塔罗占卜。" },
      { question: "适合问什么问题？", answer: "爱情、职业、关系、选择方向等问题都很适合。" },
    ],
  },
  "zh-tw": {
    title: "免費線上塔羅占卜 | 三張牌塔羅牌陣",
    description: "使用繁體中文進行免費線上塔羅占卜。三張牌牌陣適合愛情、工作、人際關係和人生選擇。",
    keywords: ["免費塔羅占卜", "線上塔羅", "三張牌塔羅", "愛情塔羅", "事業塔羅", "塔羅占卜"],
    heading: "繁體中文免費線上塔羅占卜",
    intro: "Moon Arcana 提供繁體中文的免費線上塔羅占卜。你可以詢問愛情、工作、人際關係或重要選擇，並獲得三張牌解讀與牌面圖片。",
    bulletPoints: ["免費三張牌線上塔羅", "適合愛情、工作和關係問題", "用牌面圖片顯示過去、現在和未來"],
    faq: [
      { question: "這個塔羅占卜免費嗎？", answer: "是的。你可以先使用免費的線上三張牌塔羅占卜。" },
      { question: "適合問什麼問題？", answer: "愛情、職涯、關係、選擇方向等問題都很適合。" },
    ],
  },
  hi: {
    title: "मुफ्त ऑनलाइन टैरो रीडिंग | 3 कार्ड टैरो स्प्रेड",
    description: "हिन्दी में मुफ्त ऑनलाइन टैरो रीडिंग पाएं। 3 कार्ड टैरो स्प्रेड प्रेम, करियर, रिश्तों और निर्णयों के लिए उपयोगी है।",
    keywords: ["मुफ्त टैरो", "ऑनलाइन टैरो", "3 कार्ड टैरो", "प्रेम टैरो", "करियर टैरो", "टैरो रीडिंग"],
    heading: "हिन्दी में मुफ्त ऑनलाइन टैरो रीडिंग",
    intro: "Moon Arcana हिन्दी में मुफ्त ऑनलाइन टैरो रीडिंग देता है। प्रेम, करियर, रिश्तों या जीवन के फैसलों पर प्रश्न पूछें और तीन कार्ड की व्याख्या व चित्र पाएं।",
    bulletPoints: ["मुफ्त 3 कार्ड ऑनलाइन टैरो", "प्रेम, करियर और रिश्तों के सवालों के लिए उपयोगी", "भूत, वर्तमान और भविष्य को कार्ड चित्रों के साथ दिखाता है"],
    faq: [
      { question: "क्या यह टैरो रीडिंग मुफ्त है?", answer: "हाँ। आप मुफ्त ऑनलाइन तीन कार्ड टैरो रीडिंग से शुरू कर सकते हैं।" },
      { question: "किस तरह के सवाल अच्छे रहते हैं?", answer: "प्रेम, करियर, रिश्ते और निर्णय से जुड़े सवाल विशेष रूप से अच्छे रहते हैं।" },
    ],
  },
  pt: {
    title: "Tarô Grátis Online | Leitura de Tarô de 3 Cartas",
    description: "Faça uma leitura de tarô grátis online em português. A tiragem de 3 cartas ajuda em perguntas sobre amor, carreira e relacionamentos.",
    keywords: ["tarô grátis", "tarô online", "tiragem de 3 cartas", "tarô amor", "tarô carreira", "leitura de tarô"],
    heading: "Tarô grátis online em português",
    intro: "Moon Arcana oferece tarô grátis online em português. Pergunte sobre amor, carreira, relacionamentos ou decisões e receba uma tiragem de 3 cartas com interpretação e imagens.",
    bulletPoints: ["Tarô online grátis com 3 cartas", "Útil para amor, carreira e relacionamentos", "Mostra passado, presente e futuro com imagens das cartas"],
    faq: [
      { question: "Esta leitura de tarô é grátis?", answer: "Sim. Você pode começar com uma leitura online gratuita de três cartas." },
      { question: "Que perguntas funcionam melhor?", answer: "Perguntas sobre amor, carreira, relacionamentos e decisões importantes funcionam bem." },
    ],
  },
  es: {
    title: "Tarot Gratis Online | Tirada de Tarot de 3 Cartas",
    description: "Haz una lectura de tarot gratis online en español. La tirada de 3 cartas ayuda con preguntas de amor, trabajo y relaciones.",
    keywords: ["tarot gratis", "tarot online", "tirada de 3 cartas", "tarot amor", "tarot trabajo", "lectura de tarot"],
    heading: "Tarot gratis online en español",
    intro: "Moon Arcana ofrece tarot gratis online en español. Pregunta sobre amor, trabajo, relaciones o decisiones y recibe una tirada de 3 cartas con interpretación e imágenes.",
    bulletPoints: ["Tarot online gratis con tirada de 3 cartas", "Útil para amor, trabajo y relaciones", "Muestra pasado, presente y futuro con imágenes de las cartas"],
    faq: [
      { question: "¿Esta lectura de tarot es gratis?", answer: "Sí. Puedes empezar con una lectura online gratuita de tres cartas." },
      { question: "¿Qué preguntas funcionan mejor?", answer: "Funcionan bien las preguntas sobre amor, carrera, relaciones y decisiones importantes." },
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
