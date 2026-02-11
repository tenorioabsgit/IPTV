package com.sepulnationtv.data

import com.sepulnationtv.model.Channel

object ChannelRepository {
    var currentChannels: List<Channel> = emptyList()
    var currentIndex: Int = 0
}
