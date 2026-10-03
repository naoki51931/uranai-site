package com.moonarcana.offline

import kotlin.random.Random

data class TarotCard(val slug:String,val name:String,val keywords:List<String>,val meaning:String)
data class DrawnCard(val card:TarotCard,val position:String,val reversed:Boolean)

object Tarot {
    val cards = listOf(
        TarotCard("the-fool","The Fool",listOf("beginnings","curiosity","leap of faith"),"新しい流れに飛び込む勇気が、停滞を動かします。"),
        TarotCard("the-magician","The Magician",listOf("willpower","focus","manifestation"),"自分の意思と技術を一点に集めるほど結果が現れます。"),
        TarotCard("the-high-priestess","The High Priestess",listOf("intuition","inner voice","mystery"),"外側の情報より、自分の違和感や直感を優先する局面です。"),
        TarotCard("the-empress","The Empress",listOf("growth","nurture","abundance"),"育てる姿勢が人間関係や仕事の成果を豊かにします。"),
        TarotCard("the-emperor","The Emperor",listOf("structure","authority","stability"),"感情よりもルールと段取りを整えることで前進できます。"),
        TarotCard("the-hierophant","The Hierophant",listOf("tradition","teaching","guidance"),"基本に立ち返り、信頼できる型や助言を取り入れることで道筋が見えます。"),
        TarotCard("the-lovers","The Lovers",listOf("choice","alignment","relationship"),"大切なのは好かれることより、自分の価値観に合う選択です。"),
        TarotCard("the-chariot","The Chariot",listOf("momentum","discipline","victory"),"迷いを減らして一点突破すると、状況を動かせます。"),
        TarotCard("strength","Strength",listOf("patience","courage","gentle control"),"強引さより、粘り強く向き合う姿勢が勝ち筋になります。"),
        TarotCard("the-hermit","The Hermit",listOf("reflection","solitude","wisdom"),"結論を急がず、ひとりで考える時間が精度を上げます。"),
        TarotCard("wheel-of-fortune","Wheel of Fortune",listOf("change","timing","turning point"),"運の波は変わり始めています。流れを読むことが重要です。"),
        TarotCard("justice","Justice",listOf("fairness","truth","accountability"),"感情だけでなく事実と責任の線引きを明確にするほど道が開けます。"),
        TarotCard("the-hanged-man","The Hanged Man",listOf("pause","surrender","new perspective"),"急いで動くより、見方を変えるための停止が状況を好転させます。"),
        TarotCard("death","Death",listOf("ending","transition","renewal"),"終わらせるべき流れを手放すことで、次の始まりに入れます。"),
        TarotCard("temperance","Temperance",listOf("balance","moderation","integration"),"極端に振れず、異なる要素を丁寧に混ぜ合わせる姿勢が鍵です。"),
        TarotCard("the-devil","The Devil",listOf("attachment","temptation","shadow"),"自分を縛っている習慣や執着を自覚すると、主導権を取り戻せます。"),
        TarotCard("the-tower","The Tower",listOf("shock","collapse","awakening"),"無理に保っていた前提が崩れることで、本質に立ち返る機会が来ます。"),
        TarotCard("the-star","The Star",listOf("hope","healing","guidance"),"先を急がず、回復と希望を信じるほど流れは静かに整います。"),
        TarotCard("the-moon","The Moon",listOf("uncertainty","intuition","subconscious"),"見えない不安に飲まれず、曖昧さの中で直感を磨くことが大切です。"),
        TarotCard("the-sun","The Sun",listOf("clarity","joy","success"),"素直さと明るさを前に出すほど、状況は分かりやすく前進します。"),
        TarotCard("judgement","Judgement",listOf("calling","reflection","rebirth"),"過去の流れを見直し、いま本当に応えるべき呼びかけに向き合う時です。"),
        TarotCard("the-world","The World",listOf("completion","integration","fulfillment"),"これまでの積み重ねがまとまり、ひとつの完成へ近づいています。")
    )

    fun draw(count:Int):List<DrawnCard> {
        val positions = when(count) {
            3 -> listOf("過去","現在","未来")
            5 -> listOf("現状","障害","隠れた要因","アドバイス","今後の流れ")
            else -> listOf("焦点")
        }
        return cards.shuffled().take(count).mapIndexed { i,c -> DrawnCard(c,positions[i],Random.nextBoolean()) }
    }

    fun drawWork():List<DrawnCard> = drawWithPositions(listOf("現状","強み・追い風","課題・障害","取るべき行動","今後の仕事運"))

    fun drawReconciliation():List<DrawnCard> = drawWithPositions(listOf("相手の気持ち","復縁の可能性","障害","あなたの一手","今後の流れ"))

    private fun drawWithPositions(positions:List<String>):List<DrawnCard> =
        cards.shuffled().take(positions.size).mapIndexed { i,c -> DrawnCard(c,positions[i],Random.nextBoolean()) }

    fun localText(question:String, draws:List<DrawnCard>):String = buildString {
        append("「$question」について\n\n")
        draws.forEach { d ->
            append("${d.position}：${d.card.name} ${if(d.reversed) "逆位置" else "正位置"}\n")
            append(d.card.meaning).append("\n")
            append("キーワード：${d.card.keywords.joinToString(" / ")}\n\n")
        }
        when(draws.size) {
            3 -> append("3枚の流れを、過去→現在→未来の順に見ながら、現実の判断材料として受け取ってください。")
            5 -> append("5枚それぞれの役割とカード同士のつながりを見ながら、現実の判断材料として受け取ってください。")
        }
    }
}
