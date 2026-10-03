package com.moonarcana.offline

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class SecretStore(private val context:Context) {
    private val prefs=context.getSharedPreferences("moon_arcana",Context.MODE_PRIVATE)
    private val alias="moon_arcana_openrouter"
    private fun key():SecretKey {
        val ks=KeyStore.getInstance("AndroidKeyStore").apply{load(null)}
        (ks.getKey(alias,null) as? SecretKey)?.let{return it}
        val gen=KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore")
        gen.init(KeyGenParameterSpec.Builder(alias,KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT).setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build())
        return gen.generateKey()
    }
    var apiKey:String
        get(){
            val raw=prefs.getString("api_key",null)?:return ""
            return try { val all=Base64.decode(raw,Base64.NO_WRAP); val iv=all.copyOfRange(0,12); val enc=all.copyOfRange(12,all.size); val c=Cipher.getInstance("AES/GCM/NoPadding"); c.init(Cipher.DECRYPT_MODE,key(),GCMParameterSpec(128,iv)); String(c.doFinal(enc),Charsets.UTF_8) } catch(_:Exception){""}
        }
        set(value){
            if(value.isBlank()){prefs.edit().remove("api_key").apply();return}
            val c=Cipher.getInstance("AES/GCM/NoPadding"); c.init(Cipher.ENCRYPT_MODE,key()); val enc=c.doFinal(value.toByteArray()); val all=c.iv+enc; prefs.edit().putString("api_key",Base64.encodeToString(all,Base64.NO_WRAP)).apply()
        }
    var model:String
        get()=prefs.getString("model","openai/gpt-4.1-mini")?:"openai/gpt-4.1-mini"
        set(v){prefs.edit().putString("model",v.trim()).apply()}
}

class HistoryDb(context:Context):SQLiteOpenHelper(context,"moon_arcana.db",null,1){
    override fun onCreate(db:SQLiteDatabase){db.execSQL("CREATE TABLE readings(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at INTEGER NOT NULL, question TEXT NOT NULL, cards TEXT NOT NULL, local_text TEXT NOT NULL, ai_text TEXT)")}
    override fun onUpgrade(db:SQLiteDatabase,oldVersion:Int,newVersion:Int){}
    fun add(question:String,cards:String,local:String,ai:String?){writableDatabase.execSQL("INSERT INTO readings(created_at,question,cards,local_text,ai_text) VALUES(?,?,?,?,?)", arrayOf(System.currentTimeMillis(),question,cards,local,ai))}
    fun latest(limit:Int=30):List<String>{
        val out=mutableListOf<String>(); readableDatabase.rawQuery("SELECT created_at,question,cards,COALESCE(ai_text,local_text) FROM readings ORDER BY id DESC LIMIT ?", arrayOf(limit.toString())).use{c->while(c.moveToNext()){out += "${java.text.SimpleDateFormat("yyyy/MM/dd HH:mm",java.util.Locale.JAPAN).format(java.util.Date(c.getLong(0)))}\n${c.getString(1)}\n${c.getString(2)}\n${c.getString(3)}"}}
        return out
    }
}
