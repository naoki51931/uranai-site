package com.moonarcana.offline

import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
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
    private val bg=Color.rgb(13,9,29)
    private val panel=Color.rgb(28,20,51)
    private val gold=Color.rgb(241,194,92)
    private val muted=Color.rgb(198,190,215)

    override fun onCreate(savedInstanceState:Bundle?){super.onCreate(savedInstanceState);store=SecretStore(this);db=HistoryDb(this);showHome()}
    private fun dp(v:Int)=(v*resources.displayMetrics.density).toInt()
    private fun shape(color:Int,radius:Int=22,stroke:Int?=null)=GradientDrawable().apply{setColor(color);cornerRadius=dp(radius).toFloat();stroke?.let{setStroke(dp(1),it)}}
    private fun centeredParams(width:Int=ViewGroup.LayoutParams.MATCH_PARENT)=LinearLayout.LayoutParams(width,ViewGroup.LayoutParams.WRAP_CONTENT).apply{gravity=Gravity.CENTER_HORIZONTAL;setMargins(0,dp(8),0,dp(8))}
    private fun base(title:String,subtitle:String?=null):LinearLayout{val scroll=ScrollView(this).apply{setBackgroundColor(bg);isFillViewport=true};root=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL;gravity=Gravity.TOP or Gravity.CENTER_HORIZONTAL;setPadding(dp(22),dp(34),dp(22),dp(50))};scroll.addView(root,ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT));setContentView(scroll);root.addView(TextView(this).apply{text="✦  $title  ✦";textSize=29f;setTextColor(gold);gravity=Gravity.CENTER;setTypeface(typeface,Typeface.BOLD);layoutParams=centeredParams()});subtitle?.let{root.addView(text(it,14f,muted).apply{setPadding(dp(12),0,dp(12),dp(14))})};root.addView(View(this).apply{setBackgroundColor(Color.rgb(77,60,105));layoutParams=LinearLayout.LayoutParams(dp(92),dp(1)).apply{gravity=Gravity.CENTER_HORIZONTAL;setMargins(0,dp(4),0,dp(18))}});return root}
    private fun text(s:String,size:Float=16f,color:Int=Color.WHITE)=TextView(this).apply{text=s;textSize=size;setTextColor(color);gravity=Gravity.CENTER;setPadding(dp(8),dp(10),dp(8),dp(10));setLineSpacing(dp(3).toFloat(),1.08f);layoutParams=centeredParams()}
    private fun sectionTitle(s:String)=text(s,19f,gold).apply{setTypeface(typeface,Typeface.BOLD);setPadding(dp(8),dp(18),dp(8),dp(6))}
    private fun button(label:String,action:()->Unit)=MaterialButton(this).apply{text=label;textSize=16f;isAllCaps=false;gravity=Gravity.CENTER;setTextColor(Color.rgb(25,17,39));backgroundTintList=android.content.res.ColorStateList.valueOf(gold);cornerRadius=dp(18);minHeight=dp(54);setOnClickListener{action()};layoutParams=centeredParams()}
    private fun secondaryButton(label:String,action:()->Unit)=MaterialButton(this).apply{text=label;textSize=15f;isAllCaps=false;gravity=Gravity.CENTER;setTextColor(Color.WHITE);backgroundTintList=android.content.res.ColorStateList.valueOf(Color.rgb(49,37,75));cornerRadius=dp(18);minHeight=dp(50);setOnClickListener{action()};layoutParams=centeredParams()}
    private fun input(hint:String)=EditText(this).apply{this.hint=hint;setHintTextColor(Color.rgb(158,149,177));setTextColor(Color.WHITE);setSingleLine(false);minLines=3;gravity=Gravity.CENTER;setPadding(dp(18),dp(16),dp(18),dp(16));background=shape(panel,20,Color.rgb(83,66,112));layoutParams=centeredParams()}
    private fun cardImage(d:DrawnCard)=ImageView(this).apply{val id=resources.getIdentifier(d.card.slug.replace("-","_"),"drawable",packageName);if(id!=0)setImageResource(id);adjustViewBounds=true;scaleType=ImageView.ScaleType.FIT_CENTER;rotation=if(d.reversed)180f else 0f;contentDescription="${d.card.name} ${if(d.reversed) "逆位置" else "正位置"}";layoutParams=LinearLayout.LayoutParams(dp(250),dp(430)).apply{gravity=Gravity.CENTER_HORIZONTAL;setMargins(0,dp(12),0,dp(12))}}
    private fun panelView():LinearLayout=LinearLayout(this).apply{orientation=LinearLayout.VERTICAL;gravity=Gravity.CENTER_HORIZONTAL;background=shape(panel,24,Color.rgb(73,56,102));setPadding(dp(16),dp(16),dp(16),dp(16));layoutParams=centeredParams()}

    private fun showHome(){base("Moon Arcana","静かな時間にカードを引き、今の気持ちを見つめるためのタロット。");val hero=panelView();hero.addView(text("☾",42f,gold));hero.addView(text("問いを心に浮かべて\n占い方を選んでください",18f));root.addView(hero);root.addView(sectionTitle("TAROT READING"));root.addView(button("✦  1枚引き"){showReading(1)});root.addView(button("✦  3枚引き  — 過去・現在・未来"){showReading(3)});root.addView(button("✦  5枚引き  — 総合"){showReading(5)});root.addView(sectionTitle("SPECIAL SPREAD"));root.addView(secondaryButton("仕事運  5枚引き"){showFiveCardReading("仕事運 5枚引き","仕事について知りたいことを入力",Tarot::drawWork)});root.addView(secondaryButton("復縁  5枚引き"){showFiveCardReading("復縁 5枚引き","相手との関係や知りたいことを入力",Tarot::drawReconciliation)});root.addView(sectionTitle("MY ARCANA"));root.addView(secondaryButton("占い履歴"){showHistory()});root.addView(secondaryButton("AIモデル・OpenRouter設定"){showSettings()});root.addView(text("カードと履歴は端末内に保存。AI詳細解説の時だけOpenRouterへ接続します。",12f,muted))}
    private fun showReading(count:Int){val title=when(count){1->"1枚引き";3->"3枚引き";else->"5枚引き（総合）"};base(title,"相談内容を入力してカードを引いてください。");val q=input("相談内容を入力");root.addView(q);root.addView(button("カードを引く"){currentQuestion=q.text.toString().trim().ifBlank{"今日の運勢"};current=Tarot.draw(count);currentLocal=Tarot.localText(currentQuestion,current);renderResult()});root.addView(secondaryButton("← ホーム"){showHome()})}
    private fun showFiveCardReading(title:String,hint:String,draw:()->List<DrawnCard>){base(title,"5つの視点から流れを読み解きます。");val q=input(hint);root.addView(q);root.addView(button("5枚のカードを引く"){currentQuestion=q.text.toString().trim().ifBlank{title};current=draw();currentLocal=Tarot.localText(currentQuestion,current);renderResult()});root.addView(secondaryButton("← ホーム"){showHome()})}
    private fun renderResult(){root.removeViews(2,root.childCount-2);root.addView(text("「$currentQuestion」",17f,gold));current.forEachIndexed{i,d->val p=panelView();p.addView(text("${i+1}  ·  ${d.position}",15f,gold));p.addView(text(d.card.name,22f).apply{setTypeface(typeface,Typeface.BOLD)});p.addView(text(if(d.reversed) "逆位置" else "正位置",14f,muted));p.addView(cardImage(d));p.addView(text(d.card.keywords.joinToString("  ·  "),13f,gold));p.addView(text(d.card.meaning,15f));root.addView(p)};root.addView(sectionTitle("READING"));root.addView(text(currentLocal,15f));root.addView(button("この結果を端末に保存"){save(null)});root.addView(button("AIで詳細解説  ·  ${modelLabel(store.model)}"){ai()});root.addView(secondaryButton("← ホーム"){showHome()})}
    private fun save(ai:String?){val cards=current.joinToString(" / "){"${it.card.name}(${if(it.reversed) "逆" else "正"})"};db.add(currentQuestion,cards,currentLocal,ai);Toast.makeText(this,"端末に保存しました",Toast.LENGTH_SHORT).show()}
    private fun ai(){if(store.apiKey.isBlank()){Toast.makeText(this,"先にOpenRouter設定でAPIキーを保存してください",Toast.LENGTH_LONG).show();return};val progress=ProgressBar(this).apply{layoutParams=LinearLayout.LayoutParams(dp(48),dp(48)).apply{gravity=Gravity.CENTER_HORIZONTAL;setMargins(0,dp(20),0,dp(20))}};root.addView(progress);Thread{val result=runCatching{OpenRouterClient.interpret(store.apiKey,store.model,currentQuestion,current)};runOnUiThread{root.removeView(progress);result.onSuccess{answer->val p=panelView();p.addView(sectionTitle("AI READING · ${modelLabel(store.model)}"));p.addView(text(answer,16f));root.addView(p);root.addView(button("AI解説込みで保存"){save(answer)})}.onFailure{Toast.makeText(this,it.message?:"OpenRouter通信に失敗しました",Toast.LENGTH_LONG).show()}}}.start()}
    private fun showHistory(){base("占い履歴","端末に保存したリーディングです。");val rows=db.latest();if(rows.isEmpty())root.addView(text("まだ履歴はありません。",16f,muted)) else rows.forEach{val p=panelView();p.addView(text(it,14f));root.addView(p)};root.addView(secondaryButton("← ホーム"){showHome()})}

    private data class ModelOption(val label:String,val id:String)
    private fun modelOptions()=listOf(
        ModelOption("GPT-4.1 mini  ·  バランス","openai/gpt-4.1-mini"),
        ModelOption("GPT-4.1  ·  高精度","openai/gpt-4.1"),
        ModelOption("GPT-4.1 nano  ·  軽量","openai/gpt-4.1-nano"),
        ModelOption("Gemini 3 Flash Preview  ·  高速・高性能","google/gemini-3-flash-preview"),
        ModelOption("Gemini 2.5 Flash","google/gemini-2.5-flash"),
        ModelOption("Gemini 2.5 Pro","google/gemini-2.5-pro"),
        ModelOption("Claude Sonnet 4","anthropic/claude-sonnet-4"),
        ModelOption("DeepSeek Chat V3","deepseek/deepseek-chat-v3-0324"),
        ModelOption("その他（モデルIDを入力）","custom")
    )
    private fun modelLabel(id:String)=modelOptions().firstOrNull{it.id==id}?.label?.substringBefore("  ·") ?: id.substringAfterLast('/')
    private fun showSettings(){base("AIモデル設定","占いのAI詳細解説に使うモデルを選択できます。");root.addView(text("現在のモデル\n${modelLabel(store.model)}\n${store.model}",15f,gold));val key=input("OpenRouter API key (sk-or-v1-...)").apply{inputType=InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD;minLines=1};root.addView(key);root.addView(sectionTitle("MODEL"));val options=modelOptions();val labels=options.map{it.label};val spinner=Spinner(this).apply{adapter=ArrayAdapter(this@MainActivity,android.R.layout.simple_spinner_dropdown_item,labels);layoutParams=centeredParams();background=shape(Color.rgb(49,37,75),18,Color.rgb(83,66,112));setPadding(dp(14),dp(10),dp(14),dp(10));val idx=options.indexOfFirst{it.id==store.model};setSelection(if(idx>=0)idx else options.lastIndex)};root.addView(spinner);val custom=input("OpenRouterモデルID（例: provider/model-name）").apply{minLines=1;visibility=if(options.any{it.id==store.model}) View.GONE else View.VISIBLE;if(visibility==View.VISIBLE)setText(store.model)};root.addView(custom);spinner.onItemSelectedListener=object:AdapterView.OnItemSelectedListener{override fun onItemSelected(parent:AdapterView<*>?,view:View?,position:Int,id:Long){custom.visibility=if(options[position].id=="custom")View.VISIBLE else View.GONE};override fun onNothingSelected(parent:AdapterView<*>?){}};root.addView(button("設定を保存"){if(key.text.isNotBlank())store.apiKey=key.text.toString().trim();val selected=options[spinner.selectedItemPosition];val model=if(selected.id=="custom")custom.text.toString().trim() else selected.id;if(model.isBlank()){Toast.makeText(this,"モデルIDを入力してください",Toast.LENGTH_LONG).show();return@button};store.model=model;Toast.makeText(this,"${modelLabel(model)} を保存しました",Toast.LENGTH_SHORT).show();showSettings()});root.addView(secondaryButton("APIキーを削除"){store.apiKey="";Toast.makeText(this,"APIキーを削除しました",Toast.LENGTH_SHORT).show()});root.addView(secondaryButton("← ホーム"){showHome()})}
}
