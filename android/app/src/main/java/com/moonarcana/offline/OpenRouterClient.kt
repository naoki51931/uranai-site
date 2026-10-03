package com.moonarcana.offline

import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object OpenRouterClient {
    private const val endpoint="https://openrouter.ai/api/v1/chat/completions"

    fun interpret(apiKey:String,model:String,question:String,draws:List<DrawnCard>):String {
        require(apiKey.isNotBlank()){ "OpenRouter APIキーを設定してください。" }
        val cards=draws.joinToString("\n"){"${it.position}: ${it.card.name} ${if(it.reversed) "reversed" else "upright"}; keywords=${it.card.keywords.joinToString(", ")}; base=${it.card.meaning}"}
        val prompt="""あなたはMoon Arcanaのタロット解説AIです。占いを断定的な予言として扱わず、相談者が考えるための材料として、日本語で具体的かつ丁寧に解説してください。
質問: $question
カード:
$cards

構成: 1.全体像 2.各カードのつながり 3.注意点 4.今日からできる行動。800〜1200字程度。"""
        val payload=JSONObject().put("model",model).put("messages",JSONArray().put(JSONObject().put("role","user").put("content",prompt))).put("temperature",0.7).put("max_tokens",1800)
        return post(apiKey,payload)
    }

    fun interpretPalm(apiKey:String,model:String,question:String,leftImage:String?,rightImage:String?):String {
        require(apiKey.isNotBlank()){ "OpenRouter APIキーを設定してください。" }
        require(leftImage!=null || rightImage!=null){ "手のひら画像を1枚以上選択してください。" }
        val prompt="""あなたはMoon Arcanaの手相占いAIです。添付された手のひら画像を観察し、見える範囲だけを根拠に日本語で丁寧に読み解いてください。断定的な未来予測、医療・健康診断、寿命の断定はしないでください。
相談内容: $question
${if(leftImage!=null) "左手の画像があります。" else "左手画像はありません。"}
${if(rightImage!=null) "右手の画像があります。" else "右手画像はありません。"}

構成:
1. 左手（画像がある場合）
2. 右手（画像がある場合）
3. 総合リーディング
4. 次の一歩
生命線・知能線・感情線・運命線など、画像から確認できる線を中心に説明してください。"""
        val content=JSONArray().put(JSONObject().put("type","text").put("text",prompt))
        leftImage?.let{content.put(JSONObject().put("type","image_url").put("image_url",JSONObject().put("url",it)))}
        rightImage?.let{content.put(JSONObject().put("type","image_url").put("image_url",JSONObject().put("url",it)))}
        val payload=JSONObject().put("model",model).put("messages",JSONArray().put(JSONObject().put("role","user").put("content",content))).put("temperature",0.7).put("max_tokens",1800)
        return post(apiKey,payload)
    }

    private fun post(apiKey:String,payload:JSONObject):String {
        val conn=(URL(endpoint).openConnection() as HttpURLConnection).apply{
            requestMethod="POST";connectTimeout=20000;readTimeout=90000;doOutput=true
            setRequestProperty("Authorization","Bearer $apiKey");setRequestProperty("Content-Type","application/json");setRequestProperty("X-Title","Moon Arcana Android")
        }
        conn.outputStream.use{it.write(payload.toString().toByteArray())}
        val stream=if(conn.responseCode in 200..299) conn.inputStream else conn.errorStream
        val body=stream.bufferedReader().use{it.readText()}
        if(conn.responseCode !in 200..299) throw IllegalStateException("OpenRouter ${conn.responseCode}: ${runCatching{JSONObject(body).optJSONObject("error")?.optString("message")}.getOrNull()?:body.take(300)}")
        return JSONObject(body).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content").trim()
    }
}
