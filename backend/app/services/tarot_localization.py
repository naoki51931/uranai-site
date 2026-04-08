from __future__ import annotations

from typing import Final

from app.services.learning import LearningGuidance


SUPPORTED_LOCALES: Final[set[str]] = {"ja", "en", "ru", "de", "fr", "it"}
DEFAULT_LOCALE = "ja"

POSITION_LABELS: Final[dict[str, dict[str, str]]] = {
    "ja": {"past": "過去", "present": "現在", "future": "未来"},
    "en": {"past": "past", "present": "present", "future": "future"},
    "ru": {"past": "прошлое", "present": "настоящее", "future": "будущее"},
    "de": {"past": "Vergangenheit", "present": "Gegenwart", "future": "Zukunft"},
    "fr": {"past": "passé", "present": "présent", "future": "avenir"},
    "it": {"past": "passato", "present": "presente", "future": "futuro"},
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

    reversed_prefixes = {
        "ja": f"逆位置では、{base_meaning} ただし焦りや空回りには注意が必要です。",
        "en": f"In reverse, {base_meaning} Be careful of haste or wasted effort.",
        "ru": f"В перевернутом положении: {base_meaning} Важно избегать спешки и пустой траты сил.",
        "de": f"In umgekehrter Lage gilt: {base_meaning} Achten Sie dabei auf Hast und Energieverlust.",
        "fr": f"En position renversee, {base_meaning} Attention a la precipitation et aux efforts mal diriges.",
        "it": f"In posizione rovesciata, {base_meaning} Fai attenzione alla fretta e alla dispersione di energie.",
    }
    return reversed_prefixes[normalized_locale]


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
