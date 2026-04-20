from __future__ import annotations

from typing import Final

from app.services.learning import LearningGuidance


SUPPORTED_LOCALES: Final[set[str]] = {"ja", "en", "ru", "de", "fr", "it", "zh-cn", "zh-tw", "hi", "pt", "es"}
DEFAULT_LOCALE = "ja"

POSITION_LABELS: Final[dict[str, dict[str, str]]] = {
    "ja": {"past": "過去", "present": "現在", "future": "未来"},
    "en": {"past": "past", "present": "present", "future": "future"},
    "ru": {"past": "прошлое", "present": "настоящее", "future": "будущее"},
    "de": {"past": "Vergangenheit", "present": "Gegenwart", "future": "Zukunft"},
    "fr": {"past": "passé", "present": "présent", "future": "avenir"},
    "it": {"past": "passato", "present": "presente", "future": "futuro"},
    "zh-cn": {"past": "过去", "present": "现在", "future": "未来"},
    "zh-tw": {"past": "過去", "present": "現在", "future": "未來"},
    "hi": {"past": "भूत", "present": "वर्तमान", "future": "भविष्य"},
    "pt": {"past": "passado", "present": "presente", "future": "futuro"},
    "es": {"past": "pasado", "present": "presente", "future": "futuro"},
}

CARD_MEANINGS: Final[dict[str, dict[str, str]]] = {
    "ja": {
        "the-fool": "新しい流れに飛び込む勇気が、停滞を動かします。",
        "the-magician": "自分の意思と技術を一点に集めるほど結果が現れます。",
        "the-high-priestess": "外側の情報より、自分の違和感や直感を優先する局面です。",
        "the-empress": "育てる姿勢が人間関係や仕事の成果を豊かにします。",
        "the-emperor": "感情よりもルールと段取りを整えることで前進できます。",
        "the-hierophant": "基本に立ち返り、信頼できる型や助言を取り入れることで道筋が見えます。",
        "the-lovers": "大切なのは好かれることより、自分の価値観に合う選択です。",
        "the-chariot": "迷いを減らして一点突破すると、状況を動かせます。",
        "strength": "強引さより、粘り強く向き合う姿勢が勝ち筋になります。",
        "the-hermit": "結論を急がず、ひとりで考える時間が精度を上げます。",
        "wheel-of-fortune": "運の波は変わり始めています。流れを読むことが重要です。",
        "justice": "感情だけでなく事実と責任の線引きを明確にするほど道が開けます。",
        "the-hanged-man": "急いで動くより、見方を変えるための停止が状況を好転させます。",
        "death": "終わらせるべき流れを手放すことで、次の始まりに入れます。",
        "temperance": "極端に振れず、異なる要素を丁寧に混ぜ合わせる姿勢が鍵です。",
        "the-devil": "自分を縛っている習慣や執着を自覚すると、主導権を取り戻せます。",
        "the-tower": "無理に保っていた前提が崩れることで、本質に立ち返る機会が来ます。",
        "the-star": "先を急がず、回復と希望を信じるほど流れは静かに整います。",
        "the-moon": "見えない不安に飲まれず、曖昧さの中で直感を磨くことが大切です。",
        "the-sun": "素直さと明るさを前に出すほど、状況は分かりやすく前進します。",
        "judgement": "過去の流れを見直し、いま本当に応えるべき呼びかけに向き合う時です。",
        "the-world": "これまでの積み重ねがまとまり、ひとつの完成へ近づいています。",
    },
    "en": {
        "the-fool": "A bold first step is what breaks the current stagnation.",
        "the-magician": "Results appear when your will and skill are focused in one direction.",
        "the-high-priestess": "This is a moment to trust intuition over outside noise.",
        "the-empress": "A nurturing approach helps relationships and work grow steadily.",
        "the-emperor": "Order, structure, and clear decisions move things forward.",
        "the-hierophant": "Returning to fundamentals and trusted guidance reveals the path.",
        "the-lovers": "The key is not pleasing everyone but choosing what matches your values.",
        "the-chariot": "Reduce hesitation and push in one clear direction.",
        "strength": "Gentle persistence will do more than force.",
        "the-hermit": "Taking time alone to reflect will improve your judgment.",
        "wheel-of-fortune": "The tide is turning, and timing matters now.",
        "justice": "Clarity comes from facts, balance, and accountability.",
        "the-hanged-man": "A pause and a new perspective will help more than rushing ahead.",
        "death": "Letting an old phase end opens the door to what comes next.",
        "temperance": "Balance and careful integration are the right approach.",
        "the-devil": "Notice the habit or attachment that is limiting your freedom.",
        "the-tower": "A shaken foundation can become the start of something more honest.",
        "the-star": "Hope and healing quietly restore momentum.",
        "the-moon": "Do not let uncertainty swallow you; refine your intuition instead.",
        "the-sun": "Honesty, warmth, and clarity bring progress.",
        "judgement": "Review the past and answer the call that truly matters now.",
        "the-world": "Your efforts are coming together toward completion.",
    },
    "ru": {
        "the-fool": "Смелый шаг в новое способен сдвинуть застой.",
        "the-magician": "Результат приходит, когда воля и мастерство собраны в одной точке.",
        "the-high-priestess": "Сейчас важнее доверять интуиции, чем внешнему шуму.",
        "the-empress": "Заботливый подход помогает росту в отношениях и делах.",
        "the-emperor": "Порядок, структура и ясные решения двигают ситуацию вперед.",
        "the-hierophant": "Возврат к основам и надежному совету показывает путь.",
        "the-lovers": "Главное не всем понравиться, а выбрать то, что совпадает с вашими ценностями.",
        "the-chariot": "Меньше колебаний и больше движения в одном направлении.",
        "strength": "Мягкая настойчивость сильнее грубого нажима.",
        "the-hermit": "Время на уединенное размышление улучшит точность решения.",
        "wheel-of-fortune": "Поток меняется, и сейчас особенно важно чувство момента.",
        "justice": "Ясность приходит через факты, баланс и ответственность.",
        "the-hanged-man": "Пауза и новый взгляд сейчас полезнее спешки.",
        "death": "Завершение старого этапа открывает вход в новый.",
        "temperance": "Баланс и аккуратное соединение разных элементов будут лучшей стратегией.",
        "the-devil": "Важно увидеть привычку или привязанность, которая лишает вас свободы.",
        "the-tower": "Разрушение хрупкой опоры может стать началом честного обновления.",
        "the-star": "Надежда и исцеление постепенно возвращают движение.",
        "the-moon": "Не позволяйте неопределенности поглотить вас; точнее слушайте интуицию.",
        "the-sun": "Открытость, тепло и ясность ведут к успеху.",
        "judgement": "Оглянитесь назад и ответьте на тот зов, который действительно важен.",
        "the-world": "Ваши усилия складываются в завершенную картину.",
    },
    "de": {
        "the-fool": "Ein mutiger erster Schritt kann den Stillstand lösen.",
        "the-magician": "Ergebnisse zeigen sich, wenn Wille und Können klar gebündelt sind.",
        "the-high-priestess": "Jetzt ist es wichtiger, der Intuition zu vertrauen als dem Außen.",
        "the-empress": "Eine nährende Haltung fördert Wachstum in Beziehungen und Arbeit.",
        "the-emperor": "Ordnung, Struktur und klare Entscheidungen bringen Fortschritt.",
        "the-hierophant": "Der Rückgriff auf Grundlagen und verlässliche Führung zeigt den Weg.",
        "the-lovers": "Entscheidend ist nicht Zustimmung, sondern eine Wahl im Einklang mit Ihren Werten.",
        "the-chariot": "Weniger Zögern und mehr klare Vorwärtsbewegung.",
        "strength": "Geduldige innere Stärke wirkt mehr als Druck.",
        "the-hermit": "Zeit für ruhige Selbstreflexion verbessert die Entscheidung.",
        "wheel-of-fortune": "Das Blatt wendet sich, und Timing ist jetzt entscheidend.",
        "justice": "Klarheit entsteht durch Fakten, Fairness und Verantwortung.",
        "the-hanged-man": "Eine Pause und ein Perspektivwechsel helfen mehr als Hast.",
        "death": "Wenn ein alter Abschnitt endet, beginnt Raum für Neues.",
        "temperance": "Balance und sorgfältige Verbindung verschiedener Elemente sind jetzt der Schlüssel.",
        "the-devil": "Erkennen Sie die Gewohnheit oder Bindung, die Ihre Freiheit einschränkt.",
        "the-tower": "Ein erschüttertes Fundament kann der Beginn ehrlicher Erneuerung sein.",
        "the-star": "Hoffnung und Heilung bringen die Bewegung ruhig zurück.",
        "the-moon": "Lassen Sie sich nicht von Unsicherheit verschlingen; schärfen Sie Ihre Intuition.",
        "the-sun": "Offenheit, Wärme und Klarheit fördern den Erfolg.",
        "judgement": "Blicken Sie zurück und folgen Sie dem Ruf, der jetzt wirklich zählt.",
        "the-world": "Ihre Bemühungen fügen sich zu einem runden Abschluss.",
    },
    "fr": {
        "the-fool": "Un premier pas audacieux peut débloquer la stagnation.",
        "the-magician": "Les résultats arrivent quand la volonté et le savoir-faire sont concentrés.",
        "the-high-priestess": "Il faut maintenant faire davantage confiance à l'intuition qu'au bruit extérieur.",
        "the-empress": "Une attitude nourrissante favorise la croissance dans les relations et le travail.",
        "the-emperor": "L'ordre, la structure et des décisions nettes font avancer la situation.",
        "the-hierophant": "Revenir aux bases et écouter un guide fiable éclaire le chemin.",
        "the-lovers": "L'essentiel n'est pas de plaire à tous, mais de choisir selon vos valeurs.",
        "the-chariot": "Moins d'hésitation, plus d'élan dans une direction claire.",
        "strength": "La persévérance douce sera plus forte que la contrainte.",
        "the-hermit": "Prendre du recul pour réfléchir seul améliore le discernement.",
        "wheel-of-fortune": "Le courant change, et le bon timing compte maintenant.",
        "justice": "La clarté vient des faits, de l'équilibre et de la responsabilité.",
        "the-hanged-man": "Une pause et un nouveau regard aideront plus qu'une action précipitée.",
        "death": "Laisser finir une ancienne phase ouvre la porte à la suivante.",
        "temperance": "L'équilibre et l'intégration patiente sont la bonne voie.",
        "the-devil": "Voyez l'habitude ou l'attachement qui limite votre liberté.",
        "the-tower": "Une base qui s'effondre peut ouvrir un renouveau plus honnête.",
        "the-star": "L'espoir et la guérison rétablissent peu à peu l'élan.",
        "the-moon": "Ne laissez pas l'incertitude vous engloutir; affinez plutôt votre intuition.",
        "the-sun": "La franchise, la chaleur et la clarté favorisent l'avancée.",
        "judgement": "Regardez le passé et répondez à l'appel qui compte vraiment maintenant.",
        "the-world": "Vos efforts convergent vers un accomplissement complet.",
    },
    "it": {
        "the-fool": "Un primo passo coraggioso puo rompere la stagnazione.",
        "the-magician": "I risultati arrivano quando volonta e capacita sono concentrate in una direzione.",
        "the-high-priestess": "Adesso conta piu l'intuizione del rumore esterno.",
        "the-empress": "Un approccio nutriente favorisce crescita nelle relazioni e nel lavoro.",
        "the-emperor": "Ordine, struttura e decisioni chiare fanno avanzare la situazione.",
        "the-hierophant": "Tornare alle basi e a una guida affidabile mostra la strada.",
        "the-lovers": "La chiave non e piacere a tutti, ma scegliere in linea con i propri valori.",
        "the-chariot": "Meno esitazione e piu slancio in una direzione chiara.",
        "strength": "La costanza gentile conta piu della forza bruta.",
        "the-hermit": "Prendersi tempo per riflettere da soli migliora il giudizio.",
        "wheel-of-fortune": "Il vento sta cambiando e il tempismo conta molto.",
        "justice": "La chiarezza nasce da fatti, equilibrio e responsabilita.",
        "the-hanged-man": "Una pausa e un nuovo punto di vista aiutano piu della fretta.",
        "death": "Lasciare finire una fase apre la porta a quella successiva.",
        "temperance": "Equilibrio e integrazione paziente sono la strada giusta.",
        "the-devil": "Riconosci l'abitudine o l'attaccamento che limita la tua liberta.",
        "the-tower": "Una base che crolla puo diventare l'inizio di qualcosa di piu autentico.",
        "the-star": "Speranza e guarigione riportano lentamente il movimento.",
        "the-moon": "Non lasciare che l'incertezza ti inghiotta; affina invece l'intuizione.",
        "the-sun": "Chiarezza, calore e sincerita favoriscono il progresso.",
        "judgement": "Guarda al passato e rispondi alla chiamata che conta davvero ora.",
        "the-world": "I tuoi sforzi si stanno unendo verso un compimento pieno.",
    },
    "zh-cn": {
        "the-fool": "勇敢迈出新的第一步，能打破当前的停滞。",
        "the-magician": "当意志和能力集中到一个方向时，结果会开始显现。",
        "the-high-priestess": "此刻比起外界声音，更应相信内在直觉。",
        "the-empress": "滋养和培育的态度会让关系与工作稳步成长。",
        "the-emperor": "秩序、结构和清晰决定会推动局面前进。",
        "the-hierophant": "回到基础，并参考可靠的建议，会让道路更清楚。",
        "the-lovers": "关键不是取悦所有人，而是选择符合自己价值观的方向。",
        "the-chariot": "减少犹豫，朝一个明确方向推进。",
        "strength": "温和而持续的坚持，比强迫更有力量。",
        "the-hermit": "留出独处思考的时间，会提高判断的准确度。",
        "wheel-of-fortune": "局势的潮流正在转变，现在尤其需要把握时机。",
        "justice": "事实、平衡和责任感会带来清晰。",
        "the-hanged-man": "暂停并换个角度，会比急着行动更有帮助。",
        "death": "让旧阶段结束，才会为接下来的发展打开空间。",
        "temperance": "保持平衡，并耐心整合不同因素，是此刻的关键。",
        "the-devil": "看清限制你自由的习惯或执着，就能重新掌握主动。",
        "the-tower": "被动摇的基础，可能成为更真实更新的开始。",
        "the-star": "希望与疗愈会安静地恢复前进的力量。",
        "the-moon": "不要被不确定吞没，而要在模糊中磨练直觉。",
        "the-sun": "坦率、温暖和清晰会带来进展。",
        "judgement": "回顾过去，并回应此刻真正重要的召唤。",
        "the-world": "你的努力正在汇聚，走向一个完整的完成。",
    },
    "zh-tw": {
        "the-fool": "勇敢踏出新的第一步，能打破當前的停滯。",
        "the-magician": "當意志和能力集中到一個方向時，結果會開始顯現。",
        "the-high-priestess": "此刻比起外界聲音，更應相信內在直覺。",
        "the-empress": "滋養和培育的態度會讓關係與工作穩步成長。",
        "the-emperor": "秩序、結構和清晰決定會推動局面前進。",
        "the-hierophant": "回到基礎，並參考可靠的建議，會讓道路更清楚。",
        "the-lovers": "關鍵不是取悅所有人，而是選擇符合自己價值觀的方向。",
        "the-chariot": "減少猶豫，朝一個明確方向推進。",
        "strength": "溫和而持續的堅持，比強迫更有力量。",
        "the-hermit": "留出獨處思考的時間，會提高判斷的準確度。",
        "wheel-of-fortune": "局勢的潮流正在轉變，現在尤其需要把握時機。",
        "justice": "事實、平衡和責任感會帶來清晰。",
        "the-hanged-man": "暫停並換個角度，會比急著行動更有幫助。",
        "death": "讓舊階段結束，才會為接下來的發展打開空間。",
        "temperance": "保持平衡，並耐心整合不同因素，是此刻的關鍵。",
        "the-devil": "看清限制你自由的習慣或執著，就能重新掌握主動。",
        "the-tower": "被動搖的基礎，可能成為更真實更新的開始。",
        "the-star": "希望與療癒會安靜地恢復前進的力量。",
        "the-moon": "不要被不確定吞沒，而要在模糊中磨練直覺。",
        "the-sun": "坦率、溫暖和清晰會帶來進展。",
        "judgement": "回顧過去，並回應此刻真正重要的召喚。",
        "the-world": "你的努力正在匯聚，走向一個完整的完成。",
    },
    "hi": {
        "the-fool": "नया साहसी कदम वर्तमान ठहराव को तोड़ सकता है।",
        "the-magician": "जब इच्छा और कौशल एक दिशा में केंद्रित होते हैं, परिणाम दिखने लगते हैं।",
        "the-high-priestess": "इस समय बाहरी शोर से अधिक अपनी अंतर्ज्ञान पर भरोसा करें।",
        "the-empress": "देखभाल और पोषण का रवैया संबंधों और काम को स्थिर रूप से बढ़ाता है।",
        "the-emperor": "व्यवस्था, संरचना और स्पष्ट निर्णय स्थिति को आगे बढ़ाते हैं।",
        "the-hierophant": "मूल बातों और भरोसेमंद सलाह पर लौटना रास्ता स्पष्ट करता है।",
        "the-lovers": "मुख्य बात सबको खुश करना नहीं, बल्कि अपने मूल्यों से मेल खाती पसंद करना है।",
        "the-chariot": "हिचक कम करें और एक स्पष्ट दिशा में आगे बढ़ें।",
        "strength": "नरम लेकिन लगातार धैर्य दबाव से अधिक असरदार होगा।",
        "the-hermit": "अकेले सोचने का समय निर्णय को अधिक सटीक बनाएगा।",
        "wheel-of-fortune": "प्रवाह बदल रहा है, और अभी समय की समझ महत्वपूर्ण है।",
        "justice": "तथ्य, संतुलन और जवाबदेही से स्पष्टता आती है।",
        "the-hanged-man": "ठहरना और नया दृष्टिकोण लेना जल्दबाज़ी से अधिक मदद करेगा।",
        "death": "पुराने चरण को समाप्त होने देना अगले चरण के लिए जगह बनाता है।",
        "temperance": "संतुलन और धैर्यपूर्ण समन्वय सही रास्ता है।",
        "the-devil": "उस आदत या आसक्ति को पहचानें जो आपकी स्वतंत्रता सीमित कर रही है।",
        "the-tower": "हिला हुआ आधार अधिक ईमानदार नई शुरुआत बन सकता है।",
        "the-star": "आशा और उपचार धीरे-धीरे गति वापस लाते हैं।",
        "the-moon": "अनिश्चितता में डूबने के बजाय अपनी अंतर्ज्ञान को परिष्कृत करें।",
        "the-sun": "ईमानदारी, गर्मजोशी और स्पष्टता प्रगति लाते हैं।",
        "judgement": "अतीत की समीक्षा करें और उस पुकार का उत्तर दें जो अभी सच में महत्वपूर्ण है।",
        "the-world": "आपके प्रयास पूर्णता की दिशा में एक साथ आ रहे हैं।",
    },
    "pt": {
        "the-fool": "Um primeiro passo corajoso pode romper a estagnação atual.",
        "the-magician": "Resultados aparecem quando vontade e habilidade se concentram numa direção.",
        "the-high-priestess": "Este é um momento para confiar mais na intuição do que no ruído externo.",
        "the-empress": "Uma postura cuidadosa ajuda relações e trabalho a crescerem com estabilidade.",
        "the-emperor": "Ordem, estrutura e decisões claras fazem a situação avançar.",
        "the-hierophant": "Voltar aos fundamentos e a uma orientação confiável revela o caminho.",
        "the-lovers": "A chave não é agradar a todos, mas escolher o que combina com seus valores.",
        "the-chariot": "Reduza a hesitação e avance em uma direção clara.",
        "strength": "Persistência gentil terá mais força do que pressão.",
        "the-hermit": "Um tempo a sós para refletir melhora seu julgamento.",
        "wheel-of-fortune": "A maré está mudando, e o senso de tempo importa agora.",
        "justice": "Clareza vem de fatos, equilíbrio e responsabilidade.",
        "the-hanged-man": "Uma pausa e uma nova perspectiva ajudam mais do que pressa.",
        "death": "Deixar uma fase antiga terminar abre a porta para a próxima.",
        "temperance": "Equilíbrio e integração cuidadosa são a melhor abordagem.",
        "the-devil": "Perceba o hábito ou apego que está limitando sua liberdade.",
        "the-tower": "Uma base abalada pode iniciar uma renovação mais honesta.",
        "the-star": "Esperança e cura restauram o movimento aos poucos.",
        "the-moon": "Não deixe a incerteza engolir você; refine sua intuição.",
        "the-sun": "Honestidade, calor e clareza trazem progresso.",
        "judgement": "Revise o passado e responda ao chamado que realmente importa agora.",
        "the-world": "Seus esforços estão se reunindo em direção à conclusão.",
    },
    "es": {
        "the-fool": "Un primer paso valiente puede romper el estancamiento actual.",
        "the-magician": "Los resultados aparecen cuando voluntad y habilidad se concentran en una dirección.",
        "the-high-priestess": "Este es un momento para confiar más en la intuición que en el ruido exterior.",
        "the-empress": "Una actitud nutritiva ayuda a que relaciones y trabajo crezcan con estabilidad.",
        "the-emperor": "Orden, estructura y decisiones claras hacen avanzar la situación.",
        "the-hierophant": "Volver a lo básico y a una guía confiable muestra el camino.",
        "the-lovers": "La clave no es agradar a todos, sino elegir según tus valores.",
        "the-chariot": "Reduce la duda y avanza en una dirección clara.",
        "strength": "La persistencia amable será más fuerte que la presión.",
        "the-hermit": "Tomarte tiempo a solas para reflexionar mejorará tu juicio.",
        "wheel-of-fortune": "La corriente está cambiando, y el momento adecuado importa ahora.",
        "justice": "La claridad viene de hechos, equilibrio y responsabilidad.",
        "the-hanged-man": "Una pausa y una nueva perspectiva ayudarán más que la prisa.",
        "death": "Dejar que termine una etapa antigua abre la puerta a lo siguiente.",
        "temperance": "El equilibrio y la integración cuidadosa son el mejor enfoque.",
        "the-devil": "Observa el hábito o apego que está limitando tu libertad.",
        "the-tower": "Una base sacudida puede iniciar una renovación más honesta.",
        "the-star": "La esperanza y la sanación restauran el movimiento poco a poco.",
        "the-moon": "No dejes que la incertidumbre te absorba; afina tu intuición.",
        "the-sun": "Honestidad, calidez y claridad traen progreso.",
        "judgement": "Revisa el pasado y responde al llamado que realmente importa ahora.",
        "the-world": "Tus esfuerzos se están uniendo hacia una conclusión completa.",
    },
}

REVERSED_CARD_MEANINGS: Final[dict[str, dict[str, str]]] = {
    "ja": {
        "the-fool": "勢いだけで飛び込むより、準備不足や現実逃避を見直す段階です。",
        "the-magician": "力はあるのに焦点が散り、言葉や計画が空回りしやすい局面です。",
        "the-high-priestess": "直感と不安が混ざりやすく、秘密や思い込みを整理する必要があります。",
        "the-empress": "与えすぎや甘えが成長を鈍らせているため、境界線を整える時です。",
        "the-emperor": "支配や頑固さが強まりやすく、柔軟な運用に戻すことが課題です。",
        "the-hierophant": "常識や他人の正解に寄りすぎず、自分に合う型へ組み替える段階です。",
        "the-lovers": "気持ちと選択が一致せず、関係性や優先順位を再確認する必要があります。",
        "the-chariot": "前に進みたい気持ちに対して方向が定まらず、制御を取り戻す時です。",
        "strength": "我慢が限界に近づいているため、優しさと自己防衛のバランスが必要です。",
        "the-hermit": "内省が孤立や考えすぎに傾いており、外からの視点を少し入れる時です。",
        "wheel-of-fortune": "流れが読みにくい時期なので、無理に動かずタイミングを待つ判断が合います。",
        "justice": "事実確認や責任の線引きが曖昧で、公平さを取り戻すことが先決です。",
        "the-hanged-man": "待つ理由が見えなくなり、停滞を受け入れすぎている可能性があります。",
        "death": "終わらせるべきものに未練が残り、変化への抵抗が次の展開を遅らせています。",
        "temperance": "無理に合わせようとして調和が崩れているため、配分を見直す必要があります。",
        "the-devil": "執着の正体は見え始めていますが、手放すには具体的な距離の取り方が必要です。",
        "the-tower": "大きな崩壊を避けたいなら、小さな違和感の段階で修正することが重要です。",
        "the-star": "希望は残っていますが、期待だけで進まず回復の時間を確保する局面です。",
        "the-moon": "不安が判断を曇らせやすく、確かな情報と曖昧な想像を分ける必要があります。",
        "the-sun": "喜びや成果が見えにくくても、素直な確認と小さな成功の積み直しが効きます。",
        "judgement": "過去の評価に縛られ、今の呼びかけを聞き逃していないか見直す時です。",
        "the-world": "完成目前で詰めが甘くなりやすく、未完了の一点を仕上げる段階です。",
    },
    "en": {
        "the-fool": "This calls for checking preparation and avoidance before taking a leap.",
        "the-magician": "Your tools are present, but scattered focus can make words and plans misfire.",
        "the-high-priestess": "Intuition and anxiety may be tangled, so hidden assumptions need sorting.",
        "the-empress": "Overgiving or dependency may be slowing growth; clearer boundaries help.",
        "the-emperor": "Control or rigidity may be crowding out the flexibility the situation needs.",
        "the-hierophant": "Borrowed rules are too loud; reshape the pattern so it actually fits you.",
        "the-lovers": "Feelings and choices are not aligned yet, so priorities need another look.",
        "the-chariot": "The desire to move is real, but direction and control need to be restored first.",
        "strength": "Endurance is wearing thin; balance kindness with self-protection.",
        "the-hermit": "Reflection may be turning into isolation or overthinking, so invite one outside view.",
        "wheel-of-fortune": "The timing is unstable; waiting for a clearer opening is wiser than forcing movement.",
        "justice": "Facts and responsibility are blurred, and fairness must be rebuilt before deciding.",
        "the-hanged-man": "Waiting has lost its purpose, and passive delay may now be the real obstacle.",
        "death": "Resistance to an ending is slowing the transition that wants to happen.",
        "temperance": "Forced compromise is disrupting balance; the proportions need adjustment.",
        "the-devil": "The attachment is becoming visible, but release needs a practical boundary.",
        "the-tower": "A smaller correction now can prevent a more disruptive collapse later.",
        "the-star": "Hope remains, but recovery needs time rather than expectation alone.",
        "the-moon": "Anxiety can distort judgment; separate reliable facts from imagined fears.",
        "the-sun": "Progress may feel dim, but honest check-ins and small wins rebuild clarity.",
        "judgement": "Old judgments may be drowning out the call that matters now.",
        "the-world": "Completion is close, but one unfinished detail still needs attention.",
    },
    "ru": {
        "the-fool": "Сначала стоит проверить подготовку и желание убежать от реальности, а потом делать шаг.",
        "the-magician": "Ресурсы есть, но рассеянный фокус может сбивать слова и планы.",
        "the-high-priestess": "Интуиция смешивается с тревогой, поэтому скрытые допущения нужно разобрать.",
        "the-empress": "Чрезмерная отдача или зависимость тормозит рост; помогут ясные границы.",
        "the-emperor": "Контроль или упрямство вытесняют гибкость, которая сейчас нужна.",
        "the-hierophant": "Чужие правила звучат слишком громко; форму нужно подстроить под себя.",
        "the-lovers": "Чувства и выбор пока не совпадают, поэтому приоритеты требуют пересмотра.",
        "the-chariot": "Желание двигаться есть, но сначала нужно вернуть направление и управление.",
        "strength": "Терпение истончается; важно совместить мягкость с самозащитой.",
        "the-hermit": "Размышление может перейти в изоляцию, поэтому полезен внешний взгляд.",
        "wheel-of-fortune": "Время нестабильно; лучше дождаться более ясного окна, чем давить на ситуацию.",
        "justice": "Факты и ответственность размыты, и сначала нужно восстановить справедливость.",
        "the-hanged-man": "Ожидание потеряло смысл, и пассивная задержка может стать препятствием.",
        "death": "Сопротивление завершению замедляет переход, который уже назрел.",
        "temperance": "Вынужденный компромисс нарушает баланс; пропорции нужно пересмотреть.",
        "the-devil": "Привязанность уже видна, но освобождение требует практической границы.",
        "the-tower": "Маленькая правка сейчас может предотвратить более резкое разрушение позже.",
        "the-star": "Надежда остается, но восстановлению нужно время, а не одни ожидания.",
        "the-moon": "Тревога искажает суждение; отделите факты от воображаемых страхов.",
        "the-sun": "Прогресс может быть неочевиден, но честная проверка и малые успехи возвращают ясность.",
        "judgement": "Старые оценки могут заглушать зов, важный именно сейчас.",
        "the-world": "Завершение близко, но одна незаконченная деталь еще требует внимания.",
    },
    "de": {
        "the-fool": "Pruefen Sie Vorbereitung und Ausweichverhalten, bevor Sie springen.",
        "the-magician": "Die Mittel sind da, doch zerstreuter Fokus kann Worte und Plaene entgleisen lassen.",
        "the-high-priestess": "Intuition und Angst vermischen sich; verborgene Annahmen brauchen Ordnung.",
        "the-empress": "Zu viel Geben oder Abhaengigkeit bremst Wachstum; klare Grenzen helfen.",
        "the-emperor": "Kontrolle oder Starrheit verdraengen die Flexibilitaet, die jetzt noetig ist.",
        "the-hierophant": "Fremde Regeln sind zu laut; passen Sie die Form an Ihr eigenes Leben an.",
        "the-lovers": "Gefuehle und Wahl sind noch nicht im Einklang; Prioritaeten brauchen Pruefung.",
        "the-chariot": "Der Wille zur Bewegung ist da, doch Richtung und Steuerung muessen zuerst zurueckkehren.",
        "strength": "Die Geduld wird duenn; verbinden Sie Freundlichkeit mit Selbstschutz.",
        "the-hermit": "Reflexion kann in Isolation kippen; ein Blick von aussen hilft.",
        "wheel-of-fortune": "Das Timing ist unruhig; warten Sie auf ein klareres Fenster statt zu druecken.",
        "justice": "Fakten und Verantwortung sind unscharf; Fairness muss zuerst wiederhergestellt werden.",
        "the-hanged-man": "Das Warten hat seinen Zweck verloren und kann selbst zum Hindernis werden.",
        "death": "Widerstand gegen ein Ende verlangsamt den faelligen Uebergang.",
        "temperance": "Erzwungener Ausgleich stoert die Balance; die Verteilung braucht Korrektur.",
        "the-devil": "Die Bindung wird sichtbar, doch Loesung braucht eine praktische Grenze.",
        "the-tower": "Eine kleine Korrektur jetzt kann einen groesseren Bruch spaeter verhindern.",
        "the-star": "Hoffnung bleibt, aber Heilung braucht Zeit statt nur Erwartung.",
        "the-moon": "Angst kann das Urteil verzerren; trennen Sie Fakten von Vorstellungen.",
        "the-sun": "Fortschritt wirkt gedimmt, doch ehrliche Klaerung und kleine Erfolge bringen Licht zurueck.",
        "judgement": "Alte Urteile koennen den Ruf der Gegenwart uebertoenen.",
        "the-world": "Der Abschluss ist nah, aber ein offener Punkt braucht noch Sorgfalt.",
    },
    "fr": {
        "the-fool": "Verifiez la preparation et l'evitement avant de faire le saut.",
        "the-magician": "Les moyens existent, mais un focus disperse peut faire deraper paroles et plans.",
        "the-high-priestess": "Intuition et anxiete se melangent; les suppositions cachees doivent etre triees.",
        "the-empress": "Trop donner ou trop dependre freine la croissance; des limites claires aideront.",
        "the-emperor": "Le controle ou la rigidite peut etouffer la souplesse necessaire.",
        "the-hierophant": "Les regles empruntees prennent trop de place; adaptez le cadre a votre realite.",
        "the-lovers": "Sentiments et choix ne sont pas encore alignes; les priorites demandent examen.",
        "the-chariot": "L'envie d'avancer est la, mais direction et maitrise doivent revenir d'abord.",
        "strength": "La patience s'use; equilibrez douceur et protection de soi.",
        "the-hermit": "La reflexion peut devenir isolement; un regard exterieur sera utile.",
        "wheel-of-fortune": "Le timing est instable; mieux vaut attendre une ouverture claire que forcer.",
        "justice": "Les faits et les responsabilites sont flous; l'equite doit etre retablie.",
        "the-hanged-man": "L'attente a perdu son sens et peut devenir l'obstacle principal.",
        "death": "La resistance a une fin ralentit la transition qui veut se faire.",
        "temperance": "Un compromis force trouble l'equilibre; les proportions doivent etre revues.",
        "the-devil": "L'attachement devient visible, mais s'en liberer demande une limite concrete.",
        "the-tower": "Une petite correction maintenant peut eviter une rupture plus forte plus tard.",
        "the-star": "L'espoir demeure, mais la guerison demande du temps plutot que des attentes seules.",
        "the-moon": "L'anxiete peut deformer le jugement; separez les faits des peurs imaginees.",
        "the-sun": "La progression semble moins lumineuse, mais des verifications sinceres et de petits succes ramenent la clarte.",
        "judgement": "D'anciens jugements peuvent couvrir l'appel important du present.",
        "the-world": "L'accomplissement est proche, mais un detail inacheve demande encore du soin.",
    },
    "it": {
        "the-fool": "Prima del salto, verifica preparazione ed eventuale fuga dalla realta.",
        "the-magician": "Gli strumenti ci sono, ma un focus disperso puo far inciampare parole e piani.",
        "the-high-priestess": "Intuizione e ansia si mescolano; le ipotesi nascoste vanno chiarite.",
        "the-empress": "Dare troppo o dipendere troppo rallenta la crescita; servono confini chiari.",
        "the-emperor": "Controllo o rigidita possono soffocare la flessibilita necessaria.",
        "the-hierophant": "Le regole altrui pesano troppo; adatta la forma alla tua realta.",
        "the-lovers": "Sentimenti e scelta non sono ancora allineati; le priorita vanno riviste.",
        "the-chariot": "La voglia di avanzare c'e, ma prima vanno recuperati direzione e controllo.",
        "strength": "La pazienza si sta consumando; bilancia gentilezza e autoprotezione.",
        "the-hermit": "La riflessione puo diventare isolamento; uno sguardo esterno aiuta.",
        "wheel-of-fortune": "Il tempismo e instabile; meglio attendere un'apertura chiara che forzare.",
        "justice": "Fatti e responsabilita sono sfocati; va ricostruita l'equita prima di decidere.",
        "the-hanged-man": "L'attesa ha perso scopo e puo essere diventata l'ostacolo principale.",
        "death": "La resistenza a una fine rallenta la transizione gia pronta.",
        "temperance": "Un compromesso forzato rompe l'equilibrio; le proporzioni vanno corrette.",
        "the-devil": "L'attaccamento e visibile, ma per liberarsene serve un confine concreto.",
        "the-tower": "Una piccola correzione ora puo evitare un crollo piu forte dopo.",
        "the-star": "La speranza resta, ma la guarigione richiede tempo e non solo aspettative.",
        "the-moon": "L'ansia puo deformare il giudizio; separa i fatti dalle paure immaginate.",
        "the-sun": "Il progresso sembra meno luminoso, ma verifiche sincere e piccoli successi riportano chiarezza.",
        "judgement": "Vecchi giudizi possono coprire la chiamata importante del presente.",
        "the-world": "Il compimento e vicino, ma un dettaglio incompleto richiede ancora cura.",
    },
    "zh-cn": {
        "the-fool": "在跃出之前，先检查准备不足和逃避现实的倾向。",
        "the-magician": "资源已经具备，但分散的焦点会让语言和计划失准。",
        "the-high-priestess": "直觉和焦虑可能混在一起，需要整理隐藏的假设。",
        "the-empress": "过度付出或依赖正在拖慢成长，清晰边界会有帮助。",
        "the-emperor": "控制或固执可能压过了此刻需要的灵活性。",
        "the-hierophant": "外来的规则声音太大，需要把框架调整成适合自己的形式。",
        "the-lovers": "感受和选择尚未一致，因此需要重新检查优先顺序。",
        "the-chariot": "前进的意愿真实存在，但方向和掌控需要先找回来。",
        "strength": "耐心正在变薄，需要在温柔和自我保护之间取得平衡。",
        "the-hermit": "反省可能变成孤立或过度思考，适合加入一个外部视角。",
        "wheel-of-fortune": "时机不稳定，与其强推，不如等待更清楚的窗口。",
        "justice": "事实和责任变得模糊，必须先重建公平感。",
        "the-hanged-man": "等待已经失去目的，被动拖延可能才是真正的障碍。",
        "death": "对结束的抵抗正在拖慢已经到来的转变。",
        "temperance": "被迫妥协正在破坏平衡，需要重新调整比例。",
        "the-devil": "执着已经开始显现，但释放它需要具体的界线。",
        "the-tower": "现在做小修正，可以避免之后更剧烈的崩塌。",
        "the-star": "希望仍在，但恢复需要时间，而不只是期待。",
        "the-moon": "焦虑会扭曲判断，需要把可靠事实和想象中的恐惧分开。",
        "the-sun": "进展可能不明显，但诚实确认和小成功会重新带来清晰。",
        "judgement": "旧有评价可能盖过了此刻真正重要的召唤。",
        "the-world": "完成已经接近，但仍有一个未完成的细节需要处理。",
    },
    "zh-tw": {
        "the-fool": "在躍出之前，先檢查準備不足和逃避現實的傾向。",
        "the-magician": "資源已經具備，但分散的焦點會讓語言和計畫失準。",
        "the-high-priestess": "直覺和焦慮可能混在一起，需要整理隱藏的假設。",
        "the-empress": "過度付出或依賴正在拖慢成長，清晰界線會有幫助。",
        "the-emperor": "控制或固執可能壓過了此刻需要的彈性。",
        "the-hierophant": "外來的規則聲音太大，需要把框架調整成適合自己的形式。",
        "the-lovers": "感受和選擇尚未一致，因此需要重新檢查優先順序。",
        "the-chariot": "前進的意願真實存在，但方向和掌控需要先找回來。",
        "strength": "耐心正在變薄，需要在溫柔和自我保護之間取得平衡。",
        "the-hermit": "反省可能變成孤立或過度思考，適合加入一個外部視角。",
        "wheel-of-fortune": "時機不穩定，與其強推，不如等待更清楚的窗口。",
        "justice": "事實和責任變得模糊，必須先重建公平感。",
        "the-hanged-man": "等待已經失去目的，被動拖延可能才是真正的障礙。",
        "death": "對結束的抵抗正在拖慢已經到來的轉變。",
        "temperance": "被迫妥協正在破壞平衡，需要重新調整比例。",
        "the-devil": "執著已經開始顯現，但釋放它需要具體的界線。",
        "the-tower": "現在做小修正，可以避免之後更劇烈的崩塌。",
        "the-star": "希望仍在，但恢復需要時間，而不只是期待。",
        "the-moon": "焦慮會扭曲判斷，需要把可靠事實和想像中的恐懼分開。",
        "the-sun": "進展可能不明顯，但誠實確認和小成功會重新帶來清晰。",
        "judgement": "舊有評價可能蓋過了此刻真正重要的召喚。",
        "the-world": "完成已經接近，但仍有一個未完成的細節需要處理。",
    },
    "hi": {
        "the-fool": "छलांग लगाने से पहले तैयारी और बचने की प्रवृत्ति की जांच करें।",
        "the-magician": "साधन मौजूद हैं, लेकिन बिखरा ध्यान शब्दों और योजनाओं को भटका सकता है।",
        "the-high-priestess": "अंतर्ज्ञान और चिंता उलझ सकती हैं, इसलिए छिपी धारणाओं को साफ करें।",
        "the-empress": "बहुत अधिक देना या निर्भरता विकास को धीमा कर सकती है; स्पष्ट सीमाएं मदद करेंगी।",
        "the-emperor": "नियंत्रण या कठोरता उस लचीलापन को दबा सकती है जिसकी अभी जरूरत है।",
        "the-hierophant": "उधार लिए नियम बहुत हावी हैं; ढांचे को अपने अनुरूप बनाएं।",
        "the-lovers": "भावना और चुनाव अभी साथ नहीं हैं, इसलिए प्राथमिकताओं को फिर देखें।",
        "the-chariot": "आगे बढ़ने की इच्छा है, लेकिन पहले दिशा और नियंत्रण लौटाना होगा।",
        "strength": "धैर्य कम हो रहा है; करुणा और आत्म-सुरक्षा में संतुलन रखें।",
        "the-hermit": "चिंतन अलगाव या अधिक सोच में बदल सकता है; एक बाहरी दृष्टि लें।",
        "wheel-of-fortune": "समय अस्थिर है; जबरदस्ती से बेहतर स्पष्ट अवसर की प्रतीक्षा है।",
        "justice": "तथ्य और जिम्मेदारी धुंधले हैं; निर्णय से पहले निष्पक्षता लौटाएं।",
        "the-hanged-man": "प्रतीक्षा का उद्देश्य खो गया है, और निष्क्रिय विलंब बाधा बन सकता है।",
        "death": "अंत का विरोध आवश्यक परिवर्तन को धीमा कर रहा है।",
        "temperance": "मजबूर समझौता संतुलन बिगाड़ रहा है; अनुपात सुधारें।",
        "the-devil": "आसक्ति दिख रही है, लेकिन मुक्त होने के लिए व्यावहारिक सीमा चाहिए।",
        "the-tower": "अभी छोटी सुधारात्मक कार्रवाई आगे बड़े टूटन से बचा सकती है।",
        "the-star": "आशा बनी है, पर उपचार को केवल उम्मीद नहीं, समय चाहिए।",
        "the-moon": "चिंता निर्णय को विकृत कर सकती है; तथ्यों और कल्पित डर को अलग करें।",
        "the-sun": "प्रगति मंद लग सकती है, लेकिन ईमानदार जांच और छोटे सफल कदम स्पष्टता लौटाते हैं।",
        "judgement": "पुराने निर्णय वर्तमान की महत्वपूर्ण पुकार को दबा सकते हैं।",
        "the-world": "पूर्णता पास है, लेकिन एक अधूरा विवरण अभी ध्यान चाहता है।",
    },
    "pt": {
        "the-fool": "Antes do salto, verifique preparo e possível fuga da realidade.",
        "the-magician": "Os recursos existem, mas foco disperso pode fazer palavras e planos falharem.",
        "the-high-priestess": "Intuição e ansiedade podem se misturar; organize pressupostos ocultos.",
        "the-empress": "Dar demais ou depender demais pode frear o crescimento; limites claros ajudam.",
        "the-emperor": "Controle ou rigidez podem sufocar a flexibilidade necessária agora.",
        "the-hierophant": "Regras emprestadas estão altas demais; adapte o padrão à sua realidade.",
        "the-lovers": "Sentimentos e escolhas ainda não estão alinhados; revise prioridades.",
        "the-chariot": "A vontade de avançar existe, mas direção e controle precisam voltar primeiro.",
        "strength": "A resistência está se desgastando; equilibre gentileza com autoproteção.",
        "the-hermit": "Reflexão pode virar isolamento; um olhar externo ajuda.",
        "wheel-of-fortune": "O timing está instável; espere uma abertura mais clara em vez de forçar.",
        "justice": "Fatos e responsabilidades estão borrados; recupere a justiça antes de decidir.",
        "the-hanged-man": "A espera perdeu propósito e pode ter virado o principal obstáculo.",
        "death": "Resistir a um fim está atrasando a transição necessária.",
        "temperance": "Um compromisso forçado está quebrando o equilíbrio; ajuste as proporções.",
        "the-devil": "O apego está visível, mas soltá-lo exige um limite prático.",
        "the-tower": "Uma pequena correção agora pode evitar uma ruptura maior depois.",
        "the-star": "A esperança permanece, mas a cura precisa de tempo, não apenas expectativa.",
        "the-moon": "A ansiedade pode distorcer o julgamento; separe fatos de medos imaginados.",
        "the-sun": "O progresso pode parecer fraco, mas verificações honestas e pequenas vitórias devolvem clareza.",
        "judgement": "Julgamentos antigos podem abafar o chamado importante do presente.",
        "the-world": "A conclusão está próxima, mas um detalhe inacabado ainda precisa de cuidado.",
    },
    "es": {
        "the-fool": "Antes de saltar, revisa la preparación y la posible evasión.",
        "the-magician": "Los recursos existen, pero el foco disperso puede hacer fallar palabras y planes.",
        "the-high-priestess": "Intuición y ansiedad pueden mezclarse; ordena las suposiciones ocultas.",
        "the-empress": "Dar demasiado o depender demasiado puede frenar el crecimiento; los límites claros ayudan.",
        "the-emperor": "El control o la rigidez pueden ahogar la flexibilidad que ahora hace falta.",
        "the-hierophant": "Las reglas prestadas pesan demasiado; adapta el marco a tu realidad.",
        "the-lovers": "Sentimientos y elección aún no están alineados; revisa prioridades.",
        "the-chariot": "El deseo de avanzar existe, pero antes deben volver dirección y control.",
        "strength": "La resistencia se está agotando; equilibra amabilidad con autoprotección.",
        "the-hermit": "La reflexión puede volverse aislamiento; una mirada externa ayudará.",
        "wheel-of-fortune": "El momento es inestable; espera una apertura más clara en vez de forzar.",
        "justice": "Hechos y responsabilidades están borrosos; recupera la equidad antes de decidir.",
        "the-hanged-man": "La espera perdió propósito y puede ser el obstáculo principal.",
        "death": "Resistir un final está retrasando la transición necesaria.",
        "temperance": "Un compromiso forzado rompe el equilibrio; ajusta las proporciones.",
        "the-devil": "El apego ya se ve, pero soltarlo requiere un límite práctico.",
        "the-tower": "Una pequeña corrección ahora puede evitar una ruptura mayor después.",
        "the-star": "La esperanza permanece, pero sanar requiere tiempo, no solo expectativas.",
        "the-moon": "La ansiedad puede distorsionar el juicio; separa hechos de miedos imaginados.",
        "the-sun": "El progreso puede verse tenue, pero revisiones honestas y pequeños logros devuelven claridad.",
        "judgement": "Juicios antiguos pueden tapar el llamado importante del presente.",
        "the-world": "La conclusión está cerca, pero un detalle pendiente aún necesita cuidado.",
    },
}


def normalize_locale(locale: str | None) -> str:
    if locale in SUPPORTED_LOCALES:
        return locale
    return DEFAULT_LOCALE


def localize_card_meaning(slug: str, orientation: str, locale: str) -> str:
    normalized_locale = normalize_locale(locale)
    base_meaning = CARD_MEANINGS.get(normalized_locale, CARD_MEANINGS[DEFAULT_LOCALE]).get(
        slug,
        CARD_MEANINGS[DEFAULT_LOCALE].get(slug, ""),
    )
    if orientation != "reversed":
        return base_meaning

    return REVERSED_CARD_MEANINGS.get(normalized_locale, REVERSED_CARD_MEANINGS[DEFAULT_LOCALE]).get(
        slug,
        REVERSED_CARD_MEANINGS[DEFAULT_LOCALE].get(slug, base_meaning),
    )


def localize_cards(cards: list[dict], locale: str) -> list[dict]:
    normalized_locale = normalize_locale(locale)
    localized: list[dict] = []
    for card in cards:
        localized_card = dict(card)
        slug = str(localized_card.get("slug", ""))
        orientation = str(localized_card.get("orientation", "upright"))
        if slug:
            localized_card["meaning"] = localize_card_meaning(slug, orientation, normalized_locale)
        localized.append(localized_card)
    return localized


def build_interpretation(question: str, cards: list[dict], locale: str, guidance: LearningGuidance | None = None) -> str:
    normalized_locale = normalize_locale(locale)
    present_keyword = cards[1]["keywords"][0]
    future_keyword = cards[2]["keywords"][0]
    positions = POSITION_LABELS[normalized_locale]

    templates = {
        "ja": (
            f"質問「{question}」に対して、{positions['past']}は {cards[0]['name']} が示す流れ、"
            f"{positions['present']}は {cards[1]['name']} が示す課題、{positions['future']}は {cards[2]['name']} が示す可能性です。"
            f" 今は {present_keyword} を軸に判断し、未来に向けて {future_keyword} を意識すると良いでしょう。"
        ),
        "en": (
            f"For your question \"{question}\", the {positions['past']} is shaped by {cards[0]['name']}, "
            f"the {positions['present']} is defined by {cards[1]['name']}, and the {positions['future']} points to {cards[2]['name']}. "
            f"Right now, decide around {present_keyword} and move toward {future_keyword}."
        ),
        "ru": (
            f"По вопросу \"{question}\" карта {cards[0]['name']} показывает {positions['past']}, "
            f"{cards[1]['name']} описывает {positions['present']}, а {cards[2]['name']} указывает на {positions['future']}. "
            f"Сейчас опирайтесь на {present_keyword} и двигайтесь в сторону {future_keyword}."
        ),
        "de": (
            f"Zur Frage \"{question}\" zeigt {cards[0]['name']} die {positions['past']}, "
            f"{cards[1]['name']} beschreibt die {positions['present']}, und {cards[2]['name']} weist auf die {positions['future']} hin. "
            f"Richten Sie Ihre Entscheidung jetzt an {present_keyword} aus und gehen Sie in Richtung {future_keyword}."
        ),
        "fr": (
            f"Pour la question \"{question}\", {cards[0]['name']} parle du {positions['past']}, "
            f"{cards[1]['name']} decrit le {positions['present']}, et {cards[2]['name']} indique l'{positions['future']}. "
            f"Pour l'instant, appuyez-vous sur {present_keyword} et avancez vers {future_keyword}."
        ),
        "it": (
            f"Per la domanda \"{question}\", {cards[0]['name']} mostra il {positions['past']}, "
            f"{cards[1]['name']} descrive il {positions['present']}, e {cards[2]['name']} indica il {positions['future']}. "
            f"Ora conviene decidere attorno a {present_keyword} e muoversi verso {future_keyword}."
        ),
        "zh-cn": (
            f"针对问题「{question}」，{positions['past']}由 {cards[0]['name']} 所代表的流向塑造，"
            f"{positions['present']}由 {cards[1]['name']} 所显示的课题定义，{positions['future']}则指向 {cards[2]['name']} 的可能性。"
            f" 现在适合以 {present_keyword} 为判断轴，并朝着 {future_keyword} 的方向行动。"
        ),
        "zh-tw": (
            f"針對問題「{question}」，{positions['past']}由 {cards[0]['name']} 所代表的流向塑造，"
            f"{positions['present']}由 {cards[1]['name']} 所顯示的課題定義，{positions['future']}則指向 {cards[2]['name']} 的可能性。"
            f" 現在適合以 {present_keyword} 為判斷軸，並朝著 {future_keyword} 的方向行動。"
        ),
        "hi": (
            f"आपके प्रश्न \"{question}\" के लिए {positions['past']} को {cards[0]['name']} आकार देता है, "
            f"{positions['present']} को {cards[1]['name']} परिभाषित करता है, और {positions['future']} {cards[2]['name']} की संभावना दिखाता है। "
            f"अभी {present_keyword} के आधार पर निर्णय लें और {future_keyword} की दिशा में बढ़ें।"
        ),
        "pt": (
            f"Para a pergunta \"{question}\", o {positions['past']} é moldado por {cards[0]['name']}, "
            f"o {positions['present']} é definido por {cards[1]['name']}, e o {positions['future']} aponta para {cards[2]['name']}. "
            f"Agora, decida em torno de {present_keyword} e avance em direção a {future_keyword}."
        ),
        "es": (
            f"Para la pregunta \"{question}\", el {positions['past']} está marcado por {cards[0]['name']}, "
            f"el {positions['present']} lo define {cards[1]['name']}, y el {positions['future']} apunta a {cards[2]['name']}. "
            f"Ahora conviene decidir en torno a {present_keyword} y avanzar hacia {future_keyword}."
        ),
    }
    interpretation = templates[normalized_locale]

    if guidance:
        extra = {
            "ja": {
                "action": f" 次の一手としては、{present_keyword} を意識しながら小さく一度動き、反応を見てから広げる進め方が適しています。",
                "timing": " 変化の手応えを見極める目安は、これから 2 週間前後です。",
                "cautious": " ただし状況の揺れもあるため、断定せずに途中で軌道修正できる余白を残してください。",
                "retrieval": " 過去の近い相談では、似た迷いは段階的に判断したケースで整いやすい傾向がありました。",
            },
            "en": {
                "action": f" As a next step, take one small action around {present_keyword}, then expand only after you see the response.",
                "timing": " A useful timing check is the next two weeks.",
                "cautious": " Leave room to adjust rather than forcing a fixed conclusion.",
                "retrieval": " Similar past cases tended to improve when decisions were made in stages.",
            },
            "ru": {
                "action": f" В качестве следующего шага сделайте одно небольшое действие, опираясь на {present_keyword}, а затем расширяйте его по результату.",
                "timing": " Хороший срок для проверки изменений - ближайшие две недели.",
                "cautious": " Оставьте себе пространство для корректировки, а не для жесткого вывода.",
                "retrieval": " Похожие случаи чаще выравнивались, когда решение принималось поэтапно.",
            },
            "de": {
                "action": f" Als nächsten Schritt setzen Sie eine kleine Handlung rund um {present_keyword}, und erweitern Sie sie erst nach der Reaktion.",
                "timing": " Ein guter Zeitrahmen zur Beobachtung sind die nächsten zwei Wochen.",
                "cautious": " Lassen Sie Raum für Anpassungen, statt alles sofort festzulegen.",
                "retrieval": " Vergleichbare Fälle entwickelten sich besser, wenn Entscheidungen schrittweise getroffen wurden.",
            },
            "fr": {
                "action": f" Comme prochaine etape, posez un petit acte autour de {present_keyword}, puis elargissez seulement apres avoir vu la reaction.",
                "timing": " Un bon repere temporel est les deux prochaines semaines.",
                "cautious": " Gardez une marge d'ajustement plutot que de figer une conclusion.",
                "retrieval": " Des cas proches evoluaient mieux quand la decision etait prise par etapes.",
            },
            "it": {
                "action": f" Come passo successivo, fai una piccola azione attorno a {present_keyword} e amplia solo dopo aver visto la risposta.",
                "timing": " Un buon orizzonte per valutare i cambiamenti sono le prossime due settimane.",
                "cautious": " Lascia spazio agli aggiustamenti invece di forzare una conclusione rigida.",
                "retrieval": " Nei casi simili le cose miglioravano quando le decisioni venivano prese per gradi.",
            },
            "zh-cn": {
                "action": f" 下一步适合围绕 {present_keyword} 先做一个小行动，观察反应后再扩大。",
                "timing": " 接下来两周左右适合作为观察变化的时间点。",
                "cautious": " 不要急着下定论，保留中途调整的空间。",
                "retrieval": " 过去相近的咨询中，分阶段判断的案例更容易整理出方向。",
            },
            "zh-tw": {
                "action": f" 下一步適合圍繞 {present_keyword} 先做一個小行動，觀察反應後再擴大。",
                "timing": " 接下來兩週左右適合作為觀察變化的時間點。",
                "cautious": " 不要急著下定論，保留中途調整的空間。",
                "retrieval": " 過去相近的諮詢中，分階段判斷的案例更容易整理出方向。",
            },
            "hi": {
                "action": f" अगले कदम के रूप में {present_keyword} के आसपास एक छोटा कदम लें, फिर प्रतिक्रिया देखकर आगे बढ़ाएं।",
                "timing": " बदलाव को परखने के लिए अगले दो सप्ताह उपयोगी संकेत देंगे।",
                "cautious": " कठोर निष्कर्ष पर न जाएं; बीच में सुधार की जगह रखें।",
                "retrieval": " समान पुराने मामलों में चरणबद्ध निर्णय से स्थिति अधिक स्पष्ट हुई थी।",
            },
            "pt": {
                "action": f" Como próximo passo, faça uma pequena ação em torno de {present_keyword} e só amplie depois de ver a resposta.",
                "timing": " As próximas duas semanas são um bom período para observar mudanças.",
                "cautious": " Deixe espaço para ajustar em vez de forçar uma conclusão rígida.",
                "retrieval": " Em casos parecidos, decisões por etapas tenderam a organizar melhor a situação.",
            },
            "es": {
                "action": f" Como siguiente paso, haz una acción pequeña alrededor de {present_keyword} y amplía solo después de ver la respuesta.",
                "timing": " Las próximas dos semanas son una buena referencia para observar cambios.",
                "cautious": " Deja margen para ajustar en vez de forzar una conclusión fija.",
                "retrieval": " En casos similares, decidir por etapas tendió a ordenar mejor la situación.",
            },
        }[normalized_locale]
        if guidance.include_action_step:
            interpretation += extra["action"]
        if guidance.include_timing_hint:
            interpretation += extra["timing"]
        if guidance.use_cautious_tone:
            interpretation += extra["cautious"]
        if guidance.retrieval_context:
            interpretation += extra["retrieval"]

    return interpretation
