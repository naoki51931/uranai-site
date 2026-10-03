package com.moonarcana.offline

import android.graphics.Color
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton

class MainActivity:AppCompatActivity(){
    private lateinit var root:LinearLayout
    private lateinit var store:SecretStore
    private lateinit var db:HistoryDb
    private var current:List<DrawnCard> = emptyList()
    private var currentQuestion=""
    private var currentLocal=""

    override fun onCreate(savedInstanceState:Bundle?){super.onCreate(savedInstanceState);store=SecretStore(this);db=HistoryDb(this);showHome()}
    private fun base(title:String):LinearLayout{
        val scroll=ScrollView(this).apply{setBackgroundColor(Color.rgb(15,11,31))}
        root=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL;setPadding(42,52,42,64)}
        scroll.addView(root);setContentView(scroll)
        root.addView(TextView(this).apply{text=title;textSize=28f;setTextColor(Color.rgb(246,196,83));gravity=Gravity.CENTER_HORIZONTAL;setPadding(0,0,0,28)})
        return root
    }
    private fun text(s:String,size:Float=16f)=TextView(this).apply{text=s;textSize=size;setTextColor(Color.WHITE);setPadding(0,12,0,12);setLineSpacing(4f,1.05f)}
    private fun button(label:String,action:()->Unit)=MaterialButton(this).apply{text=label;setOnClickListener{action()};setPadding(8,10,8,10)}
    private fun input(hint:String)=EditText(this).apply{this.hint=hint;setHintTextColor(Color.LTGRAY);setTextColor(Color.WHITE);setSingleLine(false);minLines=2}
    private fun cardImage(d:DrawnCard)=ImageView(this).apply{
        val resourceName=d.card.slug.replace("-","_")
        val id=resources.getIdentifier(resourceName,"drawable",packageName)
        if(id!=0)setImageResource(id)
        adjustViewBounds=true
        scaleType=ImageView.ScaleType.FIT_CENTER
        rotation=if(d.reversed)180f else 0f
        contentDescription="${d.card.name} ${if(d.reversed) "逆位置" else "正位置"}"
        layoutParams=LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT,720).apply{setMargins(0,18,0,18)}
    }

    private fun showHome(){
        base("Moon Arcana")
        root.addView(text("カード画像・抽選・基本解釈・履歴は端末内で動作します。AI詳細解説を押した時だけOpenRouterへ質問とカード情報を送信します。",17f))
        root.addView(button("1枚引き"){showReading(1)})
        root.addView(button("3枚引き（過去・現在・未来）"){showReading(3)})
        root.addView(button("占い履歴（オフライン）"){showHistory()})
        root.addView(button("OpenRouter設定"){showSettings()})
        root.addView(text("通信先: OpenRouter API のみ。カード画像はアプリに同梱済みです。",13f))
    }
    private fun showReading(count:Int){
        base(if(count==1) "1枚引き" else "3枚引き")
        val q=input("相談内容を入力（例：今の仕事についてどう動く？）");root.addView(q)
        root.addView(button("カードを引く"){
            currentQuestion=q.text.toString().trim().ifBlank{"今日の運勢"};current=Tarot.draw(count);currentLocal=Tarot.localText(currentQuestion,current)
            renderResult()
        })
        root.addView(button("← ホーム"){showHome()})
    }
    private fun renderResult(){
        root.removeViews(2,root.childCount-2)
        current.forEach{d->
            root.addView(text("${d.position}\n✦ ${d.card.name}  ${if(d.reversed) "逆位置" else "正位置"}",18f))
            root.addView(cardImage(d))
            root.addView(text("${d.card.keywords.joinToString(" / ")}\n${d.card.meaning}",16f))
        }
        root.addView(text(currentLocal,16f))
        root.addView(button("この結果を端末に保存"){save(null)})
        root.addView(button("AIで詳細解説（OpenRouter通信）"){ai()})
        root.addView(button("← ホーム"){showHome()})
    }
    private fun save(ai:String?){val cards=current.joinToString(" / "){"${it.card.name}(${if(it.reversed) "逆" else "正"})"};db.add(currentQuestion,cards,currentLocal,ai);Toast.makeText(this,"端末に保存しました",Toast.LENGTH_SHORT).show()}
    private fun ai(){
        if(store.apiKey.isBlank()){Toast.makeText(this,"先にOpenRouter設定でAPIキーを保存してください",Toast.LENGTH_LONG).show();return}
        val progress=ProgressBar(this);root.addView(progress)
        Thread{
            val result=runCatching{OpenRouterClient.interpret(store.apiKey,store.model,currentQuestion,current)}
            runOnUiThread{root.removeView(progress);result.onSuccess{answer->root.addView(text("AI詳細解説\n\n$answer",17f));root.addView(button("AI解説込みで保存"){save(answer)})}.onFailure{Toast.makeText(this,it.message?:"OpenRouter通信に失敗しました",Toast.LENGTH_LONG).show()}}
        }.start()
    }
    private fun showHistory(){base("占い履歴");val rows=db.latest();if(rows.isEmpty())root.addView(text("まだ履歴はありません。")) else rows.forEach{root.addView(text(it,15f));root.addView(View(this).apply{setBackgroundColor(Color.DKGRAY);layoutParams=LinearLayout.LayoutParams(-1,1)})};root.addView(button("← ホーム"){showHome()})}
    private fun showSettings(){
        base("OpenRouter設定")
        root.addView(text("APIキーはAndroid KeystoreのAES鍵で暗号化して端末内に保存します。アプリに固定キーは埋め込みません。"))
        val key=input("OpenRouter API key (sk-or-v1-...)").apply{inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD;minLines=1}
        val model=input("モデル名").apply{setText(store.model);minLines=1};root.addView(key);root.addView(model)
        root.addView(button("設定を保存"){if(key.text.isNotBlank())store.apiKey=key.text.toString().trim();store.model=model.text.toString().trim().ifBlank{"openai/gpt-4.1-mini"};Toast.makeText(this,"保存しました",Toast.LENGTH_SHORT).show()})
        root.addView(button("APIキーを削除"){store.apiKey="";Toast.makeText(this,"APIキーを削除しました",Toast.LENGTH_SHORT).show()})
        root.addView(button("← ホーム"){showHome()})
    }
}
