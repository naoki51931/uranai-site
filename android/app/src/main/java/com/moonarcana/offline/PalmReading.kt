package com.moonarcana.offline

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import java.io.ByteArrayOutputStream

object PalmReading {
    fun imageDataUrl(activity: MainActivity, uri: Uri): String {
        val bytes=activity.contentResolver.openInputStream(uri)?.use{it.readBytes()} ?: error("画像を読み込めませんでした")
        val source=BitmapFactory.decodeByteArray(bytes,0,bytes.size) ?: error("画像形式を読み込めませんでした")
        val max=1600
        val ratio=minOf(1f,max.toFloat()/maxOf(source.width,source.height).toFloat())
        val bitmap=if(ratio<1f) Bitmap.createScaledBitmap(source,(source.width*ratio).toInt(),(source.height*ratio).toInt(),true) else source
        val out=ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG,86,out)
        if(bitmap!==source) bitmap.recycle()
        source.recycle()
        return "data:image/jpeg;base64,"+Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP)
    }
}
