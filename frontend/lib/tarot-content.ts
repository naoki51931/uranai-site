import type { Locale } from "@/lib/i18n-core";
import { buildLanguageAlternates, localeToLanguageTag, localizedUrl } from "@/lib/site";

export type TarotCardSlug = string;

type TarotCardContent = {
  slug: string;
  name: string;
  keywords: string[];
  meanings: Record<Locale, { upright: string; reversed: string }>;
};

type TarotPageContent = {
  title: string;
  description: string;
  eyebrow: string;
  intro: string;
  sections: Array<{ heading: string; body: string }>;
  cardListTitle: string;
  cardListCopy: string;
  cardCta: string;
  startCta: string;
  backLabel: string;
  uprightLabel: string;
  reversedLabel: string;
  keywordsLabel: string;
  readingHintLabel: string;
  readingHint: string;
  moreCardsLabel: string;
};

export const TAROT_CARDS = [
  {
    "slug": "the-fool",
    "name": "The Fool",
    "keywords": [
      "beginnings",
      "curiosity",
      "leap of faith"
    ],
    "meanings": {
      "ja": {
        "upright": "新しい流れに飛び込む勇気が、停滞を動かします。",
        "reversed": "勢いだけで飛び込むより、準備不足や現実逃避を見直す段階です。"
      },
      "en": {
        "upright": "A bold first step is what breaks the current stagnation.",
        "reversed": "This calls for checking preparation and avoidance before taking a leap."
      },
      "ru": {
        "upright": "Смелый шаг в новое способен сдвинуть застой.",
        "reversed": "Сначала стоит проверить подготовку и желание убежать от реальности, а потом делать шаг."
      },
      "de": {
        "upright": "Ein mutiger erster Schritt kann den Stillstand lösen.",
        "reversed": "Pruefen Sie Vorbereitung und Ausweichverhalten, bevor Sie springen."
      },
      "fr": {
        "upright": "Un premier pas audacieux peut débloquer la stagnation.",
        "reversed": "Verifiez la preparation et l'evitement avant de faire le saut."
      },
      "it": {
        "upright": "Un primo passo coraggioso puo rompere la stagnazione.",
        "reversed": "Prima del salto, verifica preparazione ed eventuale fuga dalla realta."
      },
      "zh-cn": {
        "upright": "勇敢迈出新的第一步，能打破当前的停滞。",
        "reversed": "在跃出之前，先检查准备不足和逃避现实的倾向。"
      },
      "zh-tw": {
        "upright": "勇敢踏出新的第一步，能打破當前的停滯。",
        "reversed": "在躍出之前，先檢查準備不足和逃避現實的傾向。"
      },
      "hi": {
        "upright": "नया साहसी कदम वर्तमान ठहराव को तोड़ सकता है।",
        "reversed": "छलांग लगाने से पहले तैयारी और बचने की प्रवृत्ति की जांच करें।"
      },
      "pt": {
        "upright": "Um primeiro passo corajoso pode romper a estagnação atual.",
        "reversed": "Antes do salto, verifique preparo e possível fuga da realidade."
      },
      "es": {
        "upright": "Un primer paso valiente puede romper el estancamiento actual.",
        "reversed": "Antes de saltar, revisa la preparación y la posible evasión."
      }
    }
  },
  {
    "slug": "the-magician",
    "name": "The Magician",
    "keywords": [
      "willpower",
      "focus",
      "manifestation"
    ],
    "meanings": {
      "ja": {
        "upright": "自分の意思と技術を一点に集めるほど結果が現れます。",
        "reversed": "力はあるのに焦点が散り、言葉や計画が空回りしやすい局面です。"
      },
      "en": {
        "upright": "Results appear when your will and skill are focused in one direction.",
        "reversed": "Your tools are present, but scattered focus can make words and plans misfire."
      },
      "ru": {
        "upright": "Результат приходит, когда воля и мастерство собраны в одной точке.",
        "reversed": "Ресурсы есть, но рассеянный фокус может сбивать слова и планы."
      },
      "de": {
        "upright": "Ergebnisse zeigen sich, wenn Wille und Können klar gebündelt sind.",
        "reversed": "Die Mittel sind da, doch zerstreuter Fokus kann Worte und Plaene entgleisen lassen."
      },
      "fr": {
        "upright": "Les résultats arrivent quand la volonté et le savoir-faire sont concentrés.",
        "reversed": "Les moyens existent, mais un focus disperse peut faire deraper paroles et plans."
      },
      "it": {
        "upright": "I risultati arrivano quando volonta e capacita sono concentrate in una direzione.",
        "reversed": "Gli strumenti ci sono, ma un focus disperso puo far inciampare parole e piani."
      },
      "zh-cn": {
        "upright": "当意志和能力集中到一个方向时，结果会开始显现。",
        "reversed": "资源已经具备，但分散的焦点会让语言和计划失准。"
      },
      "zh-tw": {
        "upright": "當意志和能力集中到一個方向時，結果會開始顯現。",
        "reversed": "資源已經具備，但分散的焦點會讓語言和計畫失準。"
      },
      "hi": {
        "upright": "जब इच्छा और कौशल एक दिशा में केंद्रित होते हैं, परिणाम दिखने लगते हैं।",
        "reversed": "साधन मौजूद हैं, लेकिन बिखरा ध्यान शब्दों और योजनाओं को भटका सकता है।"
      },
      "pt": {
        "upright": "Resultados aparecem quando vontade e habilidade se concentram numa direção.",
        "reversed": "Os recursos existem, mas foco disperso pode fazer palavras e planos falharem."
      },
      "es": {
        "upright": "Los resultados aparecen cuando voluntad y habilidad se concentran en una dirección.",
        "reversed": "Los recursos existen, pero el foco disperso puede hacer fallar palabras y planes."
      }
    }
  },
  {
    "slug": "the-high-priestess",
    "name": "The High Priestess",
    "keywords": [
      "intuition",
      "inner voice",
      "mystery"
    ],
    "meanings": {
      "ja": {
        "upright": "外側の情報より、自分の違和感や直感を優先する局面です。",
        "reversed": "直感と不安が混ざりやすく、秘密や思い込みを整理する必要があります。"
      },
      "en": {
        "upright": "This is a moment to trust intuition over outside noise.",
        "reversed": "Intuition and anxiety may be tangled, so hidden assumptions need sorting."
      },
      "ru": {
        "upright": "Сейчас важнее доверять интуиции, чем внешнему шуму.",
        "reversed": "Интуиция смешивается с тревогой, поэтому скрытые допущения нужно разобрать."
      },
      "de": {
        "upright": "Jetzt ist es wichtiger, der Intuition zu vertrauen als dem Außen.",
        "reversed": "Intuition und Angst vermischen sich; verborgene Annahmen brauchen Ordnung."
      },
      "fr": {
        "upright": "Il faut maintenant faire davantage confiance à l'intuition qu'au bruit extérieur.",
        "reversed": "Intuition et anxiete se melangent; les suppositions cachees doivent etre triees."
      },
      "it": {
        "upright": "Adesso conta piu l'intuizione del rumore esterno.",
        "reversed": "Intuizione e ansia si mescolano; le ipotesi nascoste vanno chiarite."
      },
      "zh-cn": {
        "upright": "此刻比起外界声音，更应相信内在直觉。",
        "reversed": "直觉和焦虑可能混在一起，需要整理隐藏的假设。"
      },
      "zh-tw": {
        "upright": "此刻比起外界聲音，更應相信內在直覺。",
        "reversed": "直覺和焦慮可能混在一起，需要整理隱藏的假設。"
      },
      "hi": {
        "upright": "इस समय बाहरी शोर से अधिक अपनी अंतर्ज्ञान पर भरोसा करें।",
        "reversed": "अंतर्ज्ञान और चिंता उलझ सकती हैं, इसलिए छिपी धारणाओं को साफ करें।"
      },
      "pt": {
        "upright": "Este é um momento para confiar mais na intuição do que no ruído externo.",
        "reversed": "Intuição e ansiedade podem se misturar; organize pressupostos ocultos."
      },
      "es": {
        "upright": "Este es un momento para confiar más en la intuición que en el ruido exterior.",
        "reversed": "Intuición y ansiedad pueden mezclarse; ordena las suposiciones ocultas."
      }
    }
  },
  {
    "slug": "the-empress",
    "name": "The Empress",
    "keywords": [
      "growth",
      "nurture",
      "abundance"
    ],
    "meanings": {
      "ja": {
        "upright": "育てる姿勢が人間関係や仕事の成果を豊かにします。",
        "reversed": "与えすぎや甘えが成長を鈍らせているため、境界線を整える時です。"
      },
      "en": {
        "upright": "A nurturing approach helps relationships and work grow steadily.",
        "reversed": "Overgiving or dependency may be slowing growth; clearer boundaries help."
      },
      "ru": {
        "upright": "Заботливый подход помогает росту в отношениях и делах.",
        "reversed": "Чрезмерная отдача или зависимость тормозит рост; помогут ясные границы."
      },
      "de": {
        "upright": "Eine nährende Haltung fördert Wachstum in Beziehungen und Arbeit.",
        "reversed": "Zu viel Geben oder Abhaengigkeit bremst Wachstum; klare Grenzen helfen."
      },
      "fr": {
        "upright": "Une attitude nourrissante favorise la croissance dans les relations et le travail.",
        "reversed": "Trop donner ou trop dependre freine la croissance; des limites claires aideront."
      },
      "it": {
        "upright": "Un approccio nutriente favorisce crescita nelle relazioni e nel lavoro.",
        "reversed": "Dare troppo o dipendere troppo rallenta la crescita; servono confini chiari."
      },
      "zh-cn": {
        "upright": "滋养和培育的态度会让关系与工作稳步成长。",
        "reversed": "过度付出或依赖正在拖慢成长，清晰边界会有帮助。"
      },
      "zh-tw": {
        "upright": "滋養和培育的態度會讓關係與工作穩步成長。",
        "reversed": "過度付出或依賴正在拖慢成長，清晰界線會有幫助。"
      },
      "hi": {
        "upright": "देखभाल और पोषण का रवैया संबंधों और काम को स्थिर रूप से बढ़ाता है।",
        "reversed": "बहुत अधिक देना या निर्भरता विकास को धीमा कर सकती है; स्पष्ट सीमाएं मदद करेंगी।"
      },
      "pt": {
        "upright": "Uma postura cuidadosa ajuda relações e trabalho a crescerem com estabilidade.",
        "reversed": "Dar demais ou depender demais pode frear o crescimento; limites claros ajudam."
      },
      "es": {
        "upright": "Una actitud nutritiva ayuda a que relaciones y trabajo crezcan con estabilidad.",
        "reversed": "Dar demasiado o depender demasiado puede frenar el crecimiento; los límites claros ayudan."
      }
    }
  },
  {
    "slug": "the-emperor",
    "name": "The Emperor",
    "keywords": [
      "structure",
      "authority",
      "stability"
    ],
    "meanings": {
      "ja": {
        "upright": "感情よりもルールと段取りを整えることで前進できます。",
        "reversed": "支配や頑固さが強まりやすく、柔軟な運用に戻すことが課題です。"
      },
      "en": {
        "upright": "Order, structure, and clear decisions move things forward.",
        "reversed": "Control or rigidity may be crowding out the flexibility the situation needs."
      },
      "ru": {
        "upright": "Порядок, структура и ясные решения двигают ситуацию вперед.",
        "reversed": "Контроль или упрямство вытесняют гибкость, которая сейчас нужна."
      },
      "de": {
        "upright": "Ordnung, Struktur und klare Entscheidungen bringen Fortschritt.",
        "reversed": "Kontrolle oder Starrheit verdraengen die Flexibilitaet, die jetzt noetig ist."
      },
      "fr": {
        "upright": "L'ordre, la structure et des décisions nettes font avancer la situation.",
        "reversed": "Le controle ou la rigidite peut etouffer la souplesse necessaire."
      },
      "it": {
        "upright": "Ordine, struttura e decisioni chiare fanno avanzare la situazione.",
        "reversed": "Controllo o rigidita possono soffocare la flessibilita necessaria."
      },
      "zh-cn": {
        "upright": "秩序、结构和清晰决定会推动局面前进。",
        "reversed": "控制或固执可能压过了此刻需要的灵活性。"
      },
      "zh-tw": {
        "upright": "秩序、結構和清晰決定會推動局面前進。",
        "reversed": "控制或固執可能壓過了此刻需要的彈性。"
      },
      "hi": {
        "upright": "व्यवस्था, संरचना और स्पष्ट निर्णय स्थिति को आगे बढ़ाते हैं।",
        "reversed": "नियंत्रण या कठोरता उस लचीलापन को दबा सकती है जिसकी अभी जरूरत है।"
      },
      "pt": {
        "upright": "Ordem, estrutura e decisões claras fazem a situação avançar.",
        "reversed": "Controle ou rigidez podem sufocar a flexibilidade necessária agora."
      },
      "es": {
        "upright": "Orden, estructura y decisiones claras hacen avanzar la situación.",
        "reversed": "El control o la rigidez pueden ahogar la flexibilidad que ahora hace falta."
      }
    }
  },
  {
    "slug": "the-hierophant",
    "name": "The Hierophant",
    "keywords": [
      "tradition",
      "teaching",
      "guidance"
    ],
    "meanings": {
      "ja": {
        "upright": "基本に立ち返り、信頼できる型や助言を取り入れることで道筋が見えます。",
        "reversed": "常識や他人の正解に寄りすぎず、自分に合う型へ組み替える段階です。"
      },
      "en": {
        "upright": "Returning to fundamentals and trusted guidance reveals the path.",
        "reversed": "Borrowed rules are too loud; reshape the pattern so it actually fits you."
      },
      "ru": {
        "upright": "Возврат к основам и надежному совету показывает путь.",
        "reversed": "Чужие правила звучат слишком громко; форму нужно подстроить под себя."
      },
      "de": {
        "upright": "Der Rückgriff auf Grundlagen und verlässliche Führung zeigt den Weg.",
        "reversed": "Fremde Regeln sind zu laut; passen Sie die Form an Ihr eigenes Leben an."
      },
      "fr": {
        "upright": "Revenir aux bases et écouter un guide fiable éclaire le chemin.",
        "reversed": "Les regles empruntees prennent trop de place; adaptez le cadre a votre realite."
      },
      "it": {
        "upright": "Tornare alle basi e a una guida affidabile mostra la strada.",
        "reversed": "Le regole altrui pesano troppo; adatta la forma alla tua realta."
      },
      "zh-cn": {
        "upright": "回到基础，并参考可靠的建议，会让道路更清楚。",
        "reversed": "外来的规则声音太大，需要把框架调整成适合自己的形式。"
      },
      "zh-tw": {
        "upright": "回到基礎，並參考可靠的建議，會讓道路更清楚。",
        "reversed": "外來的規則聲音太大，需要把框架調整成適合自己的形式。"
      },
      "hi": {
        "upright": "मूल बातों और भरोसेमंद सलाह पर लौटना रास्ता स्पष्ट करता है।",
        "reversed": "उधार लिए नियम बहुत हावी हैं; ढांचे को अपने अनुरूप बनाएं।"
      },
      "pt": {
        "upright": "Voltar aos fundamentos e a uma orientação confiável revela o caminho.",
        "reversed": "Regras emprestadas estão altas demais; adapte o padrão à sua realidade."
      },
      "es": {
        "upright": "Volver a lo básico y a una guía confiable muestra el camino.",
        "reversed": "Las reglas prestadas pesan demasiado; adapta el marco a tu realidad."
      }
    }
  },
  {
    "slug": "the-lovers",
    "name": "The Lovers",
    "keywords": [
      "choice",
      "alignment",
      "relationship"
    ],
    "meanings": {
      "ja": {
        "upright": "大切なのは好かれることより、自分の価値観に合う選択です。",
        "reversed": "気持ちと選択が一致せず、関係性や優先順位を再確認する必要があります。"
      },
      "en": {
        "upright": "The key is not pleasing everyone but choosing what matches your values.",
        "reversed": "Feelings and choices are not aligned yet, so priorities need another look."
      },
      "ru": {
        "upright": "Главное не всем понравиться, а выбрать то, что совпадает с вашими ценностями.",
        "reversed": "Чувства и выбор пока не совпадают, поэтому приоритеты требуют пересмотра."
      },
      "de": {
        "upright": "Entscheidend ist nicht Zustimmung, sondern eine Wahl im Einklang mit Ihren Werten.",
        "reversed": "Gefuehle und Wahl sind noch nicht im Einklang; Prioritaeten brauchen Pruefung."
      },
      "fr": {
        "upright": "L'essentiel n'est pas de plaire à tous, mais de choisir selon vos valeurs.",
        "reversed": "Sentiments et choix ne sont pas encore alignes; les priorites demandent examen."
      },
      "it": {
        "upright": "La chiave non e piacere a tutti, ma scegliere in linea con i propri valori.",
        "reversed": "Sentimenti e scelta non sono ancora allineati; le priorita vanno riviste."
      },
      "zh-cn": {
        "upright": "关键不是取悦所有人，而是选择符合自己价值观的方向。",
        "reversed": "感受和选择尚未一致，因此需要重新检查优先顺序。"
      },
      "zh-tw": {
        "upright": "關鍵不是取悅所有人，而是選擇符合自己價值觀的方向。",
        "reversed": "感受和選擇尚未一致，因此需要重新檢查優先順序。"
      },
      "hi": {
        "upright": "मुख्य बात सबको खुश करना नहीं, बल्कि अपने मूल्यों से मेल खाती पसंद करना है।",
        "reversed": "भावना और चुनाव अभी साथ नहीं हैं, इसलिए प्राथमिकताओं को फिर देखें।"
      },
      "pt": {
        "upright": "A chave não é agradar a todos, mas escolher o que combina com seus valores.",
        "reversed": "Sentimentos e escolhas ainda não estão alinhados; revise prioridades."
      },
      "es": {
        "upright": "La clave no es agradar a todos, sino elegir según tus valores.",
        "reversed": "Sentimientos y elección aún no están alineados; revisa prioridades."
      }
    }
  },
  {
    "slug": "the-chariot",
    "name": "The Chariot",
    "keywords": [
      "momentum",
      "discipline",
      "victory"
    ],
    "meanings": {
      "ja": {
        "upright": "迷いを減らして一点突破すると、状況を動かせます。",
        "reversed": "前に進みたい気持ちに対して方向が定まらず、制御を取り戻す時です。"
      },
      "en": {
        "upright": "Reduce hesitation and push in one clear direction.",
        "reversed": "The desire to move is real, but direction and control need to be restored first."
      },
      "ru": {
        "upright": "Меньше колебаний и больше движения в одном направлении.",
        "reversed": "Желание двигаться есть, но сначала нужно вернуть направление и управление."
      },
      "de": {
        "upright": "Weniger Zögern und mehr klare Vorwärtsbewegung.",
        "reversed": "Der Wille zur Bewegung ist da, doch Richtung und Steuerung muessen zuerst zurueckkehren."
      },
      "fr": {
        "upright": "Moins d'hésitation, plus d'élan dans une direction claire.",
        "reversed": "L'envie d'avancer est la, mais direction et maitrise doivent revenir d'abord."
      },
      "it": {
        "upright": "Meno esitazione e piu slancio in una direzione chiara.",
        "reversed": "La voglia di avanzare c'e, ma prima vanno recuperati direzione e controllo."
      },
      "zh-cn": {
        "upright": "减少犹豫，朝一个明确方向推进。",
        "reversed": "前进的意愿真实存在，但方向和掌控需要先找回来。"
      },
      "zh-tw": {
        "upright": "減少猶豫，朝一個明確方向推進。",
        "reversed": "前進的意願真實存在，但方向和掌控需要先找回來。"
      },
      "hi": {
        "upright": "हिचक कम करें और एक स्पष्ट दिशा में आगे बढ़ें।",
        "reversed": "आगे बढ़ने की इच्छा है, लेकिन पहले दिशा और नियंत्रण लौटाना होगा।"
      },
      "pt": {
        "upright": "Reduza a hesitação e avance em uma direção clara.",
        "reversed": "A vontade de avançar existe, mas direção e controle precisam voltar primeiro."
      },
      "es": {
        "upright": "Reduce la duda y avanza en una dirección clara.",
        "reversed": "El deseo de avanzar existe, pero antes deben volver dirección y control."
      }
    }
  },
  {
    "slug": "strength",
    "name": "Strength",
    "keywords": [
      "patience",
      "courage",
      "gentle control"
    ],
    "meanings": {
      "ja": {
        "upright": "強引さより、粘り強く向き合う姿勢が勝ち筋になります。",
        "reversed": "我慢が限界に近づいているため、優しさと自己防衛のバランスが必要です。"
      },
      "en": {
        "upright": "Gentle persistence will do more than force.",
        "reversed": "Endurance is wearing thin; balance kindness with self-protection."
      },
      "ru": {
        "upright": "Мягкая настойчивость сильнее грубого нажима.",
        "reversed": "Терпение истончается; важно совместить мягкость с самозащитой."
      },
      "de": {
        "upright": "Geduldige innere Stärke wirkt mehr als Druck.",
        "reversed": "Die Geduld wird duenn; verbinden Sie Freundlichkeit mit Selbstschutz."
      },
      "fr": {
        "upright": "La persévérance douce sera plus forte que la contrainte.",
        "reversed": "La patience s'use; equilibrez douceur et protection de soi."
      },
      "it": {
        "upright": "La costanza gentile conta piu della forza bruta.",
        "reversed": "La pazienza si sta consumando; bilancia gentilezza e autoprotezione."
      },
      "zh-cn": {
        "upright": "温和而持续的坚持，比强迫更有力量。",
        "reversed": "耐心正在变薄，需要在温柔和自我保护之间取得平衡。"
      },
      "zh-tw": {
        "upright": "溫和而持續的堅持，比強迫更有力量。",
        "reversed": "耐心正在變薄，需要在溫柔和自我保護之間取得平衡。"
      },
      "hi": {
        "upright": "नरम लेकिन लगातार धैर्य दबाव से अधिक असरदार होगा।",
        "reversed": "धैर्य कम हो रहा है; करुणा और आत्म-सुरक्षा में संतुलन रखें।"
      },
      "pt": {
        "upright": "Persistência gentil terá mais força do que pressão.",
        "reversed": "A resistência está se desgastando; equilibre gentileza com autoproteção."
      },
      "es": {
        "upright": "La persistencia amable será más fuerte que la presión.",
        "reversed": "La resistencia se está agotando; equilibra amabilidad con autoprotección."
      }
    }
  },
  {
    "slug": "the-hermit",
    "name": "The Hermit",
    "keywords": [
      "reflection",
      "solitude",
      "wisdom"
    ],
    "meanings": {
      "ja": {
        "upright": "結論を急がず、ひとりで考える時間が精度を上げます。",
        "reversed": "内省が孤立や考えすぎに傾いており、外からの視点を少し入れる時です。"
      },
      "en": {
        "upright": "Taking time alone to reflect will improve your judgment.",
        "reversed": "Reflection may be turning into isolation or overthinking, so invite one outside view."
      },
      "ru": {
        "upright": "Время на уединенное размышление улучшит точность решения.",
        "reversed": "Размышление может перейти в изоляцию, поэтому полезен внешний взгляд."
      },
      "de": {
        "upright": "Zeit für ruhige Selbstreflexion verbessert die Entscheidung.",
        "reversed": "Reflexion kann in Isolation kippen; ein Blick von aussen hilft."
      },
      "fr": {
        "upright": "Prendre du recul pour réfléchir seul améliore le discernement.",
        "reversed": "La reflexion peut devenir isolement; un regard exterieur sera utile."
      },
      "it": {
        "upright": "Prendersi tempo per riflettere da soli migliora il giudizio.",
        "reversed": "La riflessione puo diventare isolamento; uno sguardo esterno aiuta."
      },
      "zh-cn": {
        "upright": "留出独处思考的时间，会提高判断的准确度。",
        "reversed": "反省可能变成孤立或过度思考，适合加入一个外部视角。"
      },
      "zh-tw": {
        "upright": "留出獨處思考的時間，會提高判斷的準確度。",
        "reversed": "反省可能變成孤立或過度思考，適合加入一個外部視角。"
      },
      "hi": {
        "upright": "अकेले सोचने का समय निर्णय को अधिक सटीक बनाएगा।",
        "reversed": "चिंतन अलगाव या अधिक सोच में बदल सकता है; एक बाहरी दृष्टि लें।"
      },
      "pt": {
        "upright": "Um tempo a sós para refletir melhora seu julgamento.",
        "reversed": "Reflexão pode virar isolamento; um olhar externo ajuda."
      },
      "es": {
        "upright": "Tomarte tiempo a solas para reflexionar mejorará tu juicio.",
        "reversed": "La reflexión puede volverse aislamiento; una mirada externa ayudará."
      }
    }
  },
  {
    "slug": "wheel-of-fortune",
    "name": "Wheel of Fortune",
    "keywords": [
      "change",
      "timing",
      "turning point"
    ],
    "meanings": {
      "ja": {
        "upright": "運の波は変わり始めています。流れを読むことが重要です。",
        "reversed": "流れが読みにくい時期なので、無理に動かずタイミングを待つ判断が合います。"
      },
      "en": {
        "upright": "The tide is turning, and timing matters now.",
        "reversed": "The timing is unstable; waiting for a clearer opening is wiser than forcing movement."
      },
      "ru": {
        "upright": "Поток меняется, и сейчас особенно важно чувство момента.",
        "reversed": "Время нестабильно; лучше дождаться более ясного окна, чем давить на ситуацию."
      },
      "de": {
        "upright": "Das Blatt wendet sich, und Timing ist jetzt entscheidend.",
        "reversed": "Das Timing ist unruhig; warten Sie auf ein klareres Fenster statt zu druecken."
      },
      "fr": {
        "upright": "Le courant change, et le bon timing compte maintenant.",
        "reversed": "Le timing est instable; mieux vaut attendre une ouverture claire que forcer."
      },
      "it": {
        "upright": "Il vento sta cambiando e il tempismo conta molto.",
        "reversed": "Il tempismo e instabile; meglio attendere un'apertura chiara che forzare."
      },
      "zh-cn": {
        "upright": "局势的潮流正在转变，现在尤其需要把握时机。",
        "reversed": "时机不稳定，与其强推，不如等待更清楚的窗口。"
      },
      "zh-tw": {
        "upright": "局勢的潮流正在轉變，現在尤其需要把握時機。",
        "reversed": "時機不穩定，與其強推，不如等待更清楚的窗口。"
      },
      "hi": {
        "upright": "प्रवाह बदल रहा है, और अभी समय की समझ महत्वपूर्ण है।",
        "reversed": "समय अस्थिर है; जबरदस्ती से बेहतर स्पष्ट अवसर की प्रतीक्षा है।"
      },
      "pt": {
        "upright": "A maré está mudando, e o senso de tempo importa agora.",
        "reversed": "O timing está instável; espere uma abertura mais clara em vez de forçar."
      },
      "es": {
        "upright": "La corriente está cambiando, y el momento adecuado importa ahora.",
        "reversed": "El momento es inestable; espera una apertura más clara en vez de forzar."
      }
    }
  },
  {
    "slug": "justice",
    "name": "Justice",
    "keywords": [
      "fairness",
      "truth",
      "accountability"
    ],
    "meanings": {
      "ja": {
        "upright": "感情だけでなく事実と責任の線引きを明確にするほど道が開けます。",
        "reversed": "事実確認や責任の線引きが曖昧で、公平さを取り戻すことが先決です。"
      },
      "en": {
        "upright": "Clarity comes from facts, balance, and accountability.",
        "reversed": "Facts and responsibility are blurred, and fairness must be rebuilt before deciding."
      },
      "ru": {
        "upright": "Ясность приходит через факты, баланс и ответственность.",
        "reversed": "Факты и ответственность размыты, и сначала нужно восстановить справедливость."
      },
      "de": {
        "upright": "Klarheit entsteht durch Fakten, Fairness und Verantwortung.",
        "reversed": "Fakten und Verantwortung sind unscharf; Fairness muss zuerst wiederhergestellt werden."
      },
      "fr": {
        "upright": "La clarté vient des faits, de l'équilibre et de la responsabilité.",
        "reversed": "Les faits et les responsabilites sont flous; l'equite doit etre retablie."
      },
      "it": {
        "upright": "La chiarezza nasce da fatti, equilibrio e responsabilita.",
        "reversed": "Fatti e responsabilita sono sfocati; va ricostruita l'equita prima di decidere."
      },
      "zh-cn": {
        "upright": "事实、平衡和责任感会带来清晰。",
        "reversed": "事实和责任变得模糊，必须先重建公平感。"
      },
      "zh-tw": {
        "upright": "事實、平衡和責任感會帶來清晰。",
        "reversed": "事實和責任變得模糊，必須先重建公平感。"
      },
      "hi": {
        "upright": "तथ्य, संतुलन और जवाबदेही से स्पष्टता आती है।",
        "reversed": "तथ्य और जिम्मेदारी धुंधले हैं; निर्णय से पहले निष्पक्षता लौटाएं।"
      },
      "pt": {
        "upright": "Clareza vem de fatos, equilíbrio e responsabilidade.",
        "reversed": "Fatos e responsabilidades estão borrados; recupere a justiça antes de decidir."
      },
      "es": {
        "upright": "La claridad viene de hechos, equilibrio y responsabilidad.",
        "reversed": "Hechos y responsabilidades están borrosos; recupera la equidad antes de decidir."
      }
    }
  },
  {
    "slug": "the-hanged-man",
    "name": "The Hanged Man",
    "keywords": [
      "pause",
      "surrender",
      "new perspective"
    ],
    "meanings": {
      "ja": {
        "upright": "急いで動くより、見方を変えるための停止が状況を好転させます。",
        "reversed": "待つ理由が見えなくなり、停滞を受け入れすぎている可能性があります。"
      },
      "en": {
        "upright": "A pause and a new perspective will help more than rushing ahead.",
        "reversed": "Waiting has lost its purpose, and passive delay may now be the real obstacle."
      },
      "ru": {
        "upright": "Пауза и новый взгляд сейчас полезнее спешки.",
        "reversed": "Ожидание потеряло смысл, и пассивная задержка может стать препятствием."
      },
      "de": {
        "upright": "Eine Pause und ein Perspektivwechsel helfen mehr als Hast.",
        "reversed": "Das Warten hat seinen Zweck verloren und kann selbst zum Hindernis werden."
      },
      "fr": {
        "upright": "Une pause et un nouveau regard aideront plus qu'une action précipitée.",
        "reversed": "L'attente a perdu son sens et peut devenir l'obstacle principal."
      },
      "it": {
        "upright": "Una pausa e un nuovo punto di vista aiutano piu della fretta.",
        "reversed": "L'attesa ha perso scopo e puo essere diventata l'ostacolo principale."
      },
      "zh-cn": {
        "upright": "暂停并换个角度，会比急着行动更有帮助。",
        "reversed": "等待已经失去目的，被动拖延可能才是真正的障碍。"
      },
      "zh-tw": {
        "upright": "暫停並換個角度，會比急著行動更有幫助。",
        "reversed": "等待已經失去目的，被動拖延可能才是真正的障礙。"
      },
      "hi": {
        "upright": "ठहरना और नया दृष्टिकोण लेना जल्दबाज़ी से अधिक मदद करेगा।",
        "reversed": "प्रतीक्षा का उद्देश्य खो गया है, और निष्क्रिय विलंब बाधा बन सकता है।"
      },
      "pt": {
        "upright": "Uma pausa e uma nova perspectiva ajudam mais do que pressa.",
        "reversed": "A espera perdeu propósito e pode ter virado o principal obstáculo."
      },
      "es": {
        "upright": "Una pausa y una nueva perspectiva ayudarán más que la prisa.",
        "reversed": "La espera perdió propósito y puede ser el obstáculo principal."
      }
    }
  },
  {
    "slug": "death",
    "name": "Death",
    "keywords": [
      "ending",
      "transition",
      "renewal"
    ],
    "meanings": {
      "ja": {
        "upright": "終わらせるべき流れを手放すことで、次の始まりに入れます。",
        "reversed": "終わらせるべきものに未練が残り、変化への抵抗が次の展開を遅らせています。"
      },
      "en": {
        "upright": "Letting an old phase end opens the door to what comes next.",
        "reversed": "Resistance to an ending is slowing the transition that wants to happen."
      },
      "ru": {
        "upright": "Завершение старого этапа открывает вход в новый.",
        "reversed": "Сопротивление завершению замедляет переход, который уже назрел."
      },
      "de": {
        "upright": "Wenn ein alter Abschnitt endet, beginnt Raum für Neues.",
        "reversed": "Widerstand gegen ein Ende verlangsamt den faelligen Uebergang."
      },
      "fr": {
        "upright": "Laisser finir une ancienne phase ouvre la porte à la suivante.",
        "reversed": "La resistance a une fin ralentit la transition qui veut se faire."
      },
      "it": {
        "upright": "Lasciare finire una fase apre la porta a quella successiva.",
        "reversed": "La resistenza a una fine rallenta la transizione gia pronta."
      },
      "zh-cn": {
        "upright": "让旧阶段结束，才会为接下来的发展打开空间。",
        "reversed": "对结束的抵抗正在拖慢已经到来的转变。"
      },
      "zh-tw": {
        "upright": "讓舊階段結束，才會為接下來的發展打開空間。",
        "reversed": "對結束的抵抗正在拖慢已經到來的轉變。"
      },
      "hi": {
        "upright": "पुराने चरण को समाप्त होने देना अगले चरण के लिए जगह बनाता है।",
        "reversed": "अंत का विरोध आवश्यक परिवर्तन को धीमा कर रहा है।"
      },
      "pt": {
        "upright": "Deixar uma fase antiga terminar abre a porta para a próxima.",
        "reversed": "Resistir a um fim está atrasando a transição necessária."
      },
      "es": {
        "upright": "Dejar que termine una etapa antigua abre la puerta a lo siguiente.",
        "reversed": "Resistir un final está retrasando la transición necesaria."
      }
    }
  },
  {
    "slug": "temperance",
    "name": "Temperance",
    "keywords": [
      "balance",
      "moderation",
      "integration"
    ],
    "meanings": {
      "ja": {
        "upright": "極端に振れず、異なる要素を丁寧に混ぜ合わせる姿勢が鍵です。",
        "reversed": "無理に合わせようとして調和が崩れているため、配分を見直す必要があります。"
      },
      "en": {
        "upright": "Balance and careful integration are the right approach.",
        "reversed": "Forced compromise is disrupting balance; the proportions need adjustment."
      },
      "ru": {
        "upright": "Баланс и аккуратное соединение разных элементов будут лучшей стратегией.",
        "reversed": "Вынужденный компромисс нарушает баланс; пропорции нужно пересмотреть."
      },
      "de": {
        "upright": "Balance und sorgfältige Verbindung verschiedener Elemente sind jetzt der Schlüssel.",
        "reversed": "Erzwungener Ausgleich stoert die Balance; die Verteilung braucht Korrektur."
      },
      "fr": {
        "upright": "L'équilibre et l'intégration patiente sont la bonne voie.",
        "reversed": "Un compromis force trouble l'equilibre; les proportions doivent etre revues."
      },
      "it": {
        "upright": "Equilibrio e integrazione paziente sono la strada giusta.",
        "reversed": "Un compromesso forzato rompe l'equilibrio; le proporzioni vanno corrette."
      },
      "zh-cn": {
        "upright": "保持平衡，并耐心整合不同因素，是此刻的关键。",
        "reversed": "被迫妥协正在破坏平衡，需要重新调整比例。"
      },
      "zh-tw": {
        "upright": "保持平衡，並耐心整合不同因素，是此刻的關鍵。",
        "reversed": "被迫妥協正在破壞平衡，需要重新調整比例。"
      },
      "hi": {
        "upright": "संतुलन और धैर्यपूर्ण समन्वय सही रास्ता है।",
        "reversed": "मजबूर समझौता संतुलन बिगाड़ रहा है; अनुपात सुधारें।"
      },
      "pt": {
        "upright": "Equilíbrio e integração cuidadosa são a melhor abordagem.",
        "reversed": "Um compromisso forçado está quebrando o equilíbrio; ajuste as proporções."
      },
      "es": {
        "upright": "El equilibrio y la integración cuidadosa son el mejor enfoque.",
        "reversed": "Un compromiso forzado rompe el equilibrio; ajusta las proporciones."
      }
    }
  },
  {
    "slug": "the-devil",
    "name": "The Devil",
    "keywords": [
      "attachment",
      "temptation",
      "shadow"
    ],
    "meanings": {
      "ja": {
        "upright": "自分を縛っている習慣や執着を自覚すると、主導権を取り戻せます。",
        "reversed": "執着の正体は見え始めていますが、手放すには具体的な距離の取り方が必要です。"
      },
      "en": {
        "upright": "Notice the habit or attachment that is limiting your freedom.",
        "reversed": "The attachment is becoming visible, but release needs a practical boundary."
      },
      "ru": {
        "upright": "Важно увидеть привычку или привязанность, которая лишает вас свободы.",
        "reversed": "Привязанность уже видна, но освобождение требует практической границы."
      },
      "de": {
        "upright": "Erkennen Sie die Gewohnheit oder Bindung, die Ihre Freiheit einschränkt.",
        "reversed": "Die Bindung wird sichtbar, doch Loesung braucht eine praktische Grenze."
      },
      "fr": {
        "upright": "Voyez l'habitude ou l'attachement qui limite votre liberté.",
        "reversed": "L'attachement devient visible, mais s'en liberer demande une limite concrete."
      },
      "it": {
        "upright": "Riconosci l'abitudine o l'attaccamento che limita la tua liberta.",
        "reversed": "L'attaccamento e visibile, ma per liberarsene serve un confine concreto."
      },
      "zh-cn": {
        "upright": "看清限制你自由的习惯或执着，就能重新掌握主动。",
        "reversed": "执着已经开始显现，但释放它需要具体的界线。"
      },
      "zh-tw": {
        "upright": "看清限制你自由的習慣或執著，就能重新掌握主動。",
        "reversed": "執著已經開始顯現，但釋放它需要具體的界線。"
      },
      "hi": {
        "upright": "उस आदत या आसक्ति को पहचानें जो आपकी स्वतंत्रता सीमित कर रही है।",
        "reversed": "आसक्ति दिख रही है, लेकिन मुक्त होने के लिए व्यावहारिक सीमा चाहिए।"
      },
      "pt": {
        "upright": "Perceba o hábito ou apego que está limitando sua liberdade.",
        "reversed": "O apego está visível, mas soltá-lo exige um limite prático."
      },
      "es": {
        "upright": "Observa el hábito o apego que está limitando tu libertad.",
        "reversed": "El apego ya se ve, pero soltarlo requiere un límite práctico."
      }
    }
  },
  {
    "slug": "the-tower",
    "name": "The Tower",
    "keywords": [
      "shock",
      "collapse",
      "awakening"
    ],
    "meanings": {
      "ja": {
        "upright": "無理に保っていた前提が崩れることで、本質に立ち返る機会が来ます。",
        "reversed": "大きな崩壊を避けたいなら、小さな違和感の段階で修正することが重要です。"
      },
      "en": {
        "upright": "A shaken foundation can become the start of something more honest.",
        "reversed": "A smaller correction now can prevent a more disruptive collapse later."
      },
      "ru": {
        "upright": "Разрушение хрупкой опоры может стать началом честного обновления.",
        "reversed": "Маленькая правка сейчас может предотвратить более резкое разрушение позже."
      },
      "de": {
        "upright": "Ein erschüttertes Fundament kann der Beginn ehrlicher Erneuerung sein.",
        "reversed": "Eine kleine Korrektur jetzt kann einen groesseren Bruch spaeter verhindern."
      },
      "fr": {
        "upright": "Une base qui s'effondre peut ouvrir un renouveau plus honnête.",
        "reversed": "Une petite correction maintenant peut eviter une rupture plus forte plus tard."
      },
      "it": {
        "upright": "Una base che crolla puo diventare l'inizio di qualcosa di piu autentico.",
        "reversed": "Una piccola correzione ora puo evitare un crollo piu forte dopo."
      },
      "zh-cn": {
        "upright": "被动摇的基础，可能成为更真实更新的开始。",
        "reversed": "现在做小修正，可以避免之后更剧烈的崩塌。"
      },
      "zh-tw": {
        "upright": "被動搖的基礎，可能成為更真實更新的開始。",
        "reversed": "現在做小修正，可以避免之後更劇烈的崩塌。"
      },
      "hi": {
        "upright": "हिला हुआ आधार अधिक ईमानदार नई शुरुआत बन सकता है।",
        "reversed": "अभी छोटी सुधारात्मक कार्रवाई आगे बड़े टूटन से बचा सकती है।"
      },
      "pt": {
        "upright": "Uma base abalada pode iniciar uma renovação mais honesta.",
        "reversed": "Uma pequena correção agora pode evitar uma ruptura maior depois."
      },
      "es": {
        "upright": "Una base sacudida puede iniciar una renovación más honesta.",
        "reversed": "Una pequeña corrección ahora puede evitar una ruptura mayor después."
      }
    }
  },
  {
    "slug": "the-star",
    "name": "The Star",
    "keywords": [
      "hope",
      "healing",
      "guidance"
    ],
    "meanings": {
      "ja": {
        "upright": "先を急がず、回復と希望を信じるほど流れは静かに整います。",
        "reversed": "希望は残っていますが、期待だけで進まず回復の時間を確保する局面です。"
      },
      "en": {
        "upright": "Hope and healing quietly restore momentum.",
        "reversed": "Hope remains, but recovery needs time rather than expectation alone."
      },
      "ru": {
        "upright": "Надежда и исцеление постепенно возвращают движение.",
        "reversed": "Надежда остается, но восстановлению нужно время, а не одни ожидания."
      },
      "de": {
        "upright": "Hoffnung und Heilung bringen die Bewegung ruhig zurück.",
        "reversed": "Hoffnung bleibt, aber Heilung braucht Zeit statt nur Erwartung."
      },
      "fr": {
        "upright": "L'espoir et la guérison rétablissent peu à peu l'élan.",
        "reversed": "L'espoir demeure, mais la guerison demande du temps plutot que des attentes seules."
      },
      "it": {
        "upright": "Speranza e guarigione riportano lentamente il movimento.",
        "reversed": "La speranza resta, ma la guarigione richiede tempo e non solo aspettative."
      },
      "zh-cn": {
        "upright": "希望与疗愈会安静地恢复前进的力量。",
        "reversed": "希望仍在，但恢复需要时间，而不只是期待。"
      },
      "zh-tw": {
        "upright": "希望與療癒會安靜地恢復前進的力量。",
        "reversed": "希望仍在，但恢復需要時間，而不只是期待。"
      },
      "hi": {
        "upright": "आशा और उपचार धीरे-धीरे गति वापस लाते हैं।",
        "reversed": "आशा बनी है, पर उपचार को केवल उम्मीद नहीं, समय चाहिए।"
      },
      "pt": {
        "upright": "Esperança e cura restauram o movimento aos poucos.",
        "reversed": "A esperança permanece, mas a cura precisa de tempo, não apenas expectativa."
      },
      "es": {
        "upright": "La esperanza y la sanación restauran el movimiento poco a poco.",
        "reversed": "La esperanza permanece, pero sanar requiere tiempo, no solo expectativas."
      }
    }
  },
  {
    "slug": "the-moon",
    "name": "The Moon",
    "keywords": [
      "uncertainty",
      "intuition",
      "subconscious"
    ],
    "meanings": {
      "ja": {
        "upright": "見えない不安に飲まれず、曖昧さの中で直感を磨くことが大切です。",
        "reversed": "不安が判断を曇らせやすく、確かな情報と曖昧な想像を分ける必要があります。"
      },
      "en": {
        "upright": "Do not let uncertainty swallow you; refine your intuition instead.",
        "reversed": "Anxiety can distort judgment; separate reliable facts from imagined fears."
      },
      "ru": {
        "upright": "Не позволяйте неопределенности поглотить вас; точнее слушайте интуицию.",
        "reversed": "Тревога искажает суждение; отделите факты от воображаемых страхов."
      },
      "de": {
        "upright": "Lassen Sie sich nicht von Unsicherheit verschlingen; schärfen Sie Ihre Intuition.",
        "reversed": "Angst kann das Urteil verzerren; trennen Sie Fakten von Vorstellungen."
      },
      "fr": {
        "upright": "Ne laissez pas l'incertitude vous engloutir; affinez plutôt votre intuition.",
        "reversed": "L'anxiete peut deformer le jugement; separez les faits des peurs imaginees."
      },
      "it": {
        "upright": "Non lasciare che l'incertezza ti inghiotta; affina invece l'intuizione.",
        "reversed": "L'ansia puo deformare il giudizio; separa i fatti dalle paure immaginate."
      },
      "zh-cn": {
        "upright": "不要被不确定吞没，而要在模糊中磨练直觉。",
        "reversed": "焦虑会扭曲判断，需要把可靠事实和想象中的恐惧分开。"
      },
      "zh-tw": {
        "upright": "不要被不確定吞沒，而要在模糊中磨練直覺。",
        "reversed": "焦慮會扭曲判斷，需要把可靠事實和想像中的恐懼分開。"
      },
      "hi": {
        "upright": "अनिश्चितता में डूबने के बजाय अपनी अंतर्ज्ञान को परिष्कृत करें।",
        "reversed": "चिंता निर्णय को विकृत कर सकती है; तथ्यों और कल्पित डर को अलग करें।"
      },
      "pt": {
        "upright": "Não deixe a incerteza engolir você; refine sua intuição.",
        "reversed": "A ansiedade pode distorcer o julgamento; separe fatos de medos imaginados."
      },
      "es": {
        "upright": "No dejes que la incertidumbre te absorba; afina tu intuición.",
        "reversed": "La ansiedad puede distorsionar el juicio; separa hechos de miedos imaginados."
      }
    }
  },
  {
    "slug": "the-sun",
    "name": "The Sun",
    "keywords": [
      "clarity",
      "joy",
      "success"
    ],
    "meanings": {
      "ja": {
        "upright": "素直さと明るさを前に出すほど、状況は分かりやすく前進します。",
        "reversed": "喜びや成果が見えにくくても、素直な確認と小さな成功の積み直しが効きます。"
      },
      "en": {
        "upright": "Honesty, warmth, and clarity bring progress.",
        "reversed": "Progress may feel dim, but honest check-ins and small wins rebuild clarity."
      },
      "ru": {
        "upright": "Открытость, тепло и ясность ведут к успеху.",
        "reversed": "Прогресс может быть неочевиден, но честная проверка и малые успехи возвращают ясность."
      },
      "de": {
        "upright": "Offenheit, Wärme und Klarheit fördern den Erfolg.",
        "reversed": "Fortschritt wirkt gedimmt, doch ehrliche Klaerung und kleine Erfolge bringen Licht zurueck."
      },
      "fr": {
        "upright": "La franchise, la chaleur et la clarté favorisent l'avancée.",
        "reversed": "La progression semble moins lumineuse, mais des verifications sinceres et de petits succes ramenent la clarte."
      },
      "it": {
        "upright": "Chiarezza, calore e sincerita favoriscono il progresso.",
        "reversed": "Il progresso sembra meno luminoso, ma verifiche sincere e piccoli successi riportano chiarezza."
      },
      "zh-cn": {
        "upright": "坦率、温暖和清晰会带来进展。",
        "reversed": "进展可能不明显，但诚实确认和小成功会重新带来清晰。"
      },
      "zh-tw": {
        "upright": "坦率、溫暖和清晰會帶來進展。",
        "reversed": "進展可能不明顯，但誠實確認和小成功會重新帶來清晰。"
      },
      "hi": {
        "upright": "ईमानदारी, गर्मजोशी और स्पष्टता प्रगति लाते हैं।",
        "reversed": "प्रगति मंद लग सकती है, लेकिन ईमानदार जांच और छोटे सफल कदम स्पष्टता लौटाते हैं।"
      },
      "pt": {
        "upright": "Honestidade, calor e clareza trazem progresso.",
        "reversed": "O progresso pode parecer fraco, mas verificações honestas e pequenas vitórias devolvem clareza."
      },
      "es": {
        "upright": "Honestidad, calidez y claridad traen progreso.",
        "reversed": "El progreso puede verse tenue, pero revisiones honestas y pequeños logros devuelven claridad."
      }
    }
  },
  {
    "slug": "judgement",
    "name": "Judgement",
    "keywords": [
      "calling",
      "reflection",
      "rebirth"
    ],
    "meanings": {
      "ja": {
        "upright": "過去の流れを見直し、いま本当に応えるべき呼びかけに向き合う時です。",
        "reversed": "過去の評価に縛られ、今の呼びかけを聞き逃していないか見直す時です。"
      },
      "en": {
        "upright": "Review the past and answer the call that truly matters now.",
        "reversed": "Old judgments may be drowning out the call that matters now."
      },
      "ru": {
        "upright": "Оглянитесь назад и ответьте на тот зов, который действительно важен.",
        "reversed": "Старые оценки могут заглушать зов, важный именно сейчас."
      },
      "de": {
        "upright": "Blicken Sie zurück und folgen Sie dem Ruf, der jetzt wirklich zählt.",
        "reversed": "Alte Urteile koennen den Ruf der Gegenwart uebertoenen."
      },
      "fr": {
        "upright": "Regardez le passé et répondez à l'appel qui compte vraiment maintenant.",
        "reversed": "D'anciens jugements peuvent couvrir l'appel important du present."
      },
      "it": {
        "upright": "Guarda al passato e rispondi alla chiamata che conta davvero ora.",
        "reversed": "Vecchi giudizi possono coprire la chiamata importante del presente."
      },
      "zh-cn": {
        "upright": "回顾过去，并回应此刻真正重要的召唤。",
        "reversed": "旧有评价可能盖过了此刻真正重要的召唤。"
      },
      "zh-tw": {
        "upright": "回顧過去，並回應此刻真正重要的召喚。",
        "reversed": "舊有評價可能蓋過了此刻真正重要的召喚。"
      },
      "hi": {
        "upright": "अतीत की समीक्षा करें और उस पुकार का उत्तर दें जो अभी सच में महत्वपूर्ण है।",
        "reversed": "पुराने निर्णय वर्तमान की महत्वपूर्ण पुकार को दबा सकते हैं।"
      },
      "pt": {
        "upright": "Revise o passado e responda ao chamado que realmente importa agora.",
        "reversed": "Julgamentos antigos podem abafar o chamado importante do presente."
      },
      "es": {
        "upright": "Revisa el pasado y responde al llamado que realmente importa ahora.",
        "reversed": "Juicios antiguos pueden tapar el llamado importante del presente."
      }
    }
  },
  {
    "slug": "the-world",
    "name": "The World",
    "keywords": [
      "completion",
      "integration",
      "fulfillment"
    ],
    "meanings": {
      "ja": {
        "upright": "これまでの積み重ねがまとまり、ひとつの完成へ近づいています。",
        "reversed": "完成目前で詰めが甘くなりやすく、未完了の一点を仕上げる段階です。"
      },
      "en": {
        "upright": "Your efforts are coming together toward completion.",
        "reversed": "Completion is close, but one unfinished detail still needs attention."
      },
      "ru": {
        "upright": "Ваши усилия складываются в завершенную картину.",
        "reversed": "Завершение близко, но одна незаконченная деталь еще требует внимания."
      },
      "de": {
        "upright": "Ihre Bemühungen fügen sich zu einem runden Abschluss.",
        "reversed": "Der Abschluss ist nah, aber ein offener Punkt braucht noch Sorgfalt."
      },
      "fr": {
        "upright": "Vos efforts convergent vers un accomplissement complet.",
        "reversed": "L'accomplissement est proche, mais un detail inacheve demande encore du soin."
      },
      "it": {
        "upright": "I tuoi sforzi si stanno unendo verso un compimento pieno.",
        "reversed": "Il compimento e vicino, ma un dettaglio incompleto richiede ancora cura."
      },
      "zh-cn": {
        "upright": "你的努力正在汇聚，走向一个完整的完成。",
        "reversed": "完成已经接近，但仍有一个未完成的细节需要处理。"
      },
      "zh-tw": {
        "upright": "你的努力正在匯聚，走向一個完整的完成。",
        "reversed": "完成已經接近，但仍有一個未完成的細節需要處理。"
      },
      "hi": {
        "upright": "आपके प्रयास पूर्णता की दिशा में एक साथ आ रहे हैं।",
        "reversed": "पूर्णता पास है, लेकिन एक अधूरा विवरण अभी ध्यान चाहता है।"
      },
      "pt": {
        "upright": "Seus esforços estão se reunindo em direção à conclusão.",
        "reversed": "A conclusão está próxima, mas um detalhe inacabado ainda precisa de cuidado."
      },
      "es": {
        "upright": "Tus esfuerzos se están uniendo hacia una conclusión completa.",
        "reversed": "La conclusión está cerca, pero un detalle pendiente aún necesita cuidado."
      }
    }
  }
] as const satisfies readonly TarotCardContent[];

const TAROT_PAGE_CONTENT = {
  "ja": {
    "title": "タロット占いとは",
    "description": "タロット占いの基本、カードの読み方、22枚の大アルカナの意味をわかりやすく解説します。",
    "eyebrow": "Tarot guide",
    "intro": "タロット占いは、カードに描かれた象徴を手がかりに、今の状況や気持ち、次の選択肢を整理するためのカードリーディングです。",
    "sections": [
      {
        "heading": "タロット占いの基本",
        "body": "カードは未来を断定する道具ではなく、問いに対して別の視点を与えるための象徴体系として使われます。"
      },
      {
        "heading": "大アルカナの役割",
        "body": "Moon Arcana では22枚の大アルカナを中心に、始まり、選択、変化、回復、完成といった大きな流れを読み解きます。"
      },
      {
        "heading": "読み方のコツ",
        "body": "カード名だけで判断せず、正位置と逆位置、質問のテーマ、直前までの流れを合わせて読むと解釈が深まります。"
      }
    ],
    "cardListTitle": "大アルカナ22枚の意味",
    "cardListCopy": "各カードの正位置・逆位置の意味を言語別に確認できます。",
    "cardCta": "カードの意味を見る",
    "startCta": "無料で占う",
    "backLabel": "タロット占いとはへ戻る",
    "uprightLabel": "正位置の意味",
    "reversedLabel": "逆位置の意味",
    "keywordsLabel": "キーワード",
    "readingHintLabel": "読み方のヒント",
    "readingHint": "このカードは単独で結論を決めるより、質問のテーマや前後に出たカードと合わせて読むことで、より自然な解釈になります。",
    "moreCardsLabel": "ほかのカードを見る"
  },
  "en": {
    "title": "What Is Tarot Reading?",
    "description": "Learn the basics of tarot reading and the meanings of the 22 Major Arcana cards.",
    "eyebrow": "Tarot guide",
    "intro": "Tarot reading uses card symbols to review the present situation, feelings, and possible next choices.",
    "sections": [
      {
        "heading": "The basic idea",
        "body": "Tarot is not used here to guarantee the future. It is a symbolic tool for looking at a question from another angle."
      },
      {
        "heading": "The Major Arcana",
        "body": "Moon Arcana focuses on the 22 Major Arcana cards, reading broad themes such as beginnings, choices, change, recovery, and completion."
      },
      {
        "heading": "How to read cards",
        "body": "A useful reading combines the card name, upright or reversed position, the question, and the surrounding flow."
      }
    ],
    "cardListTitle": "Meanings of the 22 Major Arcana Cards",
    "cardListCopy": "Open each card to read its upright and reversed meaning in this language.",
    "cardCta": "Read card meaning",
    "startCta": "Start a free reading",
    "backLabel": "Back to tarot guide",
    "uprightLabel": "Upright meaning",
    "reversedLabel": "Reversed meaning",
    "keywordsLabel": "Keywords",
    "readingHintLabel": "Reading hint",
    "readingHint": "This card is best read together with the question, the surrounding cards, and whether it appears upright or reversed.",
    "moreCardsLabel": "Explore other cards"
  },
  "ru": {
    "title": "Что такое таро?",
    "description": "Основы чтения таро и значения 22 карт Старших арканов.",
    "eyebrow": "Tarot guide",
    "intro": "Таро использует символы карт, чтобы осмыслить ситуацию, чувства и возможные следующие шаги.",
    "sections": [
      {
        "heading": "Основная идея",
        "body": "Таро не гарантирует будущее, а помогает посмотреть на вопрос с другой стороны."
      },
      {
        "heading": "Старшие арканы",
        "body": "Moon Arcana работает с 22 Старшими арканами: началом, выбором, переменами, восстановлением и завершением."
      },
      {
        "heading": "Как читать карты",
        "body": "Смотрите не только на название карты, но и на положение, тему вопроса и общий контекст расклада."
      }
    ],
    "cardListTitle": "Значения 22 Старших арканов",
    "cardListCopy": "Откройте карту, чтобы прочитать значение в прямом и перевернутом положении.",
    "cardCta": "Читать значение карты",
    "startCta": "Начать бесплатное чтение",
    "backLabel": "Назад к руководству по таро",
    "uprightLabel": "Прямое значение",
    "reversedLabel": "Перевернутое значение",
    "keywordsLabel": "Ключевые слова",
    "readingHintLabel": "Совет по чтению",
    "readingHint": "Эту карту лучше читать вместе с вопросом, соседними картами и ее положением.",
    "moreCardsLabel": "Другие карты"
  },
  "de": {
    "title": "Was ist Tarot?",
    "description": "Grundlagen des Tarot-Lesens und Bedeutungen der 22 Großen Arkana.",
    "eyebrow": "Tarot guide",
    "intro": "Tarot nutzt Kartensymbole, um Situationen, Gefühle und mögliche nächste Schritte zu betrachten.",
    "sections": [
      {
        "heading": "Grundidee",
        "body": "Tarot garantiert keine Zukunft, sondern bietet eine symbolische Perspektive auf eine Frage."
      },
      {
        "heading": "Die Großen Arkana",
        "body": "Moon Arcana konzentriert sich auf 22 Große Arkana und Themen wie Anfang, Wahl, Wandel, Heilung und Abschluss."
      },
      {
        "heading": "Karten lesen",
        "body": "Beziehen Sie Kartenname, aufrechte oder umgekehrte Lage, Frage und Kontext gemeinsam ein."
      }
    ],
    "cardListTitle": "Bedeutungen der 22 Großen Arkana",
    "cardListCopy": "Öffnen Sie jede Karte, um aufrechte und umgekehrte Bedeutung zu lesen.",
    "cardCta": "Kartenbedeutung lesen",
    "startCta": "Kostenloses Reading starten",
    "backLabel": "Zurück zum Tarot-Leitfaden",
    "uprightLabel": "Aufrechte Bedeutung",
    "reversedLabel": "Umgekehrte Bedeutung",
    "keywordsLabel": "Schlüsselwörter",
    "readingHintLabel": "Lesehinweis",
    "readingHint": "Diese Karte wirkt klarer, wenn Frage, Nachbarkarten und Lage zusammen gelesen werden.",
    "moreCardsLabel": "Weitere Karten"
  },
  "fr": {
    "title": "Qu’est-ce que le tarot ?",
    "description": "Les bases du tirage de tarot et les significations des 22 arcanes majeurs.",
    "eyebrow": "Tarot guide",
    "intro": "Le tarot utilise les symboles des cartes pour éclairer une situation, des émotions et des choix possibles.",
    "sections": [
      {
        "heading": "Principe de base",
        "body": "Le tarot ne garantit pas l’avenir; il offre un autre angle de lecture sur une question."
      },
      {
        "heading": "Les arcanes majeurs",
        "body": "Moon Arcana se concentre sur les 22 arcanes majeurs: commencements, choix, changements, guérison et accomplissement."
      },
      {
        "heading": "Lire une carte",
        "body": "Tenez compte du nom, de la position droite ou inversée, de la question et du contexte du tirage."
      }
    ],
    "cardListTitle": "Significations des 22 arcanes majeurs",
    "cardListCopy": "Ouvrez chaque carte pour lire son sens droit et inversé.",
    "cardCta": "Lire la signification",
    "startCta": "Commencer un tirage gratuit",
    "backLabel": "Retour au guide du tarot",
    "uprightLabel": "Sens droit",
    "reversedLabel": "Sens inversé",
    "keywordsLabel": "Mots-clés",
    "readingHintLabel": "Conseil de lecture",
    "readingHint": "Cette carte se lit mieux avec la question, les cartes voisines et sa position.",
    "moreCardsLabel": "Voir d’autres cartes"
  },
  "it": {
    "title": "Che cos’è la lettura dei tarocchi?",
    "description": "Le basi della lettura dei tarocchi e i significati dei 22 Arcani Maggiori.",
    "eyebrow": "Tarot guide",
    "intro": "La lettura dei tarocchi usa i simboli delle carte per osservare situazione, emozioni e prossime scelte.",
    "sections": [
      {
        "heading": "Idea di base",
        "body": "I tarocchi non garantiscono il futuro; offrono una prospettiva simbolica su una domanda."
      },
      {
        "heading": "Arcani Maggiori",
        "body": "Moon Arcana si concentra sui 22 Arcani Maggiori: inizi, scelte, cambiamenti, guarigione e compimento."
      },
      {
        "heading": "Come leggere",
        "body": "Unisci nome della carta, posizione dritta o rovesciata, domanda e contesto del tiraggio."
      }
    ],
    "cardListTitle": "Significati dei 22 Arcani Maggiori",
    "cardListCopy": "Apri ogni carta per leggere significato dritto e rovesciato.",
    "cardCta": "Leggi il significato",
    "startCta": "Inizia una lettura gratuita",
    "backLabel": "Torna alla guida tarocchi",
    "uprightLabel": "Significato dritto",
    "reversedLabel": "Significato rovesciato",
    "keywordsLabel": "Parole chiave",
    "readingHintLabel": "Suggerimento di lettura",
    "readingHint": "Questa carta va letta insieme alla domanda, alle carte vicine e alla sua posizione.",
    "moreCardsLabel": "Altre carte"
  },
  "zh-cn": {
    "title": "什么是塔罗占卜？",
    "description": "了解塔罗占卜基础，以及22张大阿尔卡那牌的正位与逆位含义。",
    "eyebrow": "Tarot guide",
    "intro": "塔罗占卜通过牌面象征，帮助整理当前状况、情绪和下一步选择。",
    "sections": [
      {
        "heading": "基本概念",
        "body": "塔罗并不是保证未来的工具，而是用象征语言为问题提供另一个观察角度。"
      },
      {
        "heading": "大阿尔卡那",
        "body": "Moon Arcana 以22张大阿尔卡那为中心，解读开始、选择、变化、疗愈与完成等主题。"
      },
      {
        "heading": "阅读方式",
        "body": "不要只看牌名，也要结合正位或逆位、问题主题和前后牌的脉络。"
      }
    ],
    "cardListTitle": "22张大阿尔卡那牌义",
    "cardListCopy": "查看每张牌在正位和逆位时的含义。",
    "cardCta": "查看牌义",
    "startCta": "开始免费占卜",
    "backLabel": "返回塔罗指南",
    "uprightLabel": "正位含义",
    "reversedLabel": "逆位含义",
    "keywordsLabel": "关键词",
    "readingHintLabel": "解读提示",
    "readingHint": "这张牌最好结合问题、相邻牌以及正逆位一起阅读。",
    "moreCardsLabel": "查看其他牌"
  },
  "zh-tw": {
    "title": "什麼是塔羅占卜？",
    "description": "了解塔羅占卜基礎，以及22張大阿爾克那牌的正位與逆位含義。",
    "eyebrow": "Tarot guide",
    "intro": "塔羅占卜透過牌面象徵，協助整理當前狀況、情緒和下一步選擇。",
    "sections": [
      {
        "heading": "基本概念",
        "body": "塔羅並不是保證未來的工具，而是用象徵語言為問題提供另一個觀察角度。"
      },
      {
        "heading": "大阿爾克那",
        "body": "Moon Arcana 以22張大阿爾克那為中心，解讀開始、選擇、變化、療癒與完成等主題。"
      },
      {
        "heading": "閱讀方式",
        "body": "不要只看牌名，也要結合正位或逆位、問題主題和前後牌的脈絡。"
      }
    ],
    "cardListTitle": "22張大阿爾克那牌義",
    "cardListCopy": "查看每張牌在正位和逆位時的含義。",
    "cardCta": "查看牌義",
    "startCta": "開始免費占卜",
    "backLabel": "返回塔羅指南",
    "uprightLabel": "正位含義",
    "reversedLabel": "逆位含義",
    "keywordsLabel": "關鍵字",
    "readingHintLabel": "解讀提示",
    "readingHint": "這張牌最好結合問題、相鄰牌以及正逆位一起閱讀。",
    "moreCardsLabel": "查看其他牌"
  },
  "hi": {
    "title": "टैरो रीडिंग क्या है?",
    "description": "टैरो रीडिंग की मूल बातें और 22 मेजर आर्काना कार्डों के अर्थ जानें।",
    "eyebrow": "Tarot guide",
    "intro": "टैरो रीडिंग कार्ड प्रतीकों के माध्यम से स्थिति, भावनाओं और अगले विकल्पों को समझने में मदद करती है।",
    "sections": [
      {
        "heading": "मूल विचार",
        "body": "टैरो भविष्य की गारंटी नहीं देता; यह प्रश्न को देखने का प्रतीकात्मक तरीका देता है।"
      },
      {
        "heading": "मेजर आर्काना",
        "body": "Moon Arcana 22 मेजर आर्काना पर केंद्रित है: शुरुआत, चुनाव, परिवर्तन, उपचार और पूर्णता।"
      },
      {
        "heading": "कैसे पढ़ें",
        "body": "कार्ड नाम, सीधी या उलटी स्थिति, प्रश्न और आसपास के संदर्भ को साथ पढ़ें।"
      }
    ],
    "cardListTitle": "22 मेजर आर्काना कार्डों के अर्थ",
    "cardListCopy": "हर कार्ड का सीधा और उलटा अर्थ पढ़ें।",
    "cardCta": "कार्ड का अर्थ पढ़ें",
    "startCta": "मुफ्त रीडिंग शुरू करें",
    "backLabel": "टैरो गाइड पर लौटें",
    "uprightLabel": "सीधा अर्थ",
    "reversedLabel": "उलटा अर्थ",
    "keywordsLabel": "कीवर्ड",
    "readingHintLabel": "रीडिंग संकेत",
    "readingHint": "इस कार्ड को प्रश्न, आसपास के कार्ड और स्थिति के साथ पढ़ना बेहतर है।",
    "moreCardsLabel": "अन्य कार्ड देखें"
  },
  "pt": {
    "title": "O que é leitura de tarô?",
    "description": "Entenda a leitura de tarô e os significados dos 22 Arcanos Maiores.",
    "eyebrow": "Tarot guide",
    "intro": "A leitura de tarô usa símbolos das cartas para observar situação, sentimentos e próximos caminhos.",
    "sections": [
      {
        "heading": "Ideia básica",
        "body": "O tarô não garante o futuro; ele oferece uma perspectiva simbólica para uma pergunta."
      },
      {
        "heading": "Arcanos Maiores",
        "body": "Moon Arcana foca nos 22 Arcanos Maiores: começos, escolhas, mudanças, cura e conclusão."
      },
      {
        "heading": "Como ler",
        "body": "Combine nome da carta, posição normal ou invertida, pergunta e contexto da tiragem."
      }
    ],
    "cardListTitle": "Significados dos 22 Arcanos Maiores",
    "cardListCopy": "Abra cada carta para ler o significado normal e invertido.",
    "cardCta": "Ler significado",
    "startCta": "Começar leitura grátis",
    "backLabel": "Voltar ao guia de tarô",
    "uprightLabel": "Significado normal",
    "reversedLabel": "Significado invertido",
    "keywordsLabel": "Palavras-chave",
    "readingHintLabel": "Dica de leitura",
    "readingHint": "Esta carta fica mais clara quando lida junto com a pergunta, cartas próximas e posição.",
    "moreCardsLabel": "Ver outras cartas"
  },
  "es": {
    "title": "¿Qué es la lectura de tarot?",
    "description": "Aprende las bases del tarot y los significados de los 22 Arcanos Mayores.",
    "eyebrow": "Tarot guide",
    "intro": "La lectura de tarot usa símbolos de las cartas para revisar situación, emociones y próximos caminos.",
    "sections": [
      {
        "heading": "Idea básica",
        "body": "El tarot no garantiza el futuro; ofrece una perspectiva simbólica sobre una pregunta."
      },
      {
        "heading": "Arcanos Mayores",
        "body": "Moon Arcana se centra en los 22 Arcanos Mayores: comienzos, elecciones, cambios, sanación y cierre."
      },
      {
        "heading": "Cómo leer",
        "body": "Combina nombre de la carta, posición derecha o invertida, pregunta y contexto de la tirada."
      }
    ],
    "cardListTitle": "Significados de los 22 Arcanos Mayores",
    "cardListCopy": "Abre cada carta para leer su significado derecho e invertido.",
    "cardCta": "Leer significado",
    "startCta": "Empezar lectura gratis",
    "backLabel": "Volver a la guía de tarot",
    "uprightLabel": "Significado derecho",
    "reversedLabel": "Significado invertido",
    "keywordsLabel": "Palabras clave",
    "readingHintLabel": "Consejo de lectura",
    "readingHint": "Esta carta se entiende mejor junto con la pregunta, las cartas cercanas y su posición.",
    "moreCardsLabel": "Ver otras cartas"
  }
} as const satisfies Record<Locale, TarotPageContent>;

export function getTarotPageContent(locale: Locale): TarotPageContent {
  return TAROT_PAGE_CONTENT[locale];
}

export function getTarotCards() {
  return TAROT_CARDS;
}

export function getTarotCardSlugs(): string[] {
  return TAROT_CARDS.map((card) => card.slug);
}

export function getTarotCard(slug: string) {
  return TAROT_CARDS.find((card) => card.slug === slug) ?? null;
}

export function getTarotCardReadingHint(locale: Locale, slug: string): string {
  const card = getTarotCard(slug);
  if (!card) {
    return "";
  }
  const content = getTarotPageContent(locale);
  const meanings = card.meanings[locale];
  const primaryKeyword = card.keywords[0];
  const keywordText = card.keywords.join(" / ");
  const templates: Record<Locale, string> = {
    ja: `${card.name}は「${keywordText}」を軸に読むカードです。正位置では ${meanings.upright} という流れを強め、逆位置では ${meanings.reversed} という注意点が出ます。質問の中で ${primaryKeyword} がどこに表れているかを見ると解釈しやすくなります。`,
    en: `${card.name} is best read through the themes of ${keywordText}. Upright, it emphasizes: ${meanings.upright} Reversed, it asks you to watch for: ${meanings.reversed} In the question, look for where ${primaryKeyword} is already showing up.`,
    ru: `${card.name} лучше читать через темы: ${keywordText}. В прямом положении карта усиливает смысл: ${meanings.upright} В перевернутом положении она предупреждает: ${meanings.reversed} В вопросе ищите, где уже проявляется ${primaryKeyword}.`,
    de: `${card.name} liest sich am besten über die Themen ${keywordText}. Aufrecht betont die Karte: ${meanings.upright} Umgekehrt weist sie auf Folgendes hin: ${meanings.reversed} Achten Sie darauf, wo ${primaryKeyword} in Ihrer Frage bereits sichtbar ist.`,
    fr: `${card.name} se lit à partir des thèmes ${keywordText}. À l’endroit, la carte souligne : ${meanings.upright} Inversée, elle invite à surveiller : ${meanings.reversed} Dans la question, repérez où ${primaryKeyword} se manifeste déjà.`,
    it: `${card.name} si legge a partire dai temi ${keywordText}. Al dritto sottolinea: ${meanings.upright} Al rovescio invita a osservare: ${meanings.reversed} Nella domanda, cerca dove ${primaryKeyword} è già presente.`,
    "zh-cn": `${card.name}适合围绕「${keywordText}」来解读。正位时，它强调：${meanings.upright} 逆位时，它提醒：${meanings.reversed} 回到问题本身，看看 ${primaryKeyword} 已经在哪个部分出现。`,
    "zh-tw": `${card.name}適合圍繞「${keywordText}」來解讀。正位時，它強調：${meanings.upright} 逆位時，它提醒：${meanings.reversed} 回到問題本身，看看 ${primaryKeyword} 已經在哪個部分出現。`,
    hi: `${card.name} को ${keywordText} के विषयों से पढ़ना उपयोगी है। सीधी स्थिति में यह बताता है: ${meanings.upright} उलटी स्थिति में यह सावधान करता है: ${meanings.reversed} अपने प्रश्न में देखें कि ${primaryKeyword} कहाँ दिखाई दे रहा है।`,
    pt: `${card.name} funciona melhor quando lida pelos temas ${keywordText}. Na posição normal, destaca: ${meanings.upright} Invertida, pede atenção a: ${meanings.reversed} Na pergunta, observe onde ${primaryKeyword} já aparece.`,
    es: `${card.name} se lee mejor desde los temas ${keywordText}. En posición derecha, destaca: ${meanings.upright} Invertida, pide observar: ${meanings.reversed} En la pregunta, busca dónde ya aparece ${primaryKeyword}.`,
  };
  return templates[locale] || content.readingHint;
}

export function getTarotOverviewMetadata(locale: Locale) {
  const content = getTarotPageContent(locale);
  return {
    title: `${content.title} | Moon Arcana`,
    description: content.description,
    alternates: {
      canonical: localizedUrl(locale, "/tarot"),
      languages: buildLanguageAlternates("/tarot"),
    },
    robots: {
      index: true,
      follow: true,
    },
    openGraph: {
      title: `${content.title} | Moon Arcana`,
      description: content.description,
      url: localizedUrl(locale, "/tarot"),
      type: "article",
    },
  };
}

export function getTarotCardMetadata(locale: Locale, slug: string) {
  const content = getTarotPageContent(locale);
  const card = getTarotCard(slug);
  if (!card) {
    return null;
  }
  const meanings = card.meanings[locale];
  const title = `${card.name} - ${content.uprightLabel}・${content.reversedLabel}`;
  const description = meanings.upright;
  const path = `/tarot/${card.slug}`;
  return {
    title: `${title} | Moon Arcana`,
    description,
    keywords: [card.name, ...card.keywords, content.title],
    alternates: {
      canonical: localizedUrl(locale, path),
      languages: buildLanguageAlternates(path),
    },
    robots: {
      index: true,
      follow: true,
    },
    openGraph: {
      title: `${title} | Moon Arcana`,
      description,
      url: localizedUrl(locale, path),
      type: "article",
    },
  };
}

function buildTarotBreadcrumbJsonLd(locale: Locale, items: Array<{ name: string; path: string }>) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: localizedUrl(locale, item.path),
    })),
  };
}

export function buildTarotOverviewJsonLd(locale: Locale) {
  const content = getTarotPageContent(locale);
  return [
    {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: content.title,
      description: content.description,
      inLanguage: localeToLanguageTag(locale),
      url: localizedUrl(locale, "/tarot"),
      mainEntityOfPage: localizedUrl(locale, "/tarot"),
      author: {
        "@type": "Organization",
        name: "Moon Arcana",
      },
      publisher: {
        "@type": "Organization",
        name: "Moon Arcana",
      },
      about: content.sections.map((section) => section.heading),
    },
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      name: content.cardListTitle,
      description: content.cardListCopy,
      inLanguage: localeToLanguageTag(locale),
      url: localizedUrl(locale, "/tarot"),
      itemListElement: TAROT_CARDS.map((card, index) => ({
        "@type": "ListItem",
        position: index + 1,
        name: card.name,
        url: localizedUrl(locale, `/tarot/${card.slug}`),
      })),
    },
    buildTarotBreadcrumbJsonLd(locale, [{ name: content.title, path: "/tarot" }]),
  ];
}

export function buildTarotCardJsonLd(locale: Locale, slug: string) {
  const content = getTarotPageContent(locale);
  const card = getTarotCard(slug);
  if (!card) {
    return null;
  }
  const meanings = card.meanings[locale];
  return [
    {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: `${card.name} - ${content.uprightLabel}・${content.reversedLabel}`,
      description: meanings.upright,
      inLanguage: localeToLanguageTag(locale),
      url: localizedUrl(locale, `/tarot/${card.slug}`),
      mainEntityOfPage: localizedUrl(locale, `/tarot/${card.slug}`),
      author: {
        "@type": "Organization",
        name: "Moon Arcana",
      },
      publisher: {
        "@type": "Organization",
        name: "Moon Arcana",
      },
      about: [card.name, ...card.keywords],
      articleSection: content.cardListTitle,
    },
    buildTarotBreadcrumbJsonLd(locale, [
      { name: content.title, path: "/tarot" },
      { name: card.name, path: `/tarot/${card.slug}` },
    ]),
  ];
}
