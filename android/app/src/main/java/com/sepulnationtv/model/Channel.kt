package com.sepulnationtv.model

import java.io.Serializable

data class Channel(
    val name: String,
    val url: String,
    val logo: String,
    val group: String
) : Serializable {

    val streamFormat: String
        get() = when {
            url.contains(".m3u8", ignoreCase = true) -> "HLS"
            url.contains(".mpd", ignoreCase = true) -> "DASH"
            url.contains(".mp4", ignoreCase = true) -> "MP4"
            else -> "HLS"
        }

    val description: String
        get() = "Categoria: $group\nFormato: $streamFormat"
}
