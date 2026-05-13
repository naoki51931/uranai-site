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
    title: "カードベースのデジタルエンターテインメント | Moon Arcana",
    description:
      "Moon Arcana は、カードコンテンツとAIテキストを組み合わせたオンラインのデジタルエンターテインメントサービスです。",
    keywords: ["Moon Arcana", "カードコンテンツ", "AIテキスト", "デジタルエンターテインメント", "自己理解", "オンラインコンテンツ"],
    heading: "カードコンテンツとAIテキストを楽しめるオンラインサービス",
    intro:
      "Moon Arcana は、恋愛・人間関係・仕事・ライフスタイルなどのテーマに応じて、カードコンテンツとAIによるテキスト解説を楽しめるオンラインのデジタルエンターテインメントサービスです。",
    bulletPoints: [
      "無料で始められるカードベースの読み物",
      "テーマに応じたAIテキストで自己理解のヒントを得られる",
      "すべてのコンテンツはWeb上で提供され、物理商品の発送はありません",
    ],
    faq: [
      {
        question: "無料で使えますか？",
        answer: "はい。無料機能を利用したうえで、必要に応じてプレミアム機能を追加できます。",
      },
      {
        question: "どのような内容を楽しめますか？",
        answer: "恋愛、人間関係、仕事、ライフスタイルなどのテーマに応じたカードコンテンツとAIテキストを楽しめます。",
      },
    ],
  },
  en: {
    title: "Card-Based Digital Entertainment | Moon Arcana",
    description:
      "Moon Arcana is an online digital entertainment service that combines card-based content with AI-generated text.",
    keywords: ["Moon Arcana", "card-based content", "AI text", "digital entertainment", "self-reflection", "online content"],
    heading: "Online card-based content with AI-generated text",
    intro:
      "Moon Arcana provides card-based digital entertainment with AI-generated text across themes such as relationships, work, lifestyle, and personal reflection.",
    bulletPoints: [
      "Start with free card-based content online",
      "Get AI-generated text designed for self-reflection and personal review",
      "All content is delivered digitally through the website with no physical shipping",
    ],
    faq: [
      {
        question: "Can I use Moon Arcana for free?",
        answer: "Yes. You can start with free features and optionally unlock premium content.",
      },
      {
        question: "What kind of content does Moon Arcana provide?",
        answer: "It provides card-based content and AI-generated text for themes like relationships, work, lifestyle, and reflection.",
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

export type ReadingTopic = "love" | "career" | "affair" | "money";

type TopicContent = {
  slug: ReadingTopic;
  title: string;
  description: string;
  heading: string;
  intro: string;
  prompts: string[];
  faq: Array<{ question: string; answer: string }>;
};

const TOPIC_CONTENT: Record<ReadingTopic, Record<"ja" | "en", TopicContent>> = {
  love: {
    ja: {
      slug: "love",
      title: "復縁・恋愛の占い",
      description: "復縁や片思い、関係修復の悩みに絞ったタロット導線です。",
      heading: "復縁や関係修復に向いた読み口",
      intro: "感情の温度差、再接近のタイミング、連絡の切り出し方を恋愛テーマに寄せて整理します。",
      prompts: ["復縁のタイミング", "相手の気持ち", "連絡してよいか"],
      faq: [
        { question: "復縁の相談に向いていますか？", answer: "はい。タイミング、温度差、次の一手の整理に向いています。" },
        { question: "どんな質問がよいですか？", answer: "相手の気持ち、連絡時期、距離の縮め方などが具体的で相性が良いです。" },
      ],
    },
    en: {
      slug: "love",
      title: "Love and Reconciliation Reading",
      description: "A tarot landing page focused on reconciliation, feelings, and timing.",
      heading: "A reading path tuned for love questions",
      intro: "Use this entry point for timing, emotional distance, and whether to reconnect.",
      prompts: ["Should I reach out?", "What are they feeling?", "Is reconciliation realistic?"],
      faq: [
        { question: "Is this useful for reconciliation?", answer: "Yes. It is tuned for timing, emotional distance, and next steps." },
        { question: "What questions fit best?", answer: "Feelings, contact timing, and how to rebuild trust work well." },
      ],
    },
  },
  career: {
    ja: {
      slug: "career",
      title: "転職・仕事運の占い",
      description: "転職、職場の人間関係、動く時期に焦点を当てた導線です。",
      heading: "転職判断と仕事運に向いた読み口",
      intro: "現職継続か移動か、評価の流れ、交渉のタイミングを仕事テーマで整理します。",
      prompts: ["転職すべきか", "現職に残るべきか", "評価が動く時期"],
      faq: [
        { question: "転職の判断に使えますか？", answer: "はい。残留・移動・準備の優先順位整理に向いています。" },
        { question: "仕事運では何が見えますか？", answer: "環境の流れ、評価、判断軸、次の一手を整理できます。" },
      ],
    },
    en: {
      slug: "career",
      title: "Career and Job Change Reading",
      description: "A landing page focused on job moves, workplace tension, and timing.",
      heading: "A reading path for career decisions",
      intro: "Use this route when deciding whether to stay, move, negotiate, or prepare quietly.",
      prompts: ["Should I change jobs?", "Should I stay?", "When will momentum shift?"],
      faq: [
        { question: "Can this help with job changes?", answer: "Yes. It helps frame whether to stay, move, or prepare." },
        { question: "What does it focus on?", answer: "Timing, work atmosphere, leverage, and your next move." },
      ],
    },
  },
  affair: {
    ja: {
      slug: "affair",
      title: "複雑愛・不倫の占い",
      description: "複雑な関係や秘密の恋に特化した導線です。",
      heading: "曖昧な関係を整理する読み口",
      intro: "言葉にしにくい距離感、続けるリスク、切り替えるタイミングを静かに整理します。",
      prompts: ["相手は本気か", "関係を続けるべきか", "離れるべき時期"],
      faq: [
        { question: "複雑な関係にも使えますか？", answer: "はい。感情と現実のずれを整理する用途に向いています。" },
        { question: "何を聞くとよいですか？", answer: "相手の本気度、続けるコスト、離れる判断軸が有効です。" },
      ],
    },
    en: {
      slug: "affair",
      title: "Complicated Relationship Reading",
      description: "A landing page for secrecy, ambiguity, and emotionally complex situations.",
      heading: "A reading path for complicated relationships",
      intro: "Use this route to examine risk, ambiguity, attachment, and when to step back.",
      prompts: ["Are they serious?", "Should I continue this?", "When should I step back?"],
      faq: [
        { question: "Can this handle complicated relationships?", answer: "Yes. It is designed to sort emotional intensity from practical risk." },
        { question: "What should I ask?", answer: "Ask about seriousness, cost, and whether the relationship is sustainable." },
      ],
    },
  },
  money: {
    ja: {
      slug: "money",
      title: "金運・お金の占い",
      description: "金運、支出判断、収入の流れに寄せた導線です。",
      heading: "金運と判断軸を整える読み口",
      intro: "支出、投資、収入の変化、守るべきラインをお金テーマで見やすくします。",
      prompts: ["今は守るべきか", "収入は伸びるか", "使うべきタイミングか"],
      faq: [
        { question: "金運の相談に使えますか？", answer: "はい。支出判断や流れの見極めに向いています。" },
        { question: "何を聞くと具体的ですか？", answer: "支出タイミング、守るライン、収入変化の兆しが具体的です。" },
      ],
    },
    en: {
      slug: "money",
      title: "Money and Luck Reading",
      description: "A landing page focused on spending, income shifts, and money timing.",
      heading: "A reading path for money questions",
      intro: "Use this route for spending restraint, income movement, and financial timing.",
      prompts: ["Should I hold back?", "Will income improve?", "Is this the right time to spend?"],
      faq: [
        { question: "Is this useful for money questions?", answer: "Yes. It helps frame spending, timing, and momentum." },
        { question: "What should I ask?", answer: "Ask about spending timing, financial caution, and income movement." },
      ],
    },
  },
};

export function getReadingTopicContent(locale: Locale, topic: ReadingTopic): TopicContent {
  return locale === "ja" ? TOPIC_CONTENT[topic].ja : TOPIC_CONTENT[topic].en;
}

export function getReadingTopics(): ReadingTopic[] {
  return Object.keys(TOPIC_CONTENT) as ReadingTopic[];
}

export function buildReadingTopicJsonLd(locale: Locale, topic: ReadingTopic) {
  const content = getReadingTopicContent(locale, topic);
  const pageUrl = localizedUrl(locale, `/reading/${topic}`);
  return [
    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      name: content.title,
      description: content.description,
      inLanguage: locale,
      url: pageUrl,
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      inLanguage: locale,
      mainEntity: content.faq.map((item) => ({
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
