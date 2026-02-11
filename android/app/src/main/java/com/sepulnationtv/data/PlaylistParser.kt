package com.sepulnationtv.data

import com.sepulnationtv.model.Channel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

object PlaylistParser {

    private const val PLAYLIST_URL =
        "https://raw.githubusercontent.com/tenorioabsgit/iptv/main/playlist.m3u"

    suspend fun loadPlaylist(): LinkedHashMap<String, List<Channel>> = withContext(Dispatchers.IO) {
        val content = downloadPlaylist()
        val channels = parseM3U(content)
        groupChannels(channels)
    }

    private fun downloadPlaylist(): String {
        val url = URL(PLAYLIST_URL)
        val connection = url.openConnection() as HttpURLConnection
        connection.connectTimeout = 30_000
        connection.readTimeout = 30_000
        connection.requestMethod = "GET"
        return try {
            connection.inputStream.bufferedReader().readText()
        } finally {
            connection.disconnect()
        }
    }

    private fun parseM3U(content: String): List<Channel> {
        val lines = content.lines()
        val channels = mutableListOf<Channel>()
        var i = 0

        while (i < lines.size) {
            val line = lines[i].trim()

            if (line.startsWith("#EXTINF:")) {
                val logo = extractAttribute(line, "tvg-logo")
                val group = extractAttribute(line, "group-title")
                val name = line.substringAfterLast(",").trim()

                // Next non-empty line should be the URL
                var j = i + 1
                while (j < lines.size && lines[j].isBlank()) j++

                if (j < lines.size) {
                    val streamUrl = lines[j].trim()
                    if (streamUrl.startsWith("http")) {
                        channels.add(Channel(name, streamUrl, logo, group))
                    }
                    i = j + 1
                    continue
                }
            }
            i++
        }

        return channels
    }

    private fun extractAttribute(line: String, attr: String): String {
        val pattern = "$attr=\""
        val start = line.indexOf(pattern)
        if (start == -1) return ""
        val valueStart = start + pattern.length
        val end = line.indexOf("\"", valueStart)
        if (end == -1) return ""
        return line.substring(valueStart, end)
    }

    private fun groupChannels(channels: List<Channel>): LinkedHashMap<String, List<Channel>> {
        val grouped = linkedMapOf<String, List<Channel>>()

        // "Todos" first with all channels
        grouped["Todos (${channels.size})"] = channels

        // Group by category
        val byGroup = channels.groupBy { it.group.ifEmpty { "Outros" } }

        // BR categories first, sorted alphabetically
        val brGroups = byGroup.filter { it.key.startsWith("BR ") }.toSortedMap()
        val otherGroups = byGroup.filter {
            !it.key.startsWith("BR ") && it.key != "Outros"
        }.toSortedMap()
        val outros = byGroup["Outros"]

        brGroups.forEach { (key, value) ->
            grouped["$key (${value.size})"] = value.sortedBy { it.name }
        }

        otherGroups.forEach { (key, value) ->
            grouped["$key (${value.size})"] = value.sortedBy { it.name }
        }

        if (outros != null) {
            grouped["Outros (${outros.size})"] = outros.sortedBy { it.name }
        }

        return grouped
    }
}
