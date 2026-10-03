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
        val conn=(URL(endpoint).openConnection() as HttpURLConnection).apply{
            requestMethod="POST"; connectTimeout=20000; readTimeout=60000; doOutput=true
            setRequestProperty("Authorization","Bearer $apiKey"); setRequestProperty("Content-Type","application/json"); setRequestProperty("X-Title","Moon Arcana Android")
        }
        conn.outputStream.use{it.write(payload.toString().toByteArray())}
        val stream=if(conn.responseCode in 200..299) conn.inputStream else conn.errorStream
        val body=stream.bufferedReader().use{it.readText()}
        if(conn.responseCode !in 200..299) throw IllegalStateException("OpenRouter ${conn.responseCode}: ${runCatching{JSONObject(body).optJSONObject("error")?.optString("message")}.getOrNull()?:body.take(300)}")
        return JSONObject(body).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content").trim()
    }
}
